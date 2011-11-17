<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    %for ord in objects:
    <% setLang(ord.company_id.partner_id.lang) %>
    <table class="dest_address">
    <tr>
    <td>
    <p align="right">
    ${_("Distinta incassi Ricevute bancarie ")}${_("Num: ")} ${ord.reference or ''}</br> 
    ${_("Presentata il: ")}${formatLang(ord.date_created, date=True)}</br>
    ${_("a: ")}&#160;<b>${ord.mode.bank_id.bank.name or ''}</b></br>
    </p>
    </td>
    </tr>
    </table>
    <table class="basic_collapse" width="100%">
        <tr class="basic_top"><th>${_("N.Eff. Cliente/Debitore")}</th><th>${_("Domicilio")}</th><th>${_("Num e Data Doc")}</th><th>${_("Scadenza")}</th><th>${_("Valuta")}</th><th>${_("Importo")}</th></tr>
        <% abi_text = '' %>
	<% cab_text = '' %>
        %for line in ord.line_ids:
           %if line.bank_id.iban is None:
                <% 
                abi_text = 'ABI'
                cab_text = 'CAB'
                %>
           %else:
		<% 
		abi_text = 'ABI ' + line.bank_id.iban[5:10]
		cab_text = 'CAB ' + line.bank_id.iban[10:15]
		%>
           %endif
        <tr class="basic_top"><td>${line.name or ''}&#160;&#160; ${line.partner_id.name or ''}</td><td>${abi_text or ''}&#160;&#160;${cab_text or ''}</td><td>${line.move_line_id.move_id.name or ''}&#160;&#160;${formatLang(line.move_line_id.move_id.date, date=True) or ''}</td><td>${formatLang(line.date, date=True) or ''}</td><td>${line.company_id.currency_id.name or ''}</td><td style="text-align:right">${formatLang(line.amount_currency) or ''}</td></tr>

        %endfor
        <tr class="basic_bottom"><td colspan="5"></td></tr>

        <tbody>
        <tr><td colspan="5">${_("Distinta incassi Ricevute bancarie")}&#160;&#160;${_("Num: ")} ${ord.reference or ''}</td><td style="text-align:right;">${formatLang(ord.total or '')}</td></tr>
      </tbody>
    </table>
    <p style="page-break-after:always"></p>
    %endfor
</body>
</html>
