<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
<h1 class="title">${_("Prime entry")} </h1>
## ${ ipdb(data) }

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
        ${ company.partner_id.lang }
        <% setLang(company.partner_id.lang) %>
        <table class="list_table"  width="90%">
            <tr>
                <th> ${ _('Date') }</th>
                <th> ${ _('JRNL') }</th>
                <th> ${ _('Partner') }</th>
                <th> ${ _('Ref') }</th>
                <th> ${ _('Move') }</th>
                <th> ${ _('Entry Label') }</th>
                <th> ${ _('Debit') }</th>
                <th> ${ _('Credit') }</th>
                <th> ${ _('Balance') }</th>
            </tr>

       
            %for line in lines(a) :
                <tr>
                    <td>${ formatLang(line['ldate'], date=True)|entity }</td>
                    <td>${ line['jname'] }</td>
                    <td>${ line['partner_name'] }</td>
                    <td>${ line['lref'] }</td>
                    <td>${ line['move'] }</td>
                    <td>${ line['lname'] }</td>
                    <td>${ formatLang(line['debit'], digits=get_digits(dp='Account')) }</td>
                    <td>${ formatLang(line['credit'], digits=get_digits(dp='Account')) }</td>
                    <td>${ line['debit'] - line['credit'] }</td>
                </tr>
            %endfor
        </table>
    %endfor
    ## ${ ipdb(data) }
</div>
</body>
</html>
