import frappe
import csv
import io
import requests

@frappe.whitelist()
def get_books():
    return frappe.db.get_list("Books", fields=["name", "title", ""])
# @frappe.whitelist()
# def issue_book(member, book):
#     member_doc = frappe.get_doc("Member", member)
#     book_doc = frappe.get_doc("Book", book)

#     if member_doc.outstanding_debt > 500:
#         frappe.throw("Outstanding debt is more than Rs.500. Cannot issue book.")

#     if book_doc.stock <= 0:
#         frappe.throw("Book is out of stock.")

#     transaction = frappe.get_doc({
#         "doctype": "Transaction",
#         "member": member,
#         "book": book,
#         "issue_date": frappe.utils.nowdate()
#     })
#     transaction.insert()
    
#     book_doc.stock -= 1
#     book_doc.save()
    
#     return "Book Issued Successfully!"

# @frappe.whitelist()
# def return_book(transaction_id):
#     transaction = frappe.get_doc("Transaction", transaction_id)
#     book_doc = frappe.get_doc("Book", transaction.book)
    
#     rent_fee = calculate_rent(transaction.issue_date)
    
#     member_doc = frappe.get_doc("Member", transaction.member)
#     member_doc.outstanding_debt += rent_fee
#     member_doc.save()
    
#     book_doc.stock += 1
#     book_doc.save()
    
#     transaction.return_date = frappe.utils.nowdate()
#     transaction.rent_fee = rent_fee
#     transaction.save()
    
#     return f"Book Returned! Rent Fee: Rs.{rent_fee}"

# def calculate_rent(issue_date):
#     days_used = (frappe.utils.datetime.datetime.now() - frappe.utils.datetime.datetime.strptime(issue_date, "%Y-%m-%d")).days
#     return days_used * 10  # Rs.10 per day


@frappe.whitelist()
def get_bookslist(title=None, page=1, isbn=None, publisher=None):
    """
    Book DocType se data fetch karta hai.
    
    Parameters:
    - title: Book title ke liye search keyword (partial match allowed)
    - page: Pagination ke liye page number (default 1, 20 records per page)
    - isbn: ISBN ke hisaab se filter karne ke liye
    - publisher: Publisher ke hisaab se filter karne ke liye
    
    Return:
    - Filtered list of books based on provided parameters.
    """
    try:
        page = int(page) if page else 1
        limit = 20
        offset = (page - 1) * limit

        filters = {}
        if title:
            filters["title"] = ["like", "%" + title + "%"]

        if isbn:
            filters["isbn"] = ["like", "%" + isbn + "%"]

        if publisher:
            filters["publisher"] = ["like", "%" + publisher + "%"]


        books = frappe.get_list(
            "Books", 
            filters=filters, 
            fields=["name", "title", "authors", "isbn", "publisher"],
            limit_page_length=limit,
            limit_start=offset
        )
        return books

    except Exception as e:
        frappe.log_error(message=str(e), title="Error in get_bookslist")
        return {"error": str(e)}
    


# import frappe
import requests
@frappe.whitelist(allow_guest=True)
def import_books(count=10, title=None):
    """
    Import books from Frappe Library API and save them in Books DocType.
    """

    api_url = "https://frappe.io/api/method/frappe-library"
    
    # API Parameters
    params = {"page": 1}
    if title:
        params["title"] = title

    # Authentication Headers
    headers = {
        "Authorization": "token c60e280acae152b:6a183b002df47f6"
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if "message" in data:
            books = data["message"][:count]
            for book in books:
                doc = frappe.get_doc({
                    "doctype": "Books",
                    "title": book.get("title"),
                    "authors": book.get("authors"),
                    "isbn": book.get("isbn"),
                    "publisher": book.get("publisher"),
                    "num_pages": book.get("num_pages"),
                })
                doc.insert()
                frappe.db.commit()
            return f"{len(books)} books imported successfully!"
        else:
            return "No books found in API response."
    
    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"
