
# 🔐 Flask Secure File Share

A secure Flask web application that allows users to upload files protected by a password, then retrieve them via a unique UUID link and a password form. Built for privacy, security, and clean development.

---

## 🚀 Features

- 🔒 Upload any file (max 16MB) with a password  
- 🔗 Generates a unique UUID-based download link  
- 🥪 Password-protected file access with Flask-WTF  
- 🔐 Passwords hashed using secure algorithms  
- 🗂️ Files saved using secure filenames  
- 🧼 CSRF protection and file type restrictions  
- 🐘 PostgreSQL database (Dockerized)  
- 🐳 Fully Dockerized development environment  
- 📁 Integration and service-level tests with pytest  
- 💬 Flash messages and error handlers for clean UX  
- 🌐 Styled with Tailwind CSS and shared layout  

---

## 🛠️ Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate  
- **Forms & Security:** Flask-WTF, Password Hashing, CSRF  
- **Database:** PostgreSQL (via Docker Compose)  
- **Frontend:** Jinja2 templates + Tailwind CSS  
- **Testing:** Pytest, BeautifulSoup (for CSRF token extraction)  
- **DevOps:** Docker, Docker Compose, Shell Entry Point  

---

## 📁 Project Structure

~~~text
.
├── app/
├── migrations/
├── tests/
├── uploads/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
~~~

---

## 🚀 Setup (Docker)

### 1. Clone the repository

~~~bash
git clone https://github.com/Urs97/flask-secure-file-share-app
cd flask-secure-file-share-app
~~~

### 2. Configure environment

Create a `.env` file in the root directory and copy the content from `.env.example` into it:

~~~bash
cp .env.example .env
~~~

### 3. Build and run the app

~~~bash
docker-compose up --build
~~~

Your app should now be available at:  
http://localhost:5001

---

## 🧪 Running Tests

~~~bash
docker-compose exec web pytest
~~~

---

## 🔄 Database Migrations

~~~bash
docker-compose exec web flask db migrate -m "Add something"
docker-compose exec web flask db upgrade
~~~

---

## 🧐 How It Works

1. **Upload a file**  
   Visit `/`, choose a file, and set a password.

2. **Share the link**  
   You get a unique UUID link like `/get-file/<uuid>`.

3. **Download**  
   Visit that link and enter the password to download the file.

4. **Security**  
   Passwords are hashed, files are saved securely, and only accessible with correct credentials.

---

## ⚙️ Environment Variables

| Key                  | Description                    | Default                                |
|----------------------|--------------------------------|----------------------------------------|
| `SECRET_KEY`         | Flask app secret key           | `super-secret-key`                     |
| `DATABASE_URL`       | PostgreSQL connection string   | `postgresql://...`                     |
| `UPLOAD_FOLDER`      | Path to store uploaded files   | `uploads/`                             |
| `MAX_CONTENT_LENGTH` | Max upload size in bytes       | `16777216` (16 MB)                     |

---

## 🔐 Security Features

- Passwords hashed with `werkzeug.security`  
- Uploads stored securely with `secure_filename`  
- CSRF protection on all forms (via Flask-WTF)  
- Flash messages + error handling for user feedback  
- Max upload size enforced: 16MB (`413` if exceeded)

---

## 🧑‍💻 VS Code Dev Container (Optional)

If you're using [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers), this project includes a ready-to-go `.devcontainer` setup.

### ⚙️ Features

- ✅ Runs inside the same Docker Compose environment
- ✅ Automatically installs Python extensions and dependencies
- ✅ Perfect for remote development or GitHub Codespaces

### ▶️ Usage

1. Install [Docker](https://www.docker.com/) and [Visual Studio Code](https://code.visualstudio.com/)
2. Make sure the **Dev Containers** extension is installed in VS Code
3. Open the project in VS Code
4. When prompted, **"Reopen in Container"**

Or manually:

~~~bash
Ctrl+Shift+P → Dev Containers: Reopen in Container
~~~

---

## 📌 Commit Guide

Follow conventional commits:

- `feat:` for new features  
- `fix:` for bug fixes  
- `test:` for tests  
- `docs:` for documentation  
- `chore:` for non-code changes (e.g., setup)
