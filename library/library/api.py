import frappe
import requests

@frappe.whitelist()
def fetch_and_import_books(page=1, limit="20", title=None, authors=None, isbn=None, publisher=None, num_pages=None,language_code=None):
    limit = int(limit) 
    base_url = "https://frappe.io/api/method/frappe-library"
    book_count = 0

    while book_count < limit:
        params = {
            "page": page,
            "title": title,
            "authors": authors,
            "isbn": isbn,
            "publisher": publisher,
            "  num_pages": num_pages, 
            "limit": limit,
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            books = response.json().get('message', [])
            
            if not books:
                break

            for book in books:
                if book_count >= limit:
                    break

                new_book = frappe.get_doc({
                    "doctype": "Books",
                    "title": book.get("title"),
                    "author": book.get("authors"),
                    "isbn": book.get("isbn"),
                    "publisher": book.get("publisher"),
                    "num_pages": book.get("  num_pages"),
                    "language_code": book.get("language_code"),
                    "stock":book.get("text_reviews_count"),
                    "average_rating":book.get("average_rating"),
                    "ratings_count":book.get("ratings_count"),
                })
                new_book.insert()
                book_count += 1  

            page += 1  

        else:
            frappe.throw(f"Error in API request: {response.status_code}")

    frappe.db.commit()  
    return f"{book_count} books successfully imported."
