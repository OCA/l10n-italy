import logging
from odoo.http import Controller, request, route

_logger = logging.getLogger()

class FatturaPAGovWay(Controller):
    # incoming invoices
    @route(["/fatturapa/govway/ricevi_fattura"], type="http", auth="user", website=True)
    def ricevi_fattura(self):
        # headers
        # - GovWay-SDI-FormatoArchivioBase64
        # - GovWay-SDI-FormatoArchivioInvioFattura
        # - GovWay-SDI-FormatoFatturaPA
        # - GovWay-SDI-IdentificativoSdI
        # - GovWay-SDI-MessageId
        # - GovWay-SDI-NomeFile
        # - GovWay-SDI-NomeFileMetadati
        # - GovWay-Transaction-ID
        identificativo_sdi = request.httprequest.headers.get('GovWay-SDI-IdentificativoSdI', '')
        sdi_nomefile = request.httprequest.headers.get('GovWay-SDI-NomeFile', '')
        transaction_id = request.httprequest.headers.get('GovWay-Transaction-ID', '')

        sdi_formatoarchiviobase64 = request.httprequest.headers.get("GovWay-SDI-FormatoArchivioBase64", "")
        sdi_formatoarchiviiinviofattura = request.httprequest.headers.get("GovWay-SDI-FormatoArchivioInvioFattura", "")
        sdi_formartofatturapa = request.httprequest.headers.get("GovWay-SDI-FormatoFatturaPA", "")
        sdi_messageid= request.httprequest.headers.get("GovWay-SDI-MessageId", "")
        sdi_nomefile_metadati = request.httprequest.headers.get("GovWay-SDI-NomeFileMetadati", "")

        _logger.info("ricevi_fattura(): {} {} {}".format(identificativo_sdi, sdi_nomefile, transaction_id))
        _logger.debug("ricevi_fattura(): args={}".format(repr(args)))
        _logger.debug("ricevi_fattura(): post={}".format(repr(post)))

    @route(["/fatturapa/govway/ricevi_ndt"], type="http", auth="user", website=True)
    def ricevi_ndt(self):
        # headers
        # - GovWay-SDI-IdentificativoSdI
        # - GovWay-SDI-NomeFile
        # - GovWay-Transaction-ID
        identificativo_sdi = request.httprequest.headers.get('GovWay-SDI-IdentificativoSdI', '')
        sdi_nomefile = request.httprequest.headers.get('GovWay-SDI-NomeFile', '')
        transaction_id = request.httprequest.headers.get('GovWay-Transaction-ID', '')

        _logger.info("ricevi_ndt(): {} {} {}".format(identificativo_sdi, sdi_nomefile, transaction_id))
        _logger.debug("ricevi_ndt(): args={}".format(repr(args)))
        _logger.debug("ricevi_ndt(): post={}".format(repr(post)))

    # outgoing invoices
    @route(["/fatturapa/govway/ricevi_notifica"], type="http", auth="user", methods=['POST'], website=True)
    def ricevi_notifica(self, *args, **post):
        # headers:
        # - GovWay-SDI-IdentificativoSdI
        # - GovWay-SDI-NomeFile
        # - GovWay-Transaction-ID
        identificativo_sdi = request.httprequest.headers.get('GovWay-SDI-IdentificativoSdI', '')
        sdi_nomefile = request.httprequest.headers.get('GovWay-SDI-NomeFile', '')
        transaction_id = request.httprequest.headers.get('GovWay-Transaction-ID', '')

        _logger.info("ricevi_notifica(): {} {} {}".format(identificativo_sdi, sdi_nomefile, transaction_id))
        _logger.debug("ricevi_notifica(): args={}".format(repr(args)))
        _logger.debug("ricevi_notifica(): post={}".format(repr(post)))
        #request.env["sdi.channel"].sdi_channel_model.receive_notification({ sdi_nomefile: post })
