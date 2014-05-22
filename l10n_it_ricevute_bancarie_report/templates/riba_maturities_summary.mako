<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body class="font_10" style="margin:0px;padding:0px;">
    
    <p class="w100 centered" style="font-size: 24px;"><b>RIBA LIST MATURITIES SUMMARY</b></p>
    
    <table class="w100">
    <%total=0%>
    %for due_date,lines in group_riba_by_date(objects).items():
        <tr style="background-color: #cecece;">
            <td colspan="6">Due date: ${due_date}</td>
        </tr>
        <tr>
            <td>LIST</td>
            <td>ROW nr</td>
            <td>CUSTOMER</td>
            <td>RIF</td>
            <td>AMOUNT</td>
            <td>DUE DATE</td>
        </tr>
        <%group_amount=0%>
        %for l in lines:
            %if l.due_date == due_date:
                <%group_amount+=l.amount%>
                <tr>
                    <td>${l.distinta_id.name or ''}</td>
                    <td>${l.sequence or ''}</td>
                    <td>${l.partner_id.name or ''}</td>
                    <td>${l.invoice_number or ''}</td>
                    <td>${l.amount or ''}</td>
                    <td>${l.due_date or ''}</td>
                </tr>
            %endif
        %endfor
        <tr>
            <td colspan="5" align="right"><b>DUE DATE TOTAL:</b></td>
            <td><b>${group_amount}</b></td>
            <%total+=group_amount%>
        </tr>
    %endfor
    <tr>
        <td colspan="4">&nbsp;</td>
        <td><b>TOTAL:</b></td>
        <td><b>${total}</b></td>
    </tr>

    </table>
</body>
</html>
