# Copyright (c) 2025, divya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class Transaction(Document):
	
    def before_submit(self):
        if self.quantity:
            book = frappe.get_doc("Books", self.book)
            book.stock = book.stock - self.quantity
            book.save()
        if self.status == "Issued":
            book = frappe.get_doc("Books", self.book)
            
            book.status = "Issued"
            book.save()
        
        elif self.status == "Returned":
            book = frappe.get_doc("Books", self.book)
            if book.status != "Issued":
                frappe.throw(("This book was not issued, so it cannot be returned."))


            book.status = "Available"
            book.save()
    def validate(self):    
        issue_date = datetime.strptime(self.issue_date, "%Y-%m-%d")
        return_date = datetime.strptime(self.return_date, "%Y-%m-%d")
        if issue_date > return_date:
            frappe.throw("Return Date cannot be before Issue Date")

        # x
        self.total_days = (return_date - issue_date).days

        if self.total_days > 7:  
            frappe.throw("You have exceeded the maximum number of days for returning the book")

        self.rent_fees = self.total_days * 10 * self.quantity

    def before_submit(self):
        if self.rent_fees > 0:
            member = frappe.get_doc("Library Membership", {"member": self.member})
            member.outstanding_dept += self.rent_fees
            member.save()
            frappe.msgprint(f"Late Fee of ₹{self.rent_fees} added for {self.member}")
            