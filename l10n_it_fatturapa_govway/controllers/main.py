import logging

from odoo.http import Controller, request, route

_logger = logging.getLogger()


class FatturaPAGovWay(Controller):
    # incoming invoices
    @route(["/fatturapa/govway/ricevi_fattura"], type="http", auth="user", website=True)
    def ricevi_fattura(self, *args, **post):
        # headers
        # - GovWay-SDI-FormatoArchivioBase64
        # - GovWay-SDI-FormatoArchivioInvioFattura
        # - GovWay-SDI-FormatoFatturaPA
        # - GovWay-SDI-IdentificativoSdI
        # - GovWay-SDI-MessageId
        # - GovWay-SDI-NomeFile
        # - GovWay-SDI-NomeFileMetadati
        # - GovWay-Transaction-ID
        identificativo_sdi = request.httprequest.headers.get(
            "GovWay-SDI-IdentificativoSdI", ""
        )
        sdi_nomefile = request.httprequest.headers.get("GovWay-SDI-NomeFile", "")
        transaction_id = request.httprequest.headers.get("GovWay-Transaction-ID", "")

        sdi_formatoarchiviobase64 = request.httprequest.headers.get(
            "GovWay-SDI-FormatoArchivioBase64", ""
        )
        sdi_formatoarchiviiinviofattura = request.httprequest.headers.get(
            "GovWay-SDI-FormatoArchivioInvioFattura", ""
        )
        sdi_formartofatturapa = request.httprequest.headers.get(
            "GovWay-SDI-FormatoFatturaPA", ""
        )
        sdi_messageid = request.httprequest.headers.get("GovWay-SDI-MessageId", "")
        sdi_nomefile_metadati = request.httprequest.headers.get(
            "GovWay-SDI-NomeFileMetadati", ""
        )

        _logger.info(
            f"ricevi_fattura(): {identificativo_sdi} {sdi_nomefile} {transaction_id}"
        )
        _logger.debug(f"ricevi_fattura(): args={repr(args)}")
        _logger.debug(f"ricevi_fattura(): post={repr(post)}")

    @route(["/fatturapa/govway/ricevi_ndt"], type="http", auth="user", website=True)
    def ricevi_ndt(self, *args, **post):
        # headers
        # - GovWay-SDI-IdentificativoSdI
        # - GovWay-SDI-NomeFile
        # - GovWay-Transaction-ID
        identificativo_sdi = request.httprequest.headers.get(
            "GovWay-SDI-IdentificativoSdI", ""
        )
        sdi_nomefile = request.httprequest.headers.get("GovWay-SDI-NomeFile", "")
        transaction_id = request.httprequest.headers.get("GovWay-Transaction-ID", "")

        _logger.info(
            f"ricevi_ndt(): {identificativo_sdi} {sdi_nomefile} {transaction_id}"
        )
        _logger.debug(f"ricevi_ndt(): args={repr(args)}")
        _logger.debug(f"ricevi_ndt(): post={repr(post)}")

    # outgoing invoices
    @route(
        ["/fatturapa/govway/ricevi_notifica"],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def ricevi_notifica(self, *args, **post):
        # headers:
        # - GovWay-SDI-IdentificativoSdI
        # - GovWay-SDI-NomeFile
        # - GovWay-Transaction-ID
        identificativo_sdi = request.httprequest.headers.get(
            "GovWay-SDI-IdentificativoSdI", ""
        )
        sdi_nomefile = request.httprequest.headers.get("GovWay-SDI-NomeFile", "")
        transaction_id = request.httprequest.headers.get("GovWay-Transaction-ID", "")

        _logger.info(
            f"ricevi_notifica(): {identificativo_sdi} {sdi_nomefile} {transaction_id}"
        )
        _logger.debug(f"ricevi_notifica(): args={repr(args)}")
        _logger.debug(f"ricevi_notifica(): post={repr(post)}")
        # request.env["sdi.channel"].sdi_channel_model.receive_notification(
        # { sdi_nomefile: post })
