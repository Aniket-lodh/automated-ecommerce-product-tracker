# Automated E-commerce Product Tracker

## Project Overview

This project is an automated platform designed to track e-commerce product information like price, availability, and other relevant details. It uses web automation techniques (similar to Selenium/Playwright) to monitor products and provide real-time updates. The backend is built with FastAPI, SQLAlchemy, and PostgreSQL to manage and store user data, product information, and track changes over time.

## Features

- **User Authentication**: Register new users via email.
- **Product Tracking**: Track product details such as price, availability, and last checked timestamp.
- **Web Automation**: Uses Playwright with Python to automate the process of scraping e-commerce websites for updated product information.
- **Database Integration**: PostgreSQL for storing user and product information. Managed via SQLAlchemy ORM.
- **API Endpoints**: Exposes RESTful APIs to interact with the system.

## Tech Stack

- **Backend**: Python, FastAPI, Playwright, SQLAlchemy
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Web Automation**: Playwright (Python)
- **ORM**: SQLAlchemy
- **API**: RESTful API using FastAPI
- **Database Management Tool**: DBeaver (for managing PostgreSQL)

## Project Structure

    ```bash
        my_project/
        ├── app/
        │   ├── __init__.py
        │   ├── main.py
        │   ├── models.py
        │   ├── crud.py
        │   ├── schemas.py
        │   └── database.py
        ├── .env
        ├── req.txt
        └── readme.md
    ```

## Installation

### Prerequisites

- Python 3.8 or later
- PostgreSQL database (you can install it locally or use a hosted solution like Supabase)

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/Aniket-lodh/automated-ecommerce-product-tracker.git
   cd automated-ecommerce-product-tracker
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r req.txt
   ```

4. Set up your `.env` file with the PostgreSQL connection URL:

   - Create a `.env` file in the root of the project directory.
   - Add the following line:
     ```ini
     SQLALCHEMY_DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
     ```
     Replace `<username>`, `<password>`, `<host>`, `<port>`, and `<database_name>` with your actual PostgreSQL credentials.

5. Run database migrations to set up the database tables:
   ```bash
   uvicorn app.main:app --reload
   ```

## Running the Project

### Start the FastAPI Server

To start the server, run the following command:

```bash
uvicorn app.main:app --reload
```
