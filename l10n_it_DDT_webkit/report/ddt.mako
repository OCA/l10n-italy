<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>

<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>
    %for picking in objects:
        <% setLang(picking.partner_id.lang) %>
        <div class="address">
            <table class="recipient">
                %if picking.partner_id.parent_id:
                <tr><td class="name">${picking.partner_id.parent_id.name or ''}</td></tr>
                <tr><td>${picking.partner_id.title and picking.partner_id.title.name or ''} ${picking.partner_id.name }</td></tr>
                <% address_lines = picking.partner_id.contact_address.split("\n")[1:] %>
                %else:
                <tr><td class="name">${picking.partner_id.title and picking.partner_id.title.name or ''} ${picking.partner_id.name }</td></tr>
                <% address_lines = picking.partner_id.contact_address.split("\n") %>
                %endif
                %for part in address_lines:
                    %if part:
                    <tr><td>${part}</td></tr>
                    %endif
                %endfor
            </table>
            <%
            invoice_addr = invoice_address(picking)
            %>
            <table class="invoice">
                <tr><td class="address_title">${_("Invoice address:")}</td></tr>
                <tr><td>${invoice_addr.title and invoice_addr.title.name or ''} ${invoice_addr.name }</td></tr>
                %if invoice_addr.contact_address:
                    <% address_lines = invoice_addr.contact_address.split("\n") %>
                    %for part in address_lines:
                        %if part:
                        <tr><td>${part}</td></tr>
                        %endif
                    %endfor
                %endif
            </table>
        </div>
        
        <h1 style="clear:both;">${_(u'Delivery Order') } ${picking.name}</h1>
        
        <table class="basic_table" width="100%">
            <tr>
                <td style="font-weight:bold;">${_("Contact")}</td>
                <td style="font-weight:bold;">${_("Origin")}</td>
                <td style="font-weight:bold;">${_("Scheduled Date")}</td>
                <td style="font-weight:bold;">${_('Weight')}</td>
                <td style="font-weight:bold;">${_('Delivery Method')}</td>
                <td style="font-weight:bold;">${_('Incoterm')}</td>
            </tr>
            <tr>
                <td>${user.name}</td>
                <td>${picking.origin or ''}</td>
                <td>${formatLang(picking.min_date, date=True)}</td>
                <td>${picking.weight}</td>
                <td>${picking.carrier_id and picking.carrier_id.name or ''}</td>
                <td>${picking.sale_id and picking.sale_id.incoterm and picking.sale_id.incoterm.name or ''}</td>
            </tr>
        </table>
    
        <table class="list_sale_table" width="100%" style="margin-top: 20px;">
            <thead>
                <tr>
                    <th style="text-align:left; ">${_("Description")}</th>
                    <th style="text-align:left; ">${_("Serial Number")}</th>
                    <th class="amount">${_("Quantity")}</th>
                </tr>
            </thead>
            <tbody>
            %for line in picking.move_lines:
                <tr class="line">
                    <td style="text-align:left; " >${ line.name }</td>
                    <td style="text-align:left; " >${ line.prodlot_id and line.prodlot_id.name or ''}</td>
                    <td class="amount" >${ formatLang(line.product_qty) } ${line.product_uom.name}</td>
                </tr>
            %endfor
        </table>
        
        <br/>
        %if picking.note :
            <p class="std_text">${picking.note | carriage_returns}</p>
        %endif

        <p style="page-break-after: always"/>
    <br/><br/><br/><br/>
     <table class="basic_table" width="100%">
            <tr>
                <td style="font-weight:bold;">Data Ritiro</td>
                <td style="font-weight:bold;">Firma</td>
            </tr>
            <tr>
                <td><br /></td>
                <td><br /><br /></td>
            </tr>
        </table>
    %endfor
</body>
</html>
