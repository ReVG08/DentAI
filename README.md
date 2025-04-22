# Dental AI Website

Production-ready FastAPI app with admin-only account creation, static web pages, and contact form.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   uvicorn app.main:app --reload
   ```
3. Visit http://127.0.0.1:8000

4. The first user must be created directly in the database as an admin.

## Features

- Home, About Us, Contact a Salesperson (form)
- Login page (admin creates accounts)
- Admin panel (account management)