openerp.pec_mail = function(instance)
 {

    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    var _lt = instance.web._lt;
     instance.pec_mail= instance.session.mail.Wall.extend({
        init: function (parent, action) {
            this._super(parent, action);
            this.ActionManager = parent;

            this.action = _.clone(action);
            this.domain = this.action.params.domain || this.action.domain || [];
            this.context = _.extend(this.action.params.context || {}, this.action.context || {});
        },

        bind_events: function () {
            var self=this;
            this.$(".oe_write_full").click(function (event) {
                event.stopPropagation();
                var action = {
                    type: 'ir.actions.act_window',
                    res_model: search['pec_messages'] ? 'mail.compose.message.pec' : 'mail.compose.message',
                    view_mode: 'form',
                    view_type: 'form',
                    action_from: 'mail.ThreadComposeMessage',
                    views: [[false, 'form']],
                    target: 'new',
                    context: {
                    },
                };
                session.client.action_manager.do_action(action);
            });
            this.$(".oe_write_onwall").click(function (event) { self.root.thread.on_compose_message(event); });
        }



     });
    instance.web.client_actions.add('pec_mail', 'instance.pec_mail');


};
