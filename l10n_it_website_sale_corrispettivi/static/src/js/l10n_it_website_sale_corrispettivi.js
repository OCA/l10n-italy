$(document).ready(function () {
$('.oe_website_sale').each(function () {
    var oe_website_sale = this;
    var select_invoice_or_receipt = $(oe_website_sale).find("#select_invoice_or_receipt");
    select_invoice_or_receipt.prop("disabled", true);
    $(oe_website_sale).on("change", '#partner_type', function (event) {
        var partner_type = $(event.target);
        if (partner_type.val() == "individual"){
            select_invoice_or_receipt.val("receipt")
        }
        else {
            select_invoice_or_receipt.val("invoice")
        }
    });
    $('#partner_type').change();
    });
});
