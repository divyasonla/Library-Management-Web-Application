// Copyright (c) 2025, divya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction", {
    refresh(frm){
        frm.trigger("setfields");
    },
    status: function(frm){
        frm.trigger("setfields");
    },
	setfields : function(frm) {
       if (frm.doc.status == "Issued"){
           set_df_property("issued_date", "hidden", 0);
           set_df_property("return_date", "hidden", 1);
       }
       else if (frm.doc.status == "Returned"){
           set_df_property("issued_date", "hidden", 1);
           set_df_property("return_date", "hidden", 0);
       }
       else{
              set_df_property("issued_date", "hidden", 1);
              set_df_property("return_date", "hidden", 1);
       }
	},
});
