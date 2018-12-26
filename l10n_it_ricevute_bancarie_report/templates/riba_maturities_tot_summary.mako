<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body class="font_10" style="margin:0px;padding:0px;">
    
    <p class="w100 centered" style="font-size: 24px;"><b>${_("RIBA LIST MATURITIES TOTAL SUMMARY")}</b></p>
    
    <table class="w100">
    <%total=0%>
    %for due_date in sorted(group_riba_by_date(objects).keys()):
        <tr style="background-color: #cecece;">
            <td colspan="6">${_("Due date:")} ${due_date}</td>
        </tr>
        <%group_amount=0%>
        %for l in group_riba_by_date(objects)[due_date]:
            %if l.due_date == due_date:
                <%group_amount+=l.amount%>
            %endif
        %endfor
        <tr>
            <td colspan="5" align="right"><b>${_("DUE DATE TOTAL:")}</b></td>
            <td><b>${group_amount}</b></td>
            <%total+=group_amount%>
        </tr>
    %endfor
    <tr>
        <td colspan="4">&nbsp;</td>
        <td><b>${_("TOTAL:")}</b></td>
        <td><b>${total}</b></td>
    </tr>

    </table>
</body>
</html>
