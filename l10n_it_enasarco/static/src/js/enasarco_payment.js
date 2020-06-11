odoo.define('l10n_it_enasarco.enasarco_payment', function (require) {
"use strict";

var bus = require('bus.bus').bus;
var core = require('web.core');
var AccountPayment = require('account.payment');
var AccountPaymentWidget = core.form_widget_registry.get('payment');

AccountPaymentWidget.include({
	render_value: function() {
	    // Your code
			var result = this._super();
			var info = JSON.parse(this.get('value'));
			console.debug('test');
			return result;
	    }
});


AccountPayment.include({
	render_value: function() {
	    // Your code
			var result = this._super();
			var info = JSON.parse(this.get('value'));
			console.debug('test');
			return result;
	    }
});
});
