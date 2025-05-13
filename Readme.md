# ✅ FastAPI Todo App with JWT Auth and PostgreSQL

A simple and secure Todo management API using **FastAPI** and **PostgreSQL**, with **JWT-based authentication**. Users can register, log in, and manage their todos—categorized as completed, pending, or overdue.

---


## ✅ Checklist

| Feature                        | Status ✅ |
|-------------------------------|-----------|
| Signup                        | ✅         |
| JWT-based Login               | ✅         |
| Create Todo with deadline     | ✅         |
| View grouped Todos            | ✅         |
| Mark Todo as completed        | ✅         |
| Edit Todo                     | ✅         |
| Delete Todo                   | ✅         |
| PostgreSQL as database        | ✅         |
| Git version control history   | ✅         |
| Uploaded to GitHub            | ✅         |
| Completed before **May 12**   | ✅         |

---

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLModel
- **Authentication**: JWT (OAuth2PasswordBearer)
- **Environment Management**: Python `dotenv`

---

## ⚙️ How to Run the Project

### 1. Clone the repo

```bash
git clone https://github.com/your-username/fastapi-todo-app.git
cd fastapi-todo-app
then setup the .env with your secret values:
DATABASE_URL
SECRET_KEY 
ALGORITHM 
ACCESS_TOKEN_EXPIRE_MINUTES
ACCESS_TOKEN_EXPIRE_MINUTES
Run uvicorn Backend.main:app --reload