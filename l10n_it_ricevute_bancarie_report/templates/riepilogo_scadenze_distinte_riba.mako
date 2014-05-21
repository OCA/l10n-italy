<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body class="font_10" style="margin:0px;padding:0px;">
    
    <p class="w100 centered" style="font-size: 24px;"><b>RIEPILOGO DISTINTE RICEVUTE BANCARIE ${datetime.today().strftime("%d/%m/%y")}</b></p>
    
    <table class="w100">
    %for due_date,lines in group_riba_data(objects).items():
        <tr style="background-color: #cecece;">
            <td colspan="3">${due_date}</td>
        </tr>
        <tr>
            <td>DISTINTA</td>
            <td>NR RIGA</td>
            <td>CLIENTE</td>
            <td>RIF</td>
            <td>IMPORTO</td>
            <td>SCADENZA</td>
        </tr>
        <%importo=0%>
        %for l in lines:
            %if l.due_date == due_date:
                <%importo+=l.amount%>
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
            <td>&nbsp;</td>
            <td><b>TOTALE:</b></td>
            <td><b>${importo}</b></td>
        </tr>
    %endfor

    </table>
</body>
</html>
