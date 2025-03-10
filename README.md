## Library Management System

#### Overview

This Library Management Web Application is designed to help librarians efficiently manage books, track issued books, and maintain records of members and transactions. The application is built using the Frappe framework with a Python backend and provides functionalities for book management, member management, transactions, and data import from an external API.

## Features

#### Base Library System

#### Books Management: Add, update, delete, and search books.

#### Member Management: Add, update, delete, and search members.

#### Transactions:

Issue a book to a member.

Return a book from a member.

Charge a rent fee on book returns.

Ensure a member’s outstanding debt does not exceed Rs. 500.

Search Books: Search books by title and author.

## Data Import Integration

Import books from the Frappe Library API.

Specify parameters such as title, author, publisher, and number of books.

Automate book entry creation in the system.

## Technology Stack

Backend: Python (Frappe Framework)

Frontend: vue.js, frappe UI 

Database: MariaDB

API Integration: Frappe Library API


## Installation & Setup

#### Prerequisites

Python (3.x)

Frappe Framework installed

MariaDB/MySQL database

Frappe-UI  (for frontend)

#### Steps

Clone the repository:

git clone https://github.com/yourusername/library-management.git
cd library-management

Install dependencies:

pip install -r requirements.txt

Setup Frappe and create a site:

bench new-site library.localhost
bench --site library.localhost install-app library_management

Start the development server:

bench start


## Scren Shots 

![Screenshot from 2025-03-10 11-10-05](https://github.com/user-attachments/assets/b66f17a3-ebe5-4743-abd0-0016865e4164)

