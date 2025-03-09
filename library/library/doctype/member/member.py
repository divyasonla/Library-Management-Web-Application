# Copyright (c) 2025, divya and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Member(WebsiteGenerator):
	def before_save(self):
		if self.first_name and self.last_name:
			self.full_name = self.first_name + " " + self.last_name	
		elif self.first_name: 
			self.full_name = self.first_name
		elif self.last_name:
			frappe.throw("Please enter First Name") 

