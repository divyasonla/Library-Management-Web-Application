# Copyright (c) 2025, divya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Books(Document):
    def validate(self):
        if self.stock < 0:
        # if self.stock < 0:
            frappe.throw("Stock cannot be negative!")
