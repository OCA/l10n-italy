<html>
<head>
    <style type="text/css">
        ${css}
        .left_with_line {
            text-align:left; vertical-align:text-top; border-top:1px solid #000; padding:5px
        }
        .right_with_line {
            text-align:right; vertical-align:text-top; border-top:1px solid #000; padding:5px
        }
        .left_without_line {
            text-align:left; vertical-align:text-top; padding:5px
        }
        .right_without_line {
            text-align:right; vertical-align:text-top; padding:5px
        }
    </style>
</head>
<body>
    <h2>Fatture Ricevute</h2>
    <% setLang(objects[0].company_id.partner_id.lang or "en_US") %>
    <table style="width:100%;" cellspacing="0">
        <thead>
        <tr>
            <th class="left_without_line">Data registrazione</th>
            <th class="left_without_line">Numero</th>
            <th class="left_without_line">Ragione sociale</th>
            <th class="left_without_line">Numero fattura</th>
            <th class="left_without_line">Data fattura</th>
            <th class="left_without_line">Sezionale</th>
            <th class="right_without_line">Totale fattura</th>
            <th class="right_without_line">Imposta</th>
            <th class="right_without_line">Importo</th>
            <th></th>
        </tr>
        </thead>
        <tbody>
        <% counter = 0 %>
        %for object in objects :
            <% counter += 1 %>
            %for line in tax_lines(object) :
                %if line['index']==0:
                    <tr><td class="left_with_line">
                %else:
                    <tr><td class="left_without_line">
                %endif
                %if line['index']==0:
                    ${ formatLang(object.date,date=True) or '' | entity}
                %endif
                %if line['index']==0:
                    </td><td class="left_with_line">
                %else:
                    </td><td class="left_without_line">
                %endif
                %if line['index']==0:
                    ${ counter | entity}
                %endif
                %if line['index']==0:
                    </td><td class="left_with_line">
                %else:
                    </td><td class="left_without_line">
                %endif
                %if line['index']==0:
                    ${object.partner_id.name or ''| entity}
                %endif
                %if line['index']==0:
                    </td><td class="left_with_line">
                %else:
                    </td><td class="left_without_line">
                %endif
                %if line['index']==0:
                    ${object.name or ''| entity}
                %endif
                %if line['index']==0:
                    </td><td class="left_with_line">
                %else:
                    </td><td class="left_without_line">
                %endif
                %if line['index']==0:
                    ${ formatLang(line['invoice_date'],date=True) or '' | entity}
                %endif
                %if line['index']==0:
                    </td><td class="left_with_line">
                %else:
                    </td><td class="left_without_line">
                %endif
                %if line['index']==0:
                    ${object.journal_id.name or ''| entity}
                %endif
                %if line['index']==0:
                    </td><td class="right_with_line">
                %else:
                    </td><td class="right_without_line">
                %endif
                %if line['index']==0:
                    ${ formatLang(object.amount) | entity}
                %endif
                </td>
                %if line['index']==0:
                    <td class="right_with_line">${ (line['tax_code_name'])  or ''| entity}</td>
                %else:
                    <td class="right_without_line">${ (line['tax_code_name'])  or ''| entity}</td>
                %endif
                %if line['index']==0:
                    <td class="right_with_line">${ formatLang(line['amount'])| entity}</td>
                %else:
                    <td class="right_without_line">${ formatLang(line['amount'])| entity}</td>
                %endif
                </tr>
            %endfor
        %endfor
        </tbody>
    </table>
    <div style="page-break-inside: avoid;">
        <br/>
        <table style="width:100%;  " border="1">
            <tr style="border-style:ridge;border-width:5px">
                <td colspan="3" style="padding:10; ">Periodo di stampa dal <strong>${formatLang(start_date(),date=True)| entity}</strong> al <strong>${formatLang(end_date(),date=True)| entity}</strong></td>
            </tr>
            <tr>
                <td colspan="2" style="vertical-align:text-top;padding:10">
                    <h3>Dettaglio</h3>
                    <table style="width:100%;">
                        <tr>
                            <th style="text-align:left">Descrizione</th>
                            <th style="text-align:right">Importo</th>
                        </tr>
                        <% tax_code_list = tax_codes() %>
                        %for tax_code_tuple in tax_code_list :
                        <tr>
                            <td>${tax_code_tuple[0]|entity}
                            </td><td style="text-align:right">${formatLang(tax_code_tuple[1])|entity}
                            </td>
                        </tr>
                        %endfor
                    </table>
                </td>
                <td style="vertical-align:text-top;padding:10">
                    <h3>Totali</h3>
                    <table style="width:100%;">
                        <tr>
                            <th style="text-align:left">Descrizione</th>
                            <th style="text-align:right">Importo</th>
                        </tr>
                        <% tax_code_totals_list = tax_codes_totals() %>
                        %for tax_code_tuple in tax_code_totals_list :
                        <tr>
                            <td>${tax_code_tuple[0]|entity}
                            </td><td style="text-align:right">${formatLang(tax_code_tuple[1])|entity}
                            </td>
                        </tr>
                        %endfor
                    </table>
                </td>
            </tr>
        </table>
    </div>
</body>
</html>
