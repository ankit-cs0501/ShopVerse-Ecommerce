# ShopVerse — Advanced Flask + MySQL E-Commerce

A portfolio-ready e-commerce starter built with Flask, MySQL, SQLAlchemy, Flask-Login, CSRF protection and Bootstrap 5.

## Features
- Customer registration, login and logout; password hashing
- Product catalogue, category filter and keyword search
- Product detail pages, inventory display and customer reviews
- User-specific shopping cart with quantity validation
- Checkout, stock decrement and order history
- Admin dashboard, product activation/deactivation and order status management
- CSRF protection on forms
- Docker Compose deployment with persistent MySQL volume

## Tech stack
Python 3.12 · Flask · Flask-SQLAlchemy · MySQL 8 · PyMySQL · Flask-Login · Flask-WTF · Bootstrap 5 · Docker

## Run locally (Windows PowerShell)

1. Install Python 3.11+ and MySQL 8.
2. Create a database and user. In MySQL Workbench, run `schema.sql` (change the password first).
3. Open this folder in VS Code / PowerShell:

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

4. Edit `.env` and set your MySQL username, password, host and database.
5. Start the app:

```powershell
python run.py
```

Open http://127.0.0.1:5000

## Demo admin
- Email: `admin@shopverse.local`
- Password: `Admin@12345`

Change this password immediately and remove/replace demo seeding before any public deployment. The seed account is for local demonstration only.

## Docker deployment

Install Docker Desktop, then from this directory:

```bash
docker compose up --build -d
docker compose logs -f web
```

Open http://localhost:5000. Stop with `docker compose down`; retain database data with the named volume. To reset all data, run `docker compose down -v` (destructive).

## Project structure

```text
shopverse_ecommerce/
├── app/
│   ├── routes/       # main, authentication, shop and admin endpoints
│   ├── templates/    # Jinja templates
│   ├── static/css/   # styles
│   ├── models.py     # relational data models
│   ├── seed.py       # demo catalog and admin
│   └── __init__.py   # app factory and extensions
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── schema.sql
```

## Important production hardening before real customers
This is a working portfolio/demo application, not a payment-ready production store. Before public launch:
- Use a unique, high-entropy `SECRET_KEY` and secrets manager; never commit `.env`.
- Remove the hard-coded demo admin and create admin users securely.
- Add database migrations (Flask-Migrate/Alembic), automated tests and structured logging.
- Add rate limiting, email verification, password reset and stronger account policies.
- Integrate a real payment provider (e.g. Razorpay/Stripe) with server-side signature/webhook verification; never trust client payment status.
- Use HTTPS, secure cookies, reverse proxy, backups, monitoring and least-privilege DB credentials.
- Use transactional row locking for inventory in high-concurrency production checkouts.
- Add pagination, image upload validation/storage (S3), and audit logs.

## Suggested resume description
**ShopVerse — Full-Stack E-Commerce Platform | Python, Flask, MySQL, Docker**
- Built a full-stack shopping platform with authentication, searchable product catalogue, cart, checkout and order tracking.
- Designed relational MySQL models for users, products, categories, carts, orders and reviews using SQLAlchemy.
- Implemented role-based admin operations, inventory validation, CSRF protection and containerized deployment using Docker Compose.
