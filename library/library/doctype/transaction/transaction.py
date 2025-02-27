# Copyright (c) 2025, divya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Transaction(Document):
	# pass
    def before_save(self):
        if self.outstanding_dept > 500:
            frappe.throw("Outstanding debt is more than Rs.500. Cannot issue book.")
