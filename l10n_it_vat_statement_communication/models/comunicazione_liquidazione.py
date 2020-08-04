
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from lxml import etree


NS_IV = 'urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp'
NS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'
NS_LOCATION = 'urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp'
NS_MAP = {
    'iv': NS_IV,
    'xsi': NS_XSI,
}
etree.register_namespace("vi", NS_IV)


class ComunicazioneLiquidazione(models.Model):
    _inherit = ['mail.thread']
    _name = 'comunicazione.liquidazione'
    _description = 'VAT statement communication'

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
                _("Communication with identifier {} already exists"
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
    identificativo = fields.Integer(string='Identifier',
                                    default=_get_identificativo)
    name = fields.Char(string='Name', compute="_compute_name")
    year = fields.Integer(string='Year', required=True, size=4)
    last_month = fields.Integer(string='Last month')
    liquidazione_del_gruppo = fields.Boolean(string='Group\'s statement')
    taxpayer_vat = fields.Char(string='Vat', required=True)
    controller_vat = fields.Char(string='Controller TIN')
    taxpayer_fiscalcode = fields.Char(string='Taxpayer Fiscalcode')
    declarant_different = fields.Boolean(
        string='Declarant different from taxpayer', default=True)
    declarant_fiscalcode = fields.Char(string='Declarant Fiscalcode')
    declarant_fiscalcode_company = fields.Char(string='Fiscalcode company')
    codice_carica_id = fields.Many2one('codice.carica', string='Role code')
    declarant_sign = fields.Boolean(string='Declarant sign', default=True)

    delegate_fiscalcode = fields.Char(string='Delegate Fiscalcode')
    delegate_commitment = fields.Selection(
        [('1', 'Communication prepared by taxpayer'),
         ('2', 'Communication prepared by sender')],
        string='Commitment')
    delegate_sign = fields.Boolean(string='Delegate sign')
    date_commitment = fields.Date(string='Date commitment')
    quadri_vp_ids = fields.One2many(
        'comunicazione.liquidazione.vp', 'comunicazione_id',
        string="VP tables")
    iva_da_versare = fields.Float(
        string='VAT to pay', readonly=True)
    iva_a_credito = fields.Float(
        string='Credit VAT', readonly=True)

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
            modulo = self.with_context(
                nr_modulo=nr_modulo)._export_xml_get_dati_modulo(quadro)
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
        if self.taxpayer_fiscalcode and len(self.taxpayer_fiscalcode) == 11\
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
                    _("For group's statement, controller's TIN must be empty"))
            if len(self.taxpayer_fiscalcode) == 16:
                raise ValidationError(
                    _("Group's statement not valid, as fiscal code is 16 "
                      "characters"))
        # CodiceCaricaDichiarante
        if self.declarant_fiscalcode:
            if not self.codice_carica_id:
                raise ValidationError(
                    _("Specify role code of declarant"))
        # CodiceFiscaleSocieta:
        # Obbligatori per codice carica 9
        if self.codice_carica_id and self.codice_carica_id.code == '9':
            if not self.declarant_fiscalcode_company:
                raise ValidationError(
                    _("With this role code, you need to specify fiscal code "
                      "of declarant company"))
        # ImpegnoPresentazione::
        if self.delegate_fiscalcode:
            if not self.delegate_commitment:
                raise ValidationError(
                    _("With intermediary fiscal code, you need to specify "
                      "commitment code"))
            if not self.date_commitment:
                raise ValidationError(
                    _("With intermediary fiscal code, you need to specify "
                      "commitment date"))
        # ImpegnoPresentazione::
        if self.delegate_fiscalcode and not self.delegate_sign:
            raise ValidationError(
                _("With delegate in commitment section, you need to check "
                  "'delegate sign'"))
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
        code = self.company_id.vsc_supply_code
        x1_1_1_CodiceFornitura.text = code
        # Codice Fiscale Dichiarante
        if self.declarant_fiscalcode:
            x1_1_2_CodiceFiscaleDichiarante = etree.SubElement(
                x1_1_Intestazione, etree.QName(NS_IV,
                                               "CodiceFiscaleDichiarante"))
            x1_1_2_CodiceFiscaleDichiarante.text = str(
                self.declarant_fiscalcode)
        # Codice Carica
        if self.codice_carica_id:
            x1_1_3_CodiceCarica = etree.SubElement(
                x1_1_Intestazione, etree.QName(NS_IV, "CodiceCarica"))
            x1_1_3_CodiceCarica.text = str(self.codice_carica_id.code)
        return x1_1_Intestazione

    def _export_xml_get_frontespizio(self):
        x1_2_1_Frontespizio = etree.Element(etree.QName(NS_IV, "Frontespizio"))
        # Codice Fiscale
        x1_2_1_1_CodiceFiscale = etree.SubElement(
            x1_2_1_Frontespizio, etree.QName(NS_IV, "CodiceFiscale"))
        x1_2_1_1_CodiceFiscale.text = str(self.taxpayer_fiscalcode) \
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
            x1_2_1_5_UltimoMese.text = str(self.last_month)
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
                self.declarant_fiscalcode_company
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
                x1_2_1_Frontespizio, etree.QName(
                    NS_IV, "ImpegnoPresentazione"))
            x1_2_1_12_ImpegnoPresentazione.text = self.delegate_commitment
        # DataImpegno
        if self.date_commitment:
            x1_2_1_13_DataImpegno = etree.SubElement(
                x1_2_1_Frontespizio, etree.QName(NS_IV, "DataImpegno"))
            x1_2_1_13_DataImpegno.text = self.date_commitment.strftime(
                '%d%m%Y')
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
        if quadro.metodo_calcolo_acconto:
            Metodo = etree.SubElement(
                xModulo, etree.QName(NS_IV, "Metodo"))
            Metodo.text = quadro.metodo_calcolo_acconto
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
    _description = 'VAT statement communication - VP table'

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
            if quadro.period_type == 'quarter' and quadro.quarter == 5:
                # VP14 non deve essere compilato dai contribuenti trimestrali di cui
                # all’art. 7 del d.P.R. 14 ottobre 1999, n.542,
                # relativamente al 4° trimestre
                # I contribuenti che hanno optato per la liquidazione trimestrale ai
                # sensi dell’art. 7 del D.P.R. n. 542/99 devono indicare “5” per il
                # quarto trimestre
                continue
            debito = (
                quadro.iva_dovuta_debito + quadro.debito_periodo_precedente +
                quadro.interessi_dovuti
            )
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
                                       string='Communication', readonly=True)
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
        string='Profitable operations total (without VAT)')
    imponibile_operazioni_passive = fields.Float(
        string='Unprofitable operations total (without VAT)')
    iva_esigibile = fields.Float(string='Due VAT')
    iva_detratta = fields.Float(string='Deducted VAT')
    iva_dovuta_debito = fields.Float(
        string='Debit VAT',
        compute="_compute_VP6_iva_dovuta_credito", store=True)
    iva_dovuta_credito = fields.Float(
        string='Credit due VAT',
        compute="_compute_VP6_iva_dovuta_credito", store=True)
    debito_periodo_precedente = fields.Float(
        string='Previous period debit')
    credito_periodo_precedente = fields.Float(
        string='Previous period credit')
    credito_anno_precedente = fields.Float(string='Previous year credit')
    versamento_auto_UE = fields.Float(string='Auto UE payment')
    crediti_imposta = fields.Float(string='Tax credits')
    interessi_dovuti = fields.Float(
        string='Due interests for quarterly statements')
    accounto_dovuto = fields.Float(string='Down payment due')
    metodo_calcolo_acconto = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string="Down payment computation method")
    iva_da_versare = fields.Float(
        string='VAT to pay',
        compute="_compute_VP14_iva_da_versare_credito", store=True)
    iva_a_credito = fields.Float(
        string='Credit VAT',
        compute="_compute_VP14_iva_da_versare_credito", store=True)
    liquidazioni_ids = fields.Many2many(
        'account.vat.period.end.statement',
        'comunicazione_iva_liquidazioni_rel',
        'comunicazione_id',
        'liquidazione_id',
        string='VAT statements')

    def _reset_values(self):
        for quadro in self:
            quadro.imponibile_operazioni_attive = 0
            quadro.imponibile_operazioni_passive = 0
            quadro.iva_esigibile = 0
            quadro.iva_detratta = 0
            quadro.debito_periodo_precedente = 0
            quadro.credito_periodo_precedente = 0
            quadro.credito_anno_precedente = 0
            quadro.versamento_auto_UE = 0
            quadro.crediti_imposta = 0
            quadro.interessi_dovuti = 0
            quadro.accounto_dovuto = 0

    def _get_tax_context(self, period):
        return {
            'from_date': period.date_start,
            'to_date': period.date_end,
        }

    def _compute_imponibile_operazioni_attive(self, liq, period):
        self.ensure_one()
        debit_taxes = self.env['account.tax']
        for debit in liq.debit_vat_account_line_ids:
            debit_taxes |= debit.tax_id
        for debit_tax in debit_taxes:
            if debit_tax.vsc_exclude_operation:
                continue
            tax = debit_taxes.with_context(
                self._get_tax_context(period)).browse(debit_tax.id)
            self.imponibile_operazioni_attive += (
                tax.base_balance)

    def _compute_imponibile_operazioni_passive(self, liq, period):
        self.ensure_one()
        credit_taxes = self.env['account.tax']
        for credit in liq.credit_vat_account_line_ids:
            credit_taxes |= credit.tax_id
        for credit_tax in credit_taxes:
            if credit_tax.vsc_exclude_operation:
                continue
            tax = credit_taxes.with_context(
                self._get_tax_context(period)).browse(credit_tax.id)
            self.imponibile_operazioni_passive -= (
                tax.base_balance)

    @api.multi
    @api.onchange('liquidazioni_ids')
    def compute_from_liquidazioni(self):

        for quadro in self:
            # Reset valori
            quadro._reset_values()

            for liq in quadro.liquidazioni_ids:

                for period in liq.date_range_ids:
                    quadro._compute_imponibile_operazioni_attive(liq, period)
                    quadro._compute_imponibile_operazioni_passive(liq, period)

                # Iva esigibile
                for vat_amount in liq.debit_vat_account_line_ids:
                    if vat_amount.tax_id.vsc_exclude_vat:
                        continue
                    quadro.iva_esigibile += vat_amount.amount
                # Iva detratta
                for vat_amount in liq.credit_vat_account_line_ids:
                    if vat_amount.tax_id.vsc_exclude_vat:
                        continue
                    quadro.iva_detratta += vat_amount.amount
                # credito/debito periodo precedente
                quadro.debito_periodo_precedente =\
                    liq.previous_debit_vat_amount
                if liq.previous_year_credit:
                    quadro.credito_anno_precedente =\
                        liq.previous_credit_vat_amount
                else:
                    quadro.credito_periodo_precedente =\
                        liq.previous_credit_vat_amount
                quadro.accounto_dovuto = liq.advance_amount
                if liq.interests_debit_vat_account_id:
                    quadro.interessi_dovuti += liq.interests_debit_vat_amount
                # Versamenti auto UE (NON GESTITO)
                # Crediti d’imposta (NON GESTITO)
                # Da altri crediti e debiti calcolo:
                # 1 - Decremento iva esigibile con righe positive
                # 2 - Decremento iva detratta con righe negative
                for line in liq.generic_vat_account_line_ids:
                    if line.amount > 0:
                        quadro.iva_esigibile -= line.amount
                    else:
                        quadro.iva_detratta += line.amount
