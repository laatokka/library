# Library System

## Overview
A modern Django project for managing a library, featuring:
*   Django 6.0
*   PostgreSQL connectivity
*   Tailwind CSS (via CDN for simplicity, or setup via npm for production)
*   HTMX for dynamic interactions
*   Alpine.js for client-side reactivity
*   Django Cotton for component-based UI
*   Playwright for E2E testing

## Prerequisites
*   Python 3.12+
*   PostgreSQL (optional, defaults to environment variables)

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repo_url>
    cd library_system
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup**:

    **Using Docker (Recommended):**
    You can easily start the database using Docker Compose:
    ```bash
    docker-compose up -d
    ```

    **Manual Setup:**
    Ensure PostgreSQL is running and create a database (default `library_db`).
    Export environment variables if different from defaults:
    ```bash
    export DB_NAME=library_db
    export DB_USER=postgres
    export DB_PASSWORD=postgres
    export DB_HOST=localhost
    export DB_PORT=5432
    ```

5.  **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

## Running Tests
Run Playwright E2E tests:
```bash
pytest
```
