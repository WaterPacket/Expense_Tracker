# Expense Tracker API

A REST API built with **FastAPI and PostgreSQL** for registering users and managing personal expenses.


## Features

- User registration with bcrypt password hashing and JWT login (30-minute token expiry)
- Create, view, update, delete, and search expenses by date
- Every expense has its own permanent `expense_id`, used for updating and deleting
- Expense lists show a per-user serial number (`sno`) for easy reading
- JWT-protected endpoints that restrict expense queries and changes to the authenticated user
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
CREATE SEQUENCE user_id_sec;
CREATE SEQUENCE expense_id_sec START WITH 1000;

CREATE TABLE user_data (
    user_id       INTEGER NOT NULL DEFAULT nextval('user_id_sec'::regclass),
    user_name     VARCHAR(40) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    CONSTRAINT pk_user_id PRIMARY KEY (user_id),
    CONSTRAINT unq_name UNIQUE (user_name)
);

CREATE TABLE expenses (
    category        VARCHAR(25) NOT NULL,
    amount          NUMERIC NOT NULL,
    description     VARCHAR(50),
    date_of_expense DATE NOT NULL,
    user_id         INTEGER NOT NULL,
    expense_id      INTEGER NOT NULL DEFAULT nextval('expense_id_sec'::regclass),
    CONSTRAINT pk PRIMARY KEY (expense_id),
    CONSTRAINT fk FOREIGN KEY (user_id) REFERENCES user_data(user_id)
);

ALTER SEQUENCE user_id_sec OWNED BY user_data.user_id;
ALTER SEQUENCE expense_id_sec OWNED BY expenses.expense_id;
```

**Tables**

- `user_data` stores each user's ID, unique username, and password hash.
- `expenses` stores each expense and links it to a user through `user_id`.

**Columns and keys**

- `expense_id` is the primary key of `expenses`. It is generated from `expense_id_sec`, starts at 1000, and is unique across all users. It never changes, so it is safe to use for updates and deletes.
- `sno` is **not** a column. It is calculated in the queries with `row_number()` each time expenses are listed (see [`sno` vs `expense_id`](#sno-vs-expense_id)).
- `description` is nullable; the other columns are `NOT NULL`.
- `user_data.user_name` has a unique constraint, and `expenses.user_id` is a foreign key to `user_data.user_id`.

**Why `OWNED BY`:** the test setup runs `TRUNCATE ... RESTART IDENTITY`, which only resets sequences that are owned by a column of the truncated tables. Without the two `ALTER SEQUENCE ... OWNED BY` lines, the ids would keep counting up between test runs instead of starting again at 1000 (expenses) and 1 (users).

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

| Method | Endpoint | Input | Purpose | Auth |
|---|---|---|---|---|
| `POST` | `/user-registration` | JSON: `user_name`, `password` (8–24 characters each) | Register a user | No |
| `POST` | `/user-login` | JSON: `user_name`, `password` | Log in and receive a JWT | No |
| `POST` | `/add-expense` | JSON: `category`, `amount` (> 0), `description`, `date_of_expense` | Add an expense | Yes |
| `GET` | `/view-expense` | none | List your expenses | Yes |
| `PUT` | `/update-expense` | JSON: `expense_id`, `amount` (> 0) | Update the amount of one expense | Yes |
| `DELETE` | `/delete-expense?expense_id=1000` | query: `expense_id` | Delete one expense | Yes |
| `GET` | `/search-expense?date_of_expense=2026-10-15` | query: `date_of_expense` | List your expenses on that date | Yes |

For protected endpoints, send the token in the header: `Authorization: Bearer <your_token>`.

### `sno` vs `expense_id`

- `sno` is a display number only. It is calculated per user (1, 2, 3, ...), ordered by date with the newest first. It changes when expenses are added or removed, so it must not be used to modify an expense.
- `expense_id` is the permanent id of an expense. Use it with `/update-expense` and `/delete-expense`.
- In `/search-expense`, `sno` is numbered within the search results, not within your full list.

### Example response (`/view-expense` and `/search-expense`)

```json
[
  {
    "sno": 1,
    "category": "food",
    "amount": "250",
    "description": "lunch",
    "date_of_expense": "2026-10-15",
    "expense_id": 1004
  }
]
```

### Update example

```json
PUT /update-expense
{
  "expense_id": 1004,
  "amount": 300
}
```

### Error responses

| Status | Meaning |
|---|---|
| `401` | Missing, invalid, or expired token, or wrong username or password |
| `404` | `expense_id` does not exist or belongs to another user |
| `409` | Username already exists (registration) |
| `422` | Invalid or missing input |
| `500` | Internal database error |
| `503` | Database connection failure |

You can only update or delete your own expenses. Using another user's `expense_id` returns `404`, the same as an id that does not exist.

## Run Tests

From inside the project folder:

```bash
pytest
```

Pytest loads `secret_details.env` first, then loads `test_details.env` with override enabled so the test database setting takes precedence. Before opening a database connection, the `channel` fixture checks that `DB_DATABASE_NAME` is exactly `test_expense_tracker`. The `cursor` and `dict_cursor` fixtures use that shared connection. An autouse, session-scoped fixture truncates and reseeds `user_data` and `expenses` once per test session—not before each individual test. Run the test suite only against the dedicated test database: the `TRUNCATE` operation deletes existing rows from those tables.

The seed data contains four users (`user_one`, `user_two`, `user_three`, `sk_sabir`) with one expense each. Because `expense_id_sec` starts at 1000 and is restarted by the truncate, their expenses always get ids 1000 to 1003, and several tests rely on these ids.

The suite covers validation, token handling, and expense operations for every endpoint, plus ownership tests that check that updating or deleting another user's `expense_id` returns `404`.

## Project Structure

```text
fastapi_app.py       # FastAPI routes and Pydantic models
Operations.py        # Application operations and SQL queries
connection.py        # PostgreSQL connection/context manager
conftest.py          # Test database fixtures
test_fastapi_app.py  # API tests
requirements.txt     # Python dependencies
```
