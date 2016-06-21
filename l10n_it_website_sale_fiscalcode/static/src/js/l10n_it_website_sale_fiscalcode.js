$(document).ready(function () {
$('.oe_website_sale').each(function () {
    var oe_website_sale = this;
    var company_name = $(oe_website_sale).find("#company_name");
    var label_your_name = $(oe_website_sale).find("#label_your_name");
    var fiscalcode = $(oe_website_sale).find("#fiscalcode");
    var vat_number = $(oe_website_sale).find("#vat_number");
    $(oe_website_sale).on("change", '#partner_type', function (event) {
        var partner_type = $(event.target);
        if (partner_type.val() == "individual"){
            vat_number.hide();
            fiscalcode.show();
        }
        else if (partner_type.val() == "company" ||
            partner_type.val() == "association"){
            vat_number.show();
            fiscalcode.show();
        }
    });
    $('#partner_type').change();
    });
});
