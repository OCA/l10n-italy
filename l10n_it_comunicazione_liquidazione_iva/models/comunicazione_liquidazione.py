# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError
from lxml import etree


NS_IV = 'urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp'
NS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'
NS_LOCATION = 'urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp'
NS_MAP = {
    'iv': NS_IV,
    'xsi': NS_XSI,
    #'schemaLocation': NS_LOCATION
}
etree.register_namespace("vi", NS_IV)


class ComunicazioneLiquidazione(models.Model):
    _name = 'comunicazione.liquidazione'
    _description = 'Comunicazione Liquidazione IVA'

    @api.model
    def _default_company(self):
        company_id = self._context.get(
            'company_id', self.env.user.company_id.id)
        return company_id

    @api.constrains('identificativo')
    def _check_identificativo(self):
        domain = [('identificativo', '=', self.identificativo)]
        dichiarazioni = self.search(domain)
        if len(dichiarazioni) > 1:
            raise ValidationError(
                _("Dichiarazione già esiste con identificativo {}"
                  ).format(self.identificativo))

    @api.multi
    def _compute_name(self):
        for dich in self:
            name = ""
            for quadro in dich.quadri_vp_ids:
                if not name:
                    period_type = ''
                    if quadro.period_type == 'month':
                        period_type = _('month')
                    else:
                        period_type = _('quarter')
                    name += '{} {}'.format(str(dich.year), period_type)
                if quadro.period_type == 'month':
                    name += ', {}'.format(str(quadro.month))
                else:
                    name += ', {}'.format(str(quadro.quarter))
            dich.name = name

    def _get_identificativo(self):
        dichiarazioni = self.search([])
        if dichiarazioni:
            return len(dichiarazioni) + 1
        else:
            return 1

    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=_default_company)
    identificativo = fields.Integer(string='Identificativo',
                                    default=_get_identificativo)
    name = fields.Char(string='Name', compute="_compute_name")
    year = fields.Integer(string='Year', required=True, size=4)
    last_month = fields.Integer(string='Last month')
    liquidazione_del_gruppo = fields.Boolean(string='Liquidazione del gruppo')
    taxpayer_vat = fields.Char(string='Vat', required=True)
    controller_vat = fields.Char(string='Controller Vat')
    taxpayer_fiscalcode = fields.Char(string='Fiscalcode')
    declarant_different = fields.Boolean(
        string='Declarant different from taxpayer')
    declarant_fiscalcode = fields.Char(string='Fiscalcode')
    declarant_fiscalcode_company = fields.Char(string='Fiscalcode company')
    codice_carica_id = fields.Many2one('codice.carica', string='Codice carica')
    declarant_sign = fields.Boolean(string='Declarant sign', default=True)

    delegate_fiscalcode = fields.Char(string='Fiscalcode')
    delegate_commitment = fields.Selection(
        [('1', 'Comunicazione è stata predisposta dal contribuente '),
         ('2', 'Comunicazione è stata predisposta da chi effettua l\'invio')],
        string='Commitment')
    delegate_sign = fields.Boolean(string='Delegate sign')
    date_commitment = fields.Date(string='Date commitment')
    quadri_vp_ids = fields.One2many(
        'comunicazione.liquidazione.vp', 'comunicazione_id',
        string="Quadri VP")
    iva_da_versare = fields.Float(
        string='IVA da versare', readonly=True)
    iva_a_credito = fields.Float(
        string='IVA a credito', readonly=True)

    @api.model
    def create(self, vals):
        comunicazione = super(ComunicazioneLiquidazione, self).create(vals)
        comunicazione._validate()
        return comunicazione

    @api.multi
    def write(self, vals):
        super(ComunicazioneLiquidazione, self).write(vals)
        for comunicazione in self:
            comunicazione._validate()
        return True

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            if self.company_id.partner_id.vat:
                self.taxpayer_vat = self.company_id.partner_id.vat[2:]
            else:
                self.taxpayer_vat = ''
            self.taxpayer_fiscalcode = \
                self.company_id.partner_id.fiscalcode

    def get_export_xml(self):
        self._validate()
        x1_Fornitura = self._export_xml_get_fornitura()

        x1_1_Intestazione = self._export_xml_get_intestazione()

        attrs = {
            'identificativo': str(self.identificativo).zfill(5)
        }
        x1_2_Comunicazione = etree.Element(
            etree.QName(NS_IV, "Comunicazione"), attrs)
        x1_2_1_Frontespizio = self._export_xml_get_frontespizio()
        x1_2_Comunicazione.append(x1_2_1_Frontespizio)

        x1_2_2_DatiContabili = etree.Element(
            etree.QName(NS_IV, "DatiContabili"))
        nr_modulo = 0
        for quadro in self.quadri_vp_ids:
            nr_modulo += 1
            modulo = self.with_context(nr_modulo=nr_modulo)\
                ._export_xml_get_dati_modulo(quadro)
            x1_2_2_DatiContabili.append(modulo)
        x1_2_Comunicazione.append(x1_2_2_DatiContabili)
        # Composizione struttura xml con le varie sezioni generate
        x1_Fornitura.append(x1_1_Intestazione)
        x1_Fornitura.append(x1_2_Comunicazione)

        xml_string = etree.tostring(
            x1_Fornitura, encoding='utf8', method='xml', pretty_print=True)
        return xml_string

    def _validate(self):
        """
        Controllo congruità dati della comunicazione
        """
        # Anno obbligatorio
        if not self.year:
            raise ValidationError(
                _("Year required"))

        # Codice Fiscale
        if not self.taxpayer_fiscalcode \
                or len(self.taxpayer_fiscalcode) not in [11, 16]:
            raise ValidationError(
                _("Taxpayer Fiscalcode is required. It's accepted codes \
                    with lenght 11 or 16 chars"))

        # Codice Fiscale dichiarante Obbligatorio se il codice fiscale
        # del contribuente è di 11 caratteri
        if self.taxpayer_fiscalcode  and len(self.taxpayer_fiscalcode) == 11\
                and not self.declarant_fiscalcode:
            raise ValidationError(
                _("Declarant Fiscalcode is required. You can enable the \
                section with different declarant option"))

        # LiquidazioneGruppo: elemento opzionale, di tipo DatoCB_Type.
        # Se presente non deve essere presente l'elemento PIVAControllante.
        # Non può essere presente se l'elemento CodiceFiscale è lungo 16
        # caratteri.
        if self.liquidazione_del_gruppo:
            if self.controller_vat:
                raise ValidationError(
                    _("Per liquidazione del gruppo, partita iva controllante\
                     deve essere vuota"))
            if len(self.taxpayer_fiscalcode) == 16:
                raise ValidationError(
                    _("Liquidazione del gruppo non valida, visto il codice\
                     fiscale di 16 caratteri"))
        # CodiceCaricaDichiarante
        if self.declarant_fiscalcode:
            if not self.codice_carica_id:
                raise ValidationError(
                    _("Indicare il codice carica del dichiarante"))
        # CodiceFiscaleSocieta:
        # Obbligatori per codice carica 9
        if self.codice_carica_id and self.codice_carica_id.code == '9':
            if not self.declarant_fiscalcode_company:
                raise ValidationError(
                    _("Visto il codice carica, occorre indicare il codice \
                    fiscale della socità dichiarante"))
        # ImpegnoPresentazione::
        if self.delegate_fiscalcode:
            if not self.delegate_commitment:
                raise ValidationError(
                    _("Visto il codice fiscale dell'intermediario, occorre \
                    indicare il codice l'impegno"))
            if not self.date_commitment:
                raise ValidationError(
                    _("Visto il codice fiscale dell'intermediario, occorre \
                    indicare la data dell'impegno"))
        # ImpegnoPresentazione::
        if self.delegate_fiscalcode and not self.delegate_sign:
            raise ValidationError(
                _("In presenza dell'incaricato nella sezione impegno \
                    alla presentazione telematica, è necessario vistare \
                    l'opzione firma dell'incaricato"))
        return True

    def _export_xml_get_fornitura(self):
        x1_Fornitura = etree.Element(
            etree.QName(NS_IV, "Fornitura"), nsmap=NS_MAP)
        return x1_Fornitura

    def _export_xml_validate(self):
        return True

    def _export_xml_get_intestazione(self):
        x1_1_Intestazione = etree.Element(etree.QName(NS_IV, "Intestazione"))
        # Codice Fornitura
        x1_1_1_CodiceFornitura = etree.SubElement(
            x1_1_Intestazione, etree.QName(NS_IV, "CodiceFornitura"))
        code = str(self.year)[-2:]
        x1_1_1_CodiceFornitura.text = unicode('IVP{}'.format(code))
        # Codice Fiscale Dichiarante
        if self.declarant_fiscalcode:
            x1_1_2_CodiceFiscaleDichiarante = etree.SubElement(
                x1_1_Intestazione, etree.QName(NS_IV,
                                               "CodiceFiscaleDichiarante"))
            x1_1_2_CodiceFiscaleDichiarante.text = unicode(
                self.declarant_fiscalcode)
        # Codice Carica
        if self.codice_carica_id:
            x1_1_3_CodiceCarica = etree.SubElement(
                x1_1_Intestazione, etree.QName(NS_IV, "CodiceCarica"))
            x1_1_3_CodiceCarica.text = unicode(self.codice_carica_id.code)
        return x1_1_Intestazione

    def _export_xml_get_frontespizio(self):
        x1_2_1_Frontespizio = etree.Element(etree.QName(NS_IV, "Frontespizio"))
        # Codice Fiscale
        x1_2_1_1_CodiceFiscale = etree.SubElement(
            x1_2_1_Frontespizio, etree.QName(NS_IV, "CodiceFiscale"))
        x1_2_1_1_CodiceFiscale.text = unicode(self.taxpayer_fiscalcode) \
            if self.taxpayer_fiscalcode else ''
        # Anno Imposta
        x1_2_1_2_AnnoImposta = etree.SubElement(
            x1_2_1_Frontespizio, etree.QName(NS_IV, "AnnoImposta"))
        x1_2_1_2_AnnoImposta.text = str(self.year)
        # Partita IVA
        x1_2_1_3_PartitaIVA = etree.SubElement(
            x1_2_1_Frontespizio, etree.QName(NS_IV, "PartitaIVA"))
        x1_2_1_3_PartitaIVA.text = self.taxpayer_vat
        # PIVA Controllante
        if self.controller_vat:
            x1_2_1_4_PIVAControllante = etree.SubElement(
                x1_2_1_Frontespizio, etree.QName(NS_IV, "PIVAControllante"))
            x1_2_1_4_PIVAControllante.text = self.controller_vat
        # Ultimo Mese
        if self.last_month:
            x1_2_1_5_UltimoMese = etree.SubElement(
                x1_2_1_Frontespizio, etree.QName(NS_IV, "UltimoMese"))
            x1_2_1_5_UltimoMese.text = self.last_month
        # Liquidazione Gruppo
        x1_2_1_6_LiquidazioneGruppo = etree.SubElement(
            x1_2_1_Frontespizio, etree.QName(NS_IV, "LiquidazioneGruppo"))
        x1_2_1_6_LiquidazioneGruppo.text = \
            '1' if self.liquidazione_del_gruppo else '0'
        # CF Dichiarante
        if self.declarant_fiscalcode:
            x1_2_1_7_CFDichiarante = etree.SubElement(
                x1_2_1_Frontespizio, etree.QName(NS_IV, "CFDichiarante"))
            x1_2_1_7_CFDichiarante.text = self.declarant_fiscalcode
        # CodiceCaricaDichiarante
        if self.codice_carica_id:
            x1_2_1_8_CodiceCaricaDichiarante = etree.SubElement(
                x1_2_1_Frontespizio,
                etree.QName(NS_IV, "CodiceCaricaDichiarante"))
            x1_2_1_8_CodiceCaricaDichiarante.text = self.codice_carica_id.code
        # CodiceFiscaleSocieta
        if self.declarant_fiscalcode_company:
            x1_2_1_9_CodiceFiscaleSocieta = etree.SubElement(
                x1_2_1_Frontespizio,
                etree.QName(NS_IV, "CodiceFiscaleSocieta"))
            x1_2_1_9_CodiceFiscaleSocieta.text =\
                self.declarant_fiscalcode_company.code
        # FirmaDichiarazione
        x1_2_1_10_FirmaDichiarazione = etree.SubElement(
            x1_2_1_Frontespizio, etree.QName(NS_IV, "FirmaDichiarazione"))
        x1_2_1_10_FirmaDichiarazione.text = '1' if self.declarant_sign else '0'
        # CFIntermediario
        if self.delegate_fiscalcode:
            x1_2_1_11_CFIntermediario = etree.SubElement(
                x1_2_1_Frontespizio, etree.QName(NS_IV, "CFIntermediario"))
            x1_2_1_11_CFIntermediario.text = self.delegate_fiscalcode
        # ImpegnoPresentazione
        if self.delegate_commitment:
            x1_2_1_12_ImpegnoPresentazione = etree.SubElement(
                x1_2_1_Frontespizio, etree.QName(NS_IV, "ImpegnoPresentazione"))
            x1_2_1_12_ImpegnoPresentazione.text = self.delegate_commitment
        # DataImpegno
        if self.date_commitment:
            x1_2_1_13_DataImpegno = etree.SubElement(
                x1_2_1_Frontespizio, etree.QName(NS_IV, "DataImpegno"))
            x1_2_1_13_DataImpegno.text = datetime.strptime(
                self.date_commitment, "%Y-%m-%d").strftime('%d%m%Y')
        # FirmaIntermediario
        if self.delegate_fiscalcode:
            x1_2_1_14_FirmaIntermediario = etree.SubElement(
                x1_2_1_Frontespizio, etree.QName(NS_IV, "FirmaIntermediario"))
            x1_2_1_14_FirmaIntermediario.text =\
                '1' if self.delegate_sign else '0'

        return x1_2_1_Frontespizio

    def _export_xml_get_dati_modulo(self, quadro):
        # 1.2.2.1 Modulo
        xModulo = etree.Element(
            etree.QName(NS_IV, "Modulo"))
        # Numero Modulo
        NumeroModulo = etree.SubElement(
            xModulo, etree.QName(NS_IV, "NumeroModulo"))
        NumeroModulo.text = str(self._context.get('nr_modulo', 1))

        if quadro.period_type == 'month':
            # 1.2.2.1.1 Mese
            Mese = etree.SubElement(
                xModulo, etree.QName(NS_IV, "Mese"))
            Mese.text = str(quadro.month)
        else:
            # 1.2.2.1.2 Trimestre
            Trimestre = etree.SubElement(
                xModulo, etree.QName(NS_IV, "Trimestre"))
            Trimestre.text = str(quadro.quarter)
        # Da escludere per liquidazione del gruppo
        if not self.liquidazione_del_gruppo:
            # 1.2.2.1.3 Subfornitura
            if quadro.subcontracting:
                Subfornitura = etree.SubElement(
                    xModulo, etree.QName(NS_IV, "Subfornitura"))
                Subfornitura.text = '1' if quadro.subcontracting \
                    else '0'
            # 1.2.2.1.4 EventiEccezionali
            if quadro.exceptional_events:
                EventiEccezionali = etree.SubElement(
                    xModulo, etree.QName(NS_IV, "EventiEccezionali"))
                EventiEccezionali.text = quadro.exceptional_events
            # 1.2.2.1.5 TotaleOperazioniAttive
            TotaleOperazioniAttive = etree.SubElement(
                xModulo, etree.QName(NS_IV, "TotaleOperazioniAttive"))
            TotaleOperazioniAttive.text = "{:.2f}"\
                .format(quadro.imponibile_operazioni_attive).replace('.', ',')
            # 1.2.2.1.6  TotaleOperazioniPassive
            TotaleOperazioniPassive = etree.SubElement(
                xModulo, etree.QName(NS_IV, "TotaleOperazioniPassive"))
            TotaleOperazioniPassive.text = "{:.2f}"\
                .format(quadro.imponibile_operazioni_passive).replace('.', ',')
        # 1.2.2.1.7  IvaEsigibile
        IvaEsigibile = etree.SubElement(
            xModulo, etree.QName(NS_IV, "IvaEsigibile"))
        IvaEsigibile.text = "{:.2f}".format(quadro.iva_esigibile)\
            .replace('.', ',')
        # 1.2.2.1.8  IvaDetratta
        IvaDetratta = etree.SubElement(
            xModulo, etree.QName(NS_IV, "IvaDetratta"))
        IvaDetratta.text = "{:.2f}".format(quadro.iva_detratta)\
            .replace('.', ',')
        # 1.2.2.1.9  IvaDovuta
        if quadro.iva_dovuta_debito:
            IvaDovuta = etree.SubElement(
                xModulo, etree.QName(NS_IV, "IvaDovuta"))
            IvaDovuta.text = "{:.2f}".format(quadro.iva_dovuta_debito)\
                .replace('.', ',')
        # 1.2.2.1.10  IvaCredito
        if quadro.iva_dovuta_credito:
            IvaCredito = etree.SubElement(
                xModulo, etree.QName(NS_IV, "IvaCredito"))
            IvaCredito.text = "{:.2f}".format(quadro.iva_dovuta_credito)\
                .replace('.', ',')
        # 1.2.2.1.11 DebitoPrecedente
        DebitoPrecedente = etree.SubElement(
            xModulo, etree.QName(NS_IV, "DebitoPrecedente"))
        DebitoPrecedente.text = "{:.2f}".format(
            quadro.debito_periodo_precedente).replace('.', ',')
        # 1.2.2.1.12 CreditoPeriodoPrecedente
        CreditoPeriodoPrecedente = etree.SubElement(
            xModulo, etree.QName(NS_IV, "CreditoPeriodoPrecedente"))
        CreditoPeriodoPrecedente.text = "{:.2f}".format(
            quadro.credito_periodo_precedente).replace('.', ',')
        # 1.2.2.1.13 CreditoAnnoPrecedente
        CreditoAnnoPrecedente = etree.SubElement(
            xModulo, etree.QName(NS_IV, "CreditoAnnoPrecedente"))
        CreditoAnnoPrecedente.text = "{:.2f}".format(
            quadro.credito_anno_precedente).replace('.', ',')
        # 1.2.2.1.14 VersamentiAutoUE
        VersamentiAutoUE = etree.SubElement(
            xModulo, etree.QName(NS_IV, "VersamentiAutoUE"))
        VersamentiAutoUE.text = "{:.2f}".format(
            quadro.versamento_auto_UE).replace('.', ',')
        # 1.2.2.1.15 CreditiImposta
        CreditiImposta = etree.SubElement(
            xModulo, etree.QName(NS_IV, "CreditiImposta"))
        CreditiImposta.text = "{:.2f}".format(
            quadro.crediti_imposta).replace('.', ',')
        # 1.2.2.1.16 InteressiDovuti
        InteressiDovuti = etree.SubElement(
            xModulo, etree.QName(NS_IV, "InteressiDovuti"))
        InteressiDovuti.text = "{:.2f}".format(
            quadro.interessi_dovuti).replace('.', ',')
        # 1.2.2.1.17 Acconto
        Acconto = etree.SubElement(
            xModulo, etree.QName(NS_IV, "Acconto"))
        Acconto.text = "{:.2f}".format(
            quadro.accounto_dovuto).replace('.', ',')
        # 1.2.2.1.18 ImportoDaVersare
        ImportoDaVersare = etree.SubElement(
            xModulo, etree.QName(NS_IV, "ImportoDaVersare"))
        ImportoDaVersare.text = "{:.2f}".format(
            quadro.iva_da_versare).replace('.', ',')
        # 1.2.2.1.19 ImportoACredito
        ImportoACredito = etree.SubElement(
            xModulo, etree.QName(NS_IV, "ImportoACredito"))
        ImportoACredito.text = "{:.2f}".format(
            quadro.iva_a_credito).replace('.', ',')

        return xModulo


class ComunicazioneLiquidazioneVp(models.Model):
    _name = 'comunicazione.liquidazione.vp'
    _description = 'Comunicazione Liquidazione IVA - Quadro VP'

    @api.multi
    @api.depends('iva_esigibile', 'iva_detratta')
    def _compute_VP6_iva_dovuta_credito(self):
        for quadro in self:
            quadro.iva_dovuta_debito = 0
            quadro.iva_dovuta_credito = 0
            if quadro.iva_esigibile >= quadro.iva_detratta:
                quadro.iva_dovuta_debito = quadro.iva_esigibile - \
                    quadro.iva_detratta
            else:
                quadro.iva_dovuta_credito = quadro.iva_detratta - \
                    quadro.iva_esigibile

    @api.multi
    @api.depends('iva_dovuta_debito', 'iva_dovuta_credito',
                 'debito_periodo_precedente', 'credito_periodo_precedente',
                 'credito_anno_precedente', 'versamento_auto_UE',
                 'crediti_imposta', 'interessi_dovuti', 'accounto_dovuto')
    def _compute_VP14_iva_da_versare_credito(self):
        """
        Tot Iva a debito = (VP6, col.1 + VP7 + VP12) 
        Tot Iva a credito = (VP6, col.2 + VP8 + VP9 + VP10 + VP11 + VP13)
        """
        for quadro in self:
            quadro.iva_da_versare = 0
            quadro.iva_a_credito = 0
            debito = quadro.iva_dovuta_debito + quadro.debito_periodo_precedente\
                + quadro.interessi_dovuti
            credito = quadro.iva_dovuta_credito \
                + quadro.credito_periodo_precedente\
                + quadro.credito_anno_precedente \
                + quadro.versamento_auto_UE + quadro.crediti_imposta \
                + quadro.accounto_dovuto
            if debito >= credito:
                quadro.iva_da_versare = debito - credito
            else:
                quadro.iva_a_credito = credito - debito

    comunicazione_id = fields.Many2one('comunicazione.liquidazione',
                                       string='Comunicazione', readonly=True)
    period_type = fields.Selection(
        [('month', 'Monthly'),
         ('quarter', 'Quarterly')],
        string='Period type', default='month')
    month = fields.Integer(string='Month', default=False)
    quarter = fields.Integer(string='Quarter', default=False)
    subcontracting = fields.Boolean(string='Subcontracting')
    exceptional_events = fields.Selection(
        [('1', 'Code 1'), ('9', 'Code 9')], string='Exceptional events')

    imponibile_operazioni_attive = fields.Float(
        string='Totale operazioni attive (al netto dell\'IVA)')
    imponibile_operazioni_passive = fields.Float(
        string='Totale operazioni passive (al netto dell\'IVA)')
    iva_esigibile = fields.Float(string='IVA esigibile')
    iva_detratta = fields.Float(string='IVA detratta')
    iva_dovuta_debito = fields.Float(
        string='IVA dovuta debito',
        compute="_compute_VP6_iva_dovuta_credito", store=True)
    iva_dovuta_credito = fields.Float(
        string='IVA dovuta credito',
        compute="_compute_VP6_iva_dovuta_credito", store=True)
    debito_periodo_precedente = fields.Float(
        string='Debito periodo precedente')
    credito_periodo_precedente = fields.Float(
        string='Credito periodo precedente')
    credito_anno_precedente = fields.Float(string='Credito anno precedente')
    versamento_auto_UE = fields.Float(string='Versamenti auto UE')
    crediti_imposta = fields.Float(string='Crediti d\'imposta')
    interessi_dovuti = fields.Float(
        string='Interessi dovuti per liquidazioni trimestrali')
    accounto_dovuto = fields.Float(string='Acconto dovuto')
    iva_da_versare = fields.Float(
        string='IVA da versare',
        compute="_compute_VP14_iva_da_versare_credito", store=True)
    iva_a_credito = fields.Float(
        string='IVA a credito',
        compute="_compute_VP14_iva_da_versare_credito", store=True)
