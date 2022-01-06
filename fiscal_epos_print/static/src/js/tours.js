odoo.define('fiscal_epos_print.tour.close_and_report', function (require) {
    "use strict";

    var Tour = require("web_tour.tour");

    var steps = [
        {
            content: "click epos button",
            trigger: ".header-button.epos-button",
        },
        {
            content: "click close and report button",
            trigger: ".button.epos_close_and_report",
        },
        {
            content: "confirm popup",
            trigger: ".button.confirm",
        },
    ];

    Tour.register('close_and_report',
        {
            test: true,
            url: '/pos/web',
        },
        steps,
    );
});
