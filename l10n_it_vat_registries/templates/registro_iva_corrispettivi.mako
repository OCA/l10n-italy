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
    <h2>Corrispettivi</h2>
    <% setLang(objects[0].company_id.partner_id.lang or "en_US") %>
    <table style="width:100%; font-size: small;" cellspacing="0">
        <thead>
        <tr>
            <th class="left_without_line">Numero</th>
            <th class="left_without_line">Data registrazione</th>
            <th class="left_without_line">Sezionale</th>
            <th class="right_without_line">Importo totale</th>
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
                    ${ counter | entity}
                %endif
                %if line['index']==0:
                    </td><td class="left_with_line">
                %else:
                    </td><td class="left_without_line">
                %endif
                %if line['index']==0: 
                    ${ formatLang(object.date,date=True) or ''| entity}
                %endif
                %if line['index']==0:
                    </td><td class="left_with_line">
                %else:
                    </td><td class="left_without_line">
                %endif
                %if line['index']==0:
                    <div style="page-break-inside: avoid">${object.journal_id.name or ''| entity}</div>
                %endif
                %if line['index']==0:
                    </td><td class="right_with_line">
                %else:
                    </td><td class="right_without_line">
                %endif
                %if line['index']==0:
                    ${ formatLang(invoice_total(object)) | entity}
                %endif
                </td>
                %if line['index']==0:
                    <td class="right_with_line"><div style="page-break-inside: avoid">${ (line['tax_code_name'])  or ''| entity}</div></td>
                %else:
                    <td class="right_without_line"><div style="page-break-inside: avoid">${ (line['tax_code_name'])  or ''| entity}</div></td>
                %endif
                %if line['index']==0:
                    <td class="right_with_line"><div style="page-break-inside: avoid">${ formatLang(line['amount'])| entity}</div></td>
                %else:
                    <td class="right_without_line"><div style="page-break-inside: avoid">${ formatLang(line['amount'])| entity}</div></td>
                %endif
                </tr>
            %endfor
        %endfor
        </tbody>
    </table>
    <div style="page-break-inside: avoid;">
        <br/>
        <% tax_code_list = tax_codes() %>
        <% tax_code_totals_list = tax_codes_totals() %>
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
                        %for tax_code_tuple in tax_code_list :
                            % if not tax_code_tuple[2]:
                                <tr>
                                    <td>${tax_code_tuple[0]|entity}
                                    </td><td style="text-align:right">${formatLang(tax_code_tuple[1])|entity}
                                    </td>
                                </tr>
                            %endif
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
                        %for tax_code_tuple in tax_code_totals_list :
                            % if not tax_code_tuple[2]:
                                <tr>
                                    <td>${tax_code_tuple[0]|entity}
                                    </td><td style="text-align:right">${formatLang(tax_code_tuple[1])|entity}
                                    </td>
                                </tr>
                            %endif
                        %endfor
                    </table>
                </td>
            </tr>
            <tr>
                <td colspan="2" style="vertical-align:text-top;padding:10">
                    <h3>Dettaglio imponibili</h3>
                    <table style="width:100%;">
                        <tr>
                            <th style="text-align:left">Descrizione</th>
                            <th style="text-align:right">Importo</th>
                        </tr>
                        %for tax_code_tuple in tax_code_list :
                            % if tax_code_tuple[2]:
                                <tr>
                                    <td>${tax_code_tuple[0]|entity}
                                    </td><td style="text-align:right">${formatLang(tax_code_tuple[1])|entity}
                                    </td>
                                </tr>
                            %endif
                        %endfor
                    </table>
                </td>
                <td style="vertical-align:text-top;padding:10">
                    <h3>Totali imponibili</h3>
                    <table style="width:100%;">
                        <tr>
                            <th style="text-align:left">Descrizione</th>
                            <th style="text-align:right">Importo</th>
                        </tr>
                        %for tax_code_tuple in tax_code_totals_list :
                            % if tax_code_tuple[2]:
                                <tr>
                                    <td>${tax_code_tuple[0]|entity}
                                    </td><td style="text-align:right">${formatLang(tax_code_tuple[1])|entity}
                                    </td>
                                </tr>
                            %endif
                        %endfor
                    </table>
                </td>
            </tr>
        </table>
    </div>
</body>
</html>
