<html>
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
    <style type="text/css">
    ${css}
    
    .page_block {
        page-break-after: always;
        width: 100%;
        }
    .page_table {
        width: 100%;
        }
    .p_row {
        page-break-inside: avoid; 
        vertical-align:text-top;
        height: 21px;
        }
    .p_cell {
        overflow: hidden;
        padding: 1px 5px;
        }
    .p_text {
        color: black;
        font-size: 9px;
        font-family: "Courier New", Courier, monospace;
        }
    .p_cell_debit, .p_cell_credit {
        text-align: right;
        }
        
    .p_row_head {
        border: 1px solid black;
        border-width: 1px 0px;
        }
    .p_cell_head {
        font-weight: bold;
        padding: 3px 5px;
        }
        
    .p_row_page {
        font-weight: bold;
        }
    .p_cell_test {
        padding: 5px 5px;
        }
    .p_cell_page {
        padding: 5px 5px;
        text-align: right;
        }

    .p_row_total {
        font-weight: bold;
        border: 1px solid gray;
        }
    .p_row_total_up {
        border-width: 0px 0px 1px 0px;
        }
    .p_row_total_down {
        border-width: 1px 0px 0px 0px;
        }
    .p_cell_progressive {
        padding: 3px 5px;
        text-align: right;
        }
        
    /* COLUMNS WIDTH 
    .p_cell_progr_row { width: 15px;}
    .p_cell_date { width: 45px;}
    .p_cell_ref { width: 70px;}
    .p_cell_move_id_name { width: 70px;}
    .p_cell_account_id_code { width: 50px;}
    .p_cell_account_id_name { width: 200px;}
    .p_cell_name { width: 250px;}
    .p_cell_debit { width: 70px;}
    .p_cell_credit { width: 70px;}
    */
    </style>
</head>

<body>
    <%
        flag_print_final = data["print_final"]
        fiscalyear_id = data["form"]["fiscalyear"]
        date_from = data["form"]["date_move_line_from"]
        date_to = data["form"]["date_move_line_to"]
    %>
    <%
        print_info = get_print_info(fiscalyear_id)
        result_wizard = set_wizard_params(data["form"])
        result_rows = get_movements()
    %>
    <%
        page_rows = 25
        
        num_rows = len(result_rows)
        num_row = 0
        new_page = True
        
        progr_page = print_info['start_page']
        progr_row = print_info['start_row']
    %>
    <%
        debit_tot = print_info['start_debit']
        credit_tot = print_info['start_credit']
    %>        
    <% result_rows and result_rows[0] and result_rows[0].company_id and result_rows[0].company_id.partner_id and result_rows[0].company_id and result_rows[0].company_id.partner_id.lang and setLang(result_rows[0].company_id and result_rows[0].company_id.partner_id.lang) %>

    %for line in result_rows :
        <% num_row = num_row + 1 %>
        <% progr_row = progr_row + 1 %>
        % if new_page == True:
            <% 
            new_page = False 
            progr_page = progr_page + 1
            %>
            <div class="page_block">
            <table class="header" style="border-bottom: 0px solid black; width: 100%">
                <tr>
                    <td style="text-align:center;"><span style="font-weight: bold; font-size: 14px;">${_("ACCOUNT JOURNAL")}</span></td>
                </tr>
            </table>

            <table class="page_table">
            <tr class="p_row p_row_page">
                <td colspan="7" class="p_cell p_cell_test">
                    % if flag_print_final == False:
                    <span class="p_text">${ _("TEST PRINTING") }&nbsp;${ _("From date") }&nbsp;${ formatLang(date_from, date=True) or ''|entity }&nbsp;${ _("to date") }&nbsp;${ formatLang(date_to, date=True) or ''|entity }</span>
                    % endif
                </td>
                <td colspan="2" class="p_cell p_cell_page"><span class="p_text p_page">${ _("Page:") }&nbsp;&nbsp;${progr_page} / ${print_info['year_name']}</span></td>
            </tr>
            
            <tr class="p_row p_row_head">
                <td class="p_cell p_cell_head"><span class="p_text">${ _("Row") }</span></td>
                <td class="p_cell p_cell_head"><span class="p_text">${ _("Date") }</span></td>
                <td class="p_cell p_cell_head"><span class="p_text">${ _("Ref") }</span></td>
                <td class="p_cell p_cell_head"><span class="p_text">${ _("Account move") }</span></td>
                <td class="p_cell p_cell_head"><span class="p_text">${ _("Account code") }</span></td>
                <td class="p_cell p_cell_head"><span class="p_text">${ _("Account name") }</span></td>
                <td class="p_cell p_cell_head"><span class="p_text">${ _("Name") }</span></td>
                <td class="p_cell p_cell_head p_cell_debit"><span class="p_text">${ _("Debit") }</span></td>
                <td class="p_cell p_cell_head p_cell_credit"><span class="p_text">${ _("Credit") }</span></td>
            </tr>

            <tr class="p_row p_row_total p_row_total_up">
                <td colspan="6"></td>
                <td class="p_cell p_cell_progressive"><span class="p_text">${ _("Progressives =>") }</span></td>
                <td class="p_cell p_cell_debit"><span class="p_text p_debit">${ formatLang(debit_tot, digits=get_digits(dp='Account')) |entity }</span></td>
                <td class="p_cell p_cell_credit"><span class="p_text p_credit">${ formatLang(credit_tot, digits=get_digits(dp='Account')) |entity }</span></td>
            </tr>
        % endif
        <tr class="p_row">
            <td class="p_cell p_cell_progr_row"><span class="p_text p_progr_row">${progr_row}</span></td>
            <td class="p_cell p_cell_date"><span class="p_text p_date">${ formatLang(line.date, date=True) or ''|entity }</span></td>
            <td class="p_cell p_cell_ref"><span class="p_text p_ref">${ line.ref or ''|entity }</span></td>
            <td class="p_cell p_cell_move_id_name"><span class="p_text p_move_id_name">${ line.move_id.name or ''|entity }</span></td>
            <td class="p_cell p_cell_account_id_code"><span class="p_text p_account_id_code">${ line.account_id.code or ''|entity }</span></td>
            <td class="p_cell p_cell_account_id_name"><span class="p_text p_account_id_name">${ line.account_id.name or ''|entity }</span></td>
            <td class="p_cell p_cell_name"><span class="p_text p_name">${ line.name or ''|entity }</span></td>
            <td class="p_cell p_cell_debit"><span class="p_text p_debit">${ formatLang(line.debit, digits=get_digits(dp='Account')) |entity }</span></td>
            <td class="p_cell p_cell_credit"><span class="p_text p_credit">${ formatLang(line.credit, digits=get_digits(dp='Account')) |entity }</span></td>
        </tr>
        <%
        debit_tot = debit_tot + line.debit
        credit_tot = credit_tot + line.credit
        %>        
        % if (num_row % page_rows) == 0 or num_row == num_rows :
            <% 
            new_page = True 
            %>
            <tr class="p_row p_row_total p_row_total_down">
            <td colspan="6"></td>
            <td class="p_cell p_cell_progressive"><span class="p_text">${ _("Progressives =>") }</span></td>
            <td class="p_cell p_cell_debit"><span class="p_text p_debit">${ formatLang(debit_tot, digits=get_digits(dp='Account')) |entity }</span></td>
            <td class="p_cell p_cell_credit"><span class="p_text p_credit">${ formatLang(credit_tot, digits=get_digits(dp='Account')) |entity }</span></td>
            </tr>
            </table>
            </div>
        % endif
    %endfor

    <%
        if flag_print_final == True:
            print_info = set_print_info(fiscalyear_id, date_to, progr_row, progr_page, debit_tot, credit_tot)
    %>
    
</body>
</html>

