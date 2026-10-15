# Expense Tracker API

A REST API built with **FastAPI and PostgreSQL** for registering users and managing personal expenses.


## Features

- User registration with bcrypt password hashing and JWT login (30-minute token expiry)
- Create, view, update, delete, and search expenses by date
- JWT-protected endpoints that restrict expense queries to the authenticated user
- Request validation with Pydantic
- Database error handling and automated API tests with Pytest

## Tech Stack

**Python · FastAPI · PostgreSQL · psycopg2 · Pydantic · bcrypt · PyJWT · Pytest · HTTPX**

## Getting Started

### 1. Install dependencies

```bash
git clone <your-repository-url>
cd Expense_Tracker
python -m venv .venv
```

Activate the environment on Windows:

```bat
.venv\Scripts\activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure PostgreSQL

Create two separate databases: `expense_tracker` for the application and `test_expense_tracker` for tests. Run the following SQL in **each database** to create the tables and sequences expected by the application:

```sql
CREATE SEQUENCE id;
CREATE SEQUENCE sno_seq;

CREATE TABLE user_data (
    user_id       INTEGER NOT NULL DEFAULT nextval('id'::regclass),
    user_name     VARCHAR(40) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    CONSTRAINT pk PRIMARY KEY (user_id),
    CONSTRAINT unq_name UNIQUE (user_name)
);

CREATE TABLE expenses (
    sno             INTEGER NOT NULL DEFAULT nextval('sno_seq'::regclass),
    category        VARCHAR(25) NOT NULL,
    amount          NUMERIC NOT NULL,
    description     VARCHAR(50),
    date_of_expense DATE NOT NULL,
    user_id         INTEGER NOT NULL,
    CONSTRAINT expenses_pkey PRIMARY KEY (sno),
    CONSTRAINT foreign_key FOREIGN KEY (user_id) REFERENCES user_data(user_id)
);
```

`user_data` stores each user's ID, unique username, and password hash. `expenses` stores each expense and links it to a user through `user_id`. The `description` column is nullable; the other listed columns are `NOT NULL`. The database has a primary key on each table, a unique constraint on `user_data.user_name`, and a foreign key from `expenses.user_id` to `user_data.user_id`.

**Validation note:** The current database schema does not have a `CHECK` constraint for positive amounts. The FastAPI/Pydantic request model validates that amounts are greater than zero when requests go through the API.

The test setup truncates and reseeds these tables, so **never point tests at a database containing real data**.

Create `secret_details.env` in the project folder with your local settings:

```env
DB_HOST_NAME=localhost
DB_PORT_NUMBER=5432
DB_DATABASE_NAME=expense_tracker
DB_USER_NAME=your_db_user
DB_PASSWORD=your_db_password
JWT_SECRET_KEY=replace_with_a_strong_random_secret
```

Create `test_details.env` with the test database override:

```env
DB_DATABASE_NAME=test_expense_tracker
```

Keep both `.env` files private. They are ignored by `.gitignore`; do not commit them.

### 3. Run the API

```bash
uvicorn fastapi_app:app --reload
```

Open **http://127.0.0.1:8000/docs** to explore and try the endpoints with Swagger UI.

## API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| `POST` | `/user-registration` | Register a user | No |
| `POST` | `/user-login` | Log in and receive a JWT | No |
| `POST` | `/add-expense` | Add an expense | Yes |
| `GET` | `/view-expense` | List your expenses | Yes |
| `PUT` | `/update-expense` | Update an expense amount | Yes |
| `DELETE` | `/delete-expense?sno=1` | Delete an expense by serial number | Yes |
| `GET` | `/search-expense?date_of_expense=2026-10-15` | Search by date | Yes |

For protected endpoints, send the token in the header: `Authorization: Bearer <your_token>`.

## Run Tests

```bash
# Run from the parent directory containing the Expense_Tracker folder
python -m pytest Expense_Tracker/test_fastapi_app.py
```

The tests use `test_details.env` to select `test_expense_tracker`. The test fixture truncates and reseeds `user_data` and `expenses`; confirm the test database configuration before running the suite.

## Project Structure

```text
fastapi_app.py       # FastAPI routes and Pydantic models
Operations.py        # Application operations and SQL queries
connection.py        # PostgreSQL connection/context manager
conftest.py          # Test database fixtures
test_fastapi_app.py  # API tests
requirements.txt     # Python dependencies
```
