console.log('si leyo el js')
odoo.define('universidad_admin.hello', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var menubase = AbstractAction.extend({
       init: function (){
           this._super.apply(this,arguments);
           console.log('si entro a la funcion')
           window.alert('Bienvenido usuario')

       }
    });

    core.action_registry.add('hello_world.action',menubase);
    return menubase;


});



