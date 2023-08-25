odoo.define("l10n_it_delivery_note.DeliveryNotePortalSidebar", function (require) {
    "use strict";

    const dom = require("web.dom");
    var publicWidget = require("web.public.widget");
    var PortalSidebar = require("portal.PortalSidebar");
    var utils = require("web.utils");

    publicWidget.registry.DeliveryNotePortalSidebar = PortalSidebar.extend({
        selector: ".o_portal_dn_sidebar",
        events: {
            "click .o_portal_dn_print": "_onPrintDN",
        },

        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);

            var $dnHtml = this.$el.find("iframe#dn_html");
            var updateIframeSize = this._updateIframeSize.bind(this, $dnHtml);

            $(window).on("resize", updateIframeSize);

            var iframeDoc =
                $dnHtml[0].contentDocument || $dnHtml[0].contentWindow.document;
            if (iframeDoc.readyState === "complete") {
                updateIframeSize();
            } else {
                $dnHtml.on("load", updateIframeSize);
            }

            return def;
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * Called when the iframe is loaded or the window is resized on customer portal.
         * The goal is to expand the iframe height to display the full report without scrollbar.
         *
         * @private
         * @param {Object} $el: the iframe
         */
        _updateIframeSize: function ($el) {
            var $wrapwrap = $el.contents().find("div#wrapwrap");
            // Set it to 0 first to handle the case where scrollHeight is too big for its content.
            $el.height(0);
            $el.height($wrapwrap[0].scrollHeight);

            // Scroll to the right place after iframe resize
            if (!utils.isValidAnchor(window.location.hash)) {
                return;
            }
            var $target = $(window.location.hash);
            if (!$target.length) {
                return;
            }
            dom.scrollTo($target[0], {duration: 0});
        },
        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onPrintDN: function (ev) {
            ev.preventDefault();
            var href = $(ev.currentTarget).attr("href");
            this._printIframeContent(href);
        },
    });
});
