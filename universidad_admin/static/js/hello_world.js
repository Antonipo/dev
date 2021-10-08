
/*
odoo.define('universidad_admin.teacher', function (require) {
    "use strict";

    const teacher = require('universidad_admin.models');

    teacher.load_fields("college.teacher",["calculate_today"])

    class PosSalary extends teacher{
        async onclick(){
            alert('has sido modificado')
            this.showPopup('selectionPopup',{title : 'Has modificado'})
        }
    }

    return PosSalary ;

});
*/
odoo.define('hello_world.main', function (require) {
    "use strict";
    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    const OurAction =AbstractAction.extend({  template: "hello_world.CLientAction",  info: "this message comes from the JS"});
    core.action_registry.add('hello_world.action', OurAction);
});
