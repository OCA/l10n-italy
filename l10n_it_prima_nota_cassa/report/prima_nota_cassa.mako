<html>
    <head>
        <style type="text/css">
            ${css}
        </style>
    </head>
    <body>
        <h1 class="title">${_("Prime entry")} </h1>

        <table class="basic_table" width="90%">
            <tr>
                <td>${ _("Chart of Account") }</td>
                <td>${ _("Fiscal Year") }</td>
                <td>${ _("Jounal")}</td>
                <td>${ _("Filter By") }</td>
                <td>${ _("Target Moves") }</td>
            </tr>
            <tr>
                
                <td>${ get_account(data) or '' }</td>
                <td>${ get_fiscalyear(data) or '' }</td>
                <td>${ ', '.join([ lt or '' for lt in get_journal(data)]) }</td>
                <td>${ get_filter(data) or '' }</td>
                <td>${ get_target_move(data) }</td>
            </tr>
        </table>

        <br />

        <div id="results">
            % for a in objects:
                <% setLang(company.partner_id.lang) %>
                <table class="list_table"  width="90%">
                    <tr>
                        <th> ${ _('Date') }</th>
                        <th> ${ _('Journal') }</th>
                        <th> ${ _('Partner') }</th>
                        <th> ${ _('Entry') }</th>
                        <th> ${ _('Description') }</th>
                        <th> ${ _('Debit') }</th>
                        <th> ${ _('Credit') }</th>
                        <th> ${ _('Balance') }</th>
                    </tr>

               
                    %for line in lines(a) :
                        <tr style="page-break-inside: avoid; vertical-align:text-top;">
                            <td>${ formatLang(line['ldate'], date=True) or ''|entity }</td>
                            <td>${ line['jname']  or ''|entity }</td>
                            <td>${ line['partner_name']  or ''|entity }</td>
                            <td>${ line['move']  or ''|entity }</td>
                            <td>${ line['lname']  or ''|entity }</td>
                            <td>${ formatLang(line['debit'], digits=get_digits(dp='Account')) |entity}</td>
                            <td>${ formatLang(line['credit'], digits=get_digits(dp='Account')) |entity}</td>
                            <td>${ line['debit'] - line['credit'] |entity}</td>
                        </tr>
                    %endfor
                </table>
            %endfor

        </div>
    </body>
</html>
