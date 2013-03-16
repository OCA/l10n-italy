<html>
<head>
    <style type="text/css">
        ${css}
table.tax_codes {
	border-width: 1px;
	border-spacing: 2px;
	border-style: outset;
	border-color: gray;
	border-collapse: collapse;
	background-color: white;
    margin-right:auto;
    margin-left:auto;
}
table.tax_codes th {
	border-width: 1px;
	padding: 4px;
	border-style: inset;
	border-color: gray;
	background-color: white;
}
table.tax_codes td {
	border-width: 1px;
	padding: 4px;
	border-style: inset;
	border-color: gray;
	background-color: white;
}
tr {
    page-break-inside: avoid;
}
    </style>
</head>
<body>
<% setLang(company.partner_id.lang) %>
% for statement in objects:
<h1 style="text-align: center;">${_("VAT Statement Summary")} </h1>
<h2 style="text-align: center;">${_("Date")}: ${formatLang(statement.date, date=True)|entity} </h2>

<table width="100%"  class="tax_codes">
    <tr >
        <th  colspan="3">${ _('Sales') }</th>
    </tr>
    <tr >
        <th >${ _('Tax Code') }</th>
        <th >${ _('Base') }</th>
        <th >${ _('VAT') }</th>
    </tr>
    <% debit_total_base = 0.0 %>
    <% debit_total_vat = 0.0 %>
    <% totals_by_tax_code = {} %>
    %for period in statement.period_ids:
        <tr >
            <td style="text-align:left" colspan="3"><strong>${ _('Period') + ' ' + period.name}</strong></td>
        </tr>
        <% debit_amounts = tax_codes_amounts(period.id, [l.tax_code_id.id for l in statement.debit_vat_account_line_ids]) %>
        %for tax_code in debit_amounts :
            <% if tax_code not in totals_by_tax_code: totals_by_tax_code[tax_code]={'base':0.0,'vat':0.0} %>
            <% totals_by_tax_code[tax_code]['base'] += debit_amounts[tax_code]['base'] %>
            <% totals_by_tax_code[tax_code]['vat'] += debit_amounts[tax_code]['vat'] %>
            <tr >
                <td style="text-align:left">${ tax_code|entity }</td>
                <td style="text-align:right">${ formatLang(debit_amounts[tax_code]['base'])|entity }</td>
                <td style="text-align:right">${ formatLang(debit_amounts[tax_code]['vat'])|entity }</td>
                <% debit_total_base += debit_amounts[tax_code]['base'] %>
                <% debit_total_vat += debit_amounts[tax_code]['vat'] %>
            </tr>
        %endfor
    %endfor
    <tr >
        <td style="text-align:left" colspan="3"><strong>${ _('Totals')}</strong></td>
    </tr>
    %for tax_code in totals_by_tax_code:
        <tr >
            <td style="text-align:left">${ tax_code|entity }</td>
            <td style="text-align:right">${ formatLang(totals_by_tax_code[tax_code]['base'])|entity }</td>
            <td style="text-align:right">${ formatLang(totals_by_tax_code[tax_code]['vat'])|entity }</td>
        </tr>
    %endfor
    <tr >
        <td style="text-align:left"></td>
        <td style="text-align:right"><strong>${ formatLang(debit_total_base)|entity }</strong></td>
        <td style="text-align:right"><strong>${ formatLang(debit_total_vat)|entity }</strong></td>
    </tr>
</table>
<br/><br/>
<table width="100%"  class="tax_codes">
    <tr >
        <th  colspan="3">${ _('Purchases') }</th>
    </tr>
    <tr >
        <th >${ _('Tax Code') }</th>
        <th >${ _('Base') }</th>
        <th >${ _('VAT') }</th>
    </tr>
    <% credit_total_base = 0.0 %>
    <% credit_total_vat = 0.0 %>
    <% totals_by_tax_code = {} %>
    %for period in statement.period_ids:
        <tr >
            <td style="text-align:left" colspan="3"><strong>${ _('Period') + ' ' + period.name}</strong></td>
        </tr>
        <% credit_amounts = tax_codes_amounts(period.id, [l.tax_code_id.id for l in statement.credit_vat_account_line_ids]) %>
        %for tax_code in credit_amounts :
            <% if tax_code not in totals_by_tax_code: totals_by_tax_code[tax_code]={'base':0.0,'vat':0.0} %>
            <% totals_by_tax_code[tax_code]['base'] += credit_amounts[tax_code]['base'] %>
            <% totals_by_tax_code[tax_code]['vat'] += credit_amounts[tax_code]['vat'] %>
            <tr >
                <td style="text-align:left">${ tax_code|entity }</td>
                <td style="text-align:right">${ formatLang(credit_amounts[tax_code]['base'])|entity }</td>
                <td style="text-align:right">${ formatLang(credit_amounts[tax_code]['vat'])|entity }</td>
                <% credit_total_base += credit_amounts[tax_code]['base'] %>
                <% credit_total_vat += credit_amounts[tax_code]['vat'] %>
            </tr>
        %endfor
    %endfor
    <tr >
        <td style="text-align:left" colspan="3"><strong>${ _('Totals')}</strong></td>
    </tr>
    %for tax_code in totals_by_tax_code:
        <tr >
            <td style="text-align:left">${ tax_code|entity }</td>
            <td style="text-align:right">${ formatLang(totals_by_tax_code[tax_code]['base'])|entity }</td>
            <td style="text-align:right">${ formatLang(totals_by_tax_code[tax_code]['vat'])|entity }</td>
        </tr>
    %endfor
    <tr >
        <td style="text-align:left"></td>
        <td style="text-align:right"><strong>${ formatLang(credit_total_base)|entity }</strong></td>
        <td style="text-align:right"><strong>${ formatLang(credit_total_vat)|entity }</strong></td>
    </tr>
</table>
<br/><br/>
<table class="tax_codes"  width="100%" >
    <tr >
        <th  colspan="3">${_("Summary")}</th>
    </tr>
    <tr>
        <th></th>
        <th> ${ _('Debit') }</th>
        <th> ${ _('Credit') }</th>
    </tr>
    %for debit_line in statement.debit_vat_account_line_ids :
        <tr >
            <td>${ debit_line.account_id.name|entity }</td>
            <td>${ formatLang(debit_line.amount)|entity }</td>
            <td></td>
        </tr>
    %endfor
    <!--
    <tr >
        <td>${_("Total")}</td>
        <td>${ statement.payable_vat_amount|entity }</td>
    </tr>
    -->
    %for credit_line in statement.credit_vat_account_line_ids :
        <tr >
            <td>${ credit_line.account_id.name|entity }</td>
            <td></td>
            <td>${ formatLang(credit_line.amount)|entity }</td>
        </tr>
    %endfor
    <!--
    <tr >
        <td>${_("Total")}</td>
        <td>${ statement.deductible_vat_amount|entity }</td>
    </tr>
    -->
    <tr >
        <td>${_("Previous Credits VAT")}</td>
        <td></td>
        <td>${ formatLang(statement.previous_credit_vat_amount)|entity }</td>
    </tr>
    <tr >
        <td>${_("Previous Debits VAT")}</td>
        <td>${ formatLang(statement.previous_debit_vat_amount)|entity }</td>
        <td></td>
    </tr>
    %for generic_line in statement.generic_vat_account_line_ids :
        <tr >
            <td>${ generic_line.account_id.name|entity }</td>
            <td>${ generic_line.amount < 0 and formatLang(generic_line.amount) or ''|entity }</td>
            <td>${ generic_line.amount > 0 and formatLang(generic_line.amount) or ''|entity }</td>
        </tr>
    %endfor
    <tr >
        <td><strong>${_("Amount to pay")}</strong></td>
        <td colspan="2" style="text-align:center"><strong>${ formatLang(statement.authority_vat_amount)|entity }</strong></td>
    </tr>
</table>
%endfor
</body>
</html>
