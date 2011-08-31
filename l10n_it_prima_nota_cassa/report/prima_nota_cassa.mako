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
##        ${ company.partner_id.lang }
        <% setLang(company.partner_id.lang) %>
        <table id="primanota_table">
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

            % if data['form']['initial_balance']:
            <tr style="page-break-inside: avoid; vertical-align:text-top;">
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>${ _('Initial Balance') }</td>
                <td></td>
                <td></td>
                <td class="right">${ formatLang(compute_totals(a)['initial_balance'], digits=get_digits(dp='Account')) | entity}</td>
            </tr>
            % endif
            
            % for line in lines(a) :
                <tr style="page-break-inside: avoid; vertical-align:text-top;">
                    <td>${ formatLang(line['ldate'], date=True) or ''|entity }</td>
                    <td>${ line['jname']  or ''|entity }</td>
                    <td>${ line['partner_name']  or ''|entity }</td>
                    <td>${ line['lref']  or ''|entity }</td>
                    <td>${ line['move']  or ''|entity }</td>
                    <td>${ line['lname']  or ''|entity }</td>
                    <td class="right">${ formatLang(line['debit'], digits=get_digits(dp='Account')) |entity}</td>
                    <td class="right">${ formatLang(line['credit'], digits=get_digits(dp='Account')) |entity}</td>
                    <td class="right">${ line['progress'] |entity}</td>
                </tr>
            %endfor
            <tr style="page-break-inside: avoid; vertical-align:text-top;">
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td class="right">${ _('Total') }</td>
                <td class="right">${ formatLang(compute_totals(a)['total_debit'], digits=get_digits(dp='Account')) | entity}</td>
                <td class="right">${ formatLang(compute_totals(a)['total_credit'], digits=get_digits(dp='Account')) | entity}</td>
                <td></td>
            </tr>
        </table>
    %endfor
    ## ${ ipdb(data) }
</div>
</body>
</html>
