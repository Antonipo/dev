console.log('si leyo el js')
odoo.define('universidad_admin', function (require) {
    "use strict";
    const core = require('web.core');
    alert(core._t('Bienvenido'));




});

/*

odoo.define('hello_world.main', function (require) {
    "use strict";
    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    const OurAction =AbstractAction.extend({  template: "hello_world.CLientAction"});
    core.action_registry.add('hello_world.action', OurAction);
});
*/

