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

## Book Management: Maintain, Update, and Track books.
![Screenshot from 2025-03-10 11-57-30](https://github.com/user-attachments/assets/5f73a498-4221-47b0-8e64-f4ae93b0f57f)


## Members Management: Add, Edit and delete member details
![Screenshot from 2025-03-10 12-00-01](https://github.com/user-attachments/assets/7d2db944-7d8b-4331-822a-ce17e4976f54)
![Screenshot from 2025-03-10 12-01-10](https://github.com/user-attachments/assets/79937816-3747-49ed-99b3-7f3f46b5acfb)
![Screenshot from 2025-03-10 12-02-12](https://github.com/user-attachments/assets/70ec217d-fd91-4d56-8005-8e4c6e412213)
![Screenshot from 2025-03-10 12-02-24](https://github.com/user-attachments/assets/bdca4fa4-3a04-435e-855c-7e4bd6cc625b)

## Debt Control: Limit debt to Rs. 500 per member


