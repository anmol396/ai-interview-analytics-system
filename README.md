# AI Interview Analytics System

> AI-powered HR analytics platform for intelligent candidate evaluation, hiring insights, and conversational analytics.

<p align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi\&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react\&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite\&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python\&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-yellow)

</p>

---

# Project Overview

AI Interview Analytics System is a full-stack intelligent recruitment platform built to help HR teams streamline candidate evaluation and decision-making.

The platform combines structured analytics with AI-assisted interaction by routing requests between databases and Large Language Models (LLMs) to deliver fast, contextual, and actionable hiring insights.

### Objectives

* Simplify candidate management
* Generate intelligent hiring insights
* Enable conversational data analysis
* Improve recruitment efficiency
* Support scalable analytics workflows

---

# Features

### HR Analytics Dashboard

* Candidate statistics
* Hiring performance tracking
* Recruitment insights

### Candidate Management

* Add candidates
* Edit candidate records
* Delete entries
* Track evaluation progress

### AI Hiring Assistant

* Natural language interaction
* Candidate analysis
* Smart recommendation generation

### Automated Candidate Scoring

Calculates final evaluation score using:

* Written Round
* Technical Round
* PM Round
* HR Round

### Authentication & Security

* JWT Authentication
* Protected APIs
* Secure session handling

### Multi-LLM Routing

Supports:

* Google Gemini
* Groq
* Fallback handling

### Monitoring

* Health checks
* Database reconnection

---

# Screenshots

## Dashboard

![Dashboard](docs/dashboard-dark.png)

---

## AI Assistant

![AI Assistant](docs/ai-assistant-dark.png)

---

## About Page

![About](docs/about-dark.png)

---

## Login & Signup

| Login                    | Signup                    |
| ------------------------ | ------------------------- |
| ![](docs/login-dark.png) | ![](docs/signup-dark.png) |

---

# System Architecture

The application follows a layered architecture where requests move through processing services before reaching databases or AI providers.

![System Architecture](docs/architecture-dark.png)

---

# Data Pipeline

The assistant processes requests using intent classification and dynamic routing.

![Data Pipeline](docs/pipeline-dark.png)

Flow:

```text
User Input
→ Validation
→ Intent Classification
→ SQL / AI Routing
→ Response Generation
→ UI Rendering
```

---

# Tech Stack

| Layer          | Technologies                  |
| -------------- | ----------------------------- |
| Frontend       | React, Vite, Tailwind CSS     |
| Backend        | FastAPI, SQLAlchemy, Pydantic |
| Database       | MySQL                         |
| Authentication | JWT                           |
| AI             | Google Gemini, Groq           |
| Visualization  | Recharts                      |

---

# Project Structure

```text
ai-interview-analytics-system/
│
├── backend/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── tests/
│   ├── database.py
│   ├── models.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── docs/
│   ├── dashboard-dark.png
│   ├── ai-assistant-dark.png
│   ├── about-dark.png
│   ├── architecture-dark.png
│   └── pipeline-dark.png
│
├── .env.example
├── requirements.txt
├── README.md
└── run.py
```

---

# Setup

## Clone Repository

```bash
git clone https://github.com/anmol396/ai-interview-analytics-system.git

cd ai-interview-analytics-system
```

---

## Environment Setup

Create environment file:

```bash
cp .env.example .env
```

Example:

```env
DATABASE_URL=
API_BASE_URL=
VITE_API_BASE_URL=
GOOGLE_API_KEY=
GROQ_API_KEY=
SECRET_KEY=
```

---

## Backend Setup

```bash
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python run.py
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# API Overview

## Authentication

POST `/auth/signup`
POST `/auth/token`

---

## Candidates

GET `/candidates`

POST `/candidates`

PUT `/candidates/{id}`

DELETE `/candidates/{id}`

---

## Dashboard

GET `/dashboard-stats`

---

## AI Assistant

POST `/chat`

---

## Health

GET `/health`

POST `/reconnect-db`

---

# Testing

Run verification scripts:

```bash
python backend/tests/verify_gemini_migration.py

python backend/tests/groq_verification.py

python backend/tests/ai_self_test.py
```

---

# Future Scope

* Resume parsing
* Role-based access control
* Email notifications
* Advanced analytics
* Docker deployment
* Cloud hosting

---


# License

Licensed under MIT License.
