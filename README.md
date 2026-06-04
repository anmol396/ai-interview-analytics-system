# AI Interview Analytics System

> AI-powered HR analytics platform delivering intelligent candidate evaluation, real-time hiring insights, automated scoring, and conversational analytics.

<p align="center">

![Stars](https://img.shields.io/github/stars/anmol396/ai-interview-analytics-system?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/anmol396/ai-interview-analytics-system?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/anmol396/ai-interview-analytics-system?style=for-the-badge)

<br>

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi\&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react\&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite\&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

</p>

---

# Project Overview

AI Interview Analytics System is a production-ready full-stack recruitment intelligence platform designed to modernize candidate evaluation and hiring decisions.

The system combines structured analytics with conversational AI by routing requests intelligently between databases and Large Language Models (LLMs) to deliver actionable recruitment insights.

### Objectives

* Improve recruitment workflows
* Enable intelligent hiring decisions
* Deliver conversational analytics
* Automate candidate evaluation
* Support scalable analytics operations

---

# Features

| Module                    | Description                                                                  |
| ------------------------- | ---------------------------------------------------------------------------- |
| HR Analytics Dashboard    | View candidate statistics, hiring trends, rankings, and recruitment insights |
| Candidate Evaluation      | Candidate assessment lifecycle and intelligent evaluation workflows          |
| AI Hiring Assistant       | Conversational interface for hiring insights and recommendations             |
| Automated Scoring         | Aggregate Written, Technical, PM, and HR assessment scores                   |
| Authentication & Security | JWT authentication with protected routes                                     |
| Multi-LLM Routing         | Dynamic routing across Gemini, Groq, and fallback providers                  |
| System Monitoring         | Database health checks and recovery endpoints                                |

---

# Screenshots

## Dashboard

![Dashboard](docs/dashboard.png)

---

## AI Assistant

![AI Assistant](docs/ai-assistant.png)

---

## About Page

![About](docs/about.png)

---

## Login & Signup

| Login               | Signup               |
| ------------------- | -------------------- |
| ![](docs/login.png) | ![](docs/signup.png) |

---

# System Architecture

The platform follows a layered architecture where frontend interactions are processed through backend services and routed toward structured retrieval or AI generation.

![System Architecture](docs/system_architecture.png)

Architecture Flow:

```text
React Frontend
↓
FastAPI Backend
↓
Authentication + Processing
↓
Database / AI Layer
↓
Response Generation
```

---

# Data Pipeline

The assistant processes requests through validation, classification, intelligent routing, and response generation.

![Data Pipeline](docs/data_pipeline.png)

```text
User Input
→ Validation
→ Intent Classification
→ SQL / AI Routing
→ Response Generation
→ JSON Response
→ UI Rendering
```

---

# Tech Stack

| Category       | Technologies                             |
| -------------- | ---------------------------------------- |
| Frontend       | React • Vite • Tailwind CSS • Axios      |
| Backend        | FastAPI • SQLAlchemy • Pydantic • Python |
| Database       | MySQL                                    |
| Authentication | JWT • Passlib                            |
| AI & LLM       | Google Gemini API • Groq API             |
| Visualization  | Recharts                                 |
| Environment    | python-dotenv                            |

---

# Project Structure

```text
ai-interview-analytics-system/

backend/
├── routes/
├── schemas/
├── services/
├── tests/
├── database.py
├── models.py
└── main.py

frontend/
├── src/
├── package.json
├── tailwind.config.js
└── vite.config.js

docs/
├── dashboard.png
├── ai-assistant.png
├── about.png
├── system_architecture.png
└── data_pipeline.png

.env.example
requirements.txt
README.md
run.py
```

---

# Setup

## Prerequisites

* Python 3.11+
* Node.js 18+
* MySQL 8+
* Google API Key
* Groq API Key

## Clone Repository

```bash
git clone https://github.com/anmol396/ai-interview-analytics-system.git

cd ai-interview-analytics-system
```

---

## Environment Setup

```bash
cp .env.example .env
```

## Environment Setup

Create environment file:

```bash
cp .env.example .env
```

Configure your environment variables:

```env
# Database (MySQL)
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name

# Frontend / Backend
VITE_API_BASE_URL=http://localhost:8000
API_BASE_URL=http://localhost:8000

# Google Gemini API Key
# Get Key → https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key

# Groq API Key
# Get Key → https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key

# JWT Secret
# Generate → https://generate-secret.vercel.app/32
SECRET_KEY=your_secret_key
```

### Create API Keys

| Service          | Purpose    | Get Key                                |
| ---------------- | ---------- | -------------------------------------- |
| Google AI Studio | Gemini API | https://aistudio.google.com/app/apikey |
| Groq Cloud       | Groq API   | https://console.groq.com/keys          |
| Secret Generator | JWT Secret | https://generate-secret.vercel.app/32  |

> Never commit `.env` to GitHub. Only commit `.env.example`.


---

## Backend Setup

```bash
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python run.py
```

Backend:

```
http://localhost:8000
```

Swagger:

```
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

```
http://localhost:5173
```

---

# API Overview

| Module         | Endpoint                      |
| -------------- | ----------------------------- |
| Authentication | `/auth/signup`, `/auth/token` |
| Candidates     | `/candidates`                 |
| Dashboard      | `/dashboard-stats`            |
| AI Assistant   | `/chat`                       |
| Health         | `/health`, `/reconnect-db`    |

---

# Testing

```bash
python backend/tests/verify_gemini_migration.py

python backend/tests/groq_verification.py

python backend/tests/ai_self_test.py
```

---

# Future Scope

* Resume parsing and evaluation
* Role-based access control
* Email notifications
* Advanced analytics dashboards
* Docker deployment
* Cloud hosting support

---

# Contributors

This project was developed collaboratively with shared ownership across frontend, backend, API integration, testing, and system design.

| Contributor        | Responsibilities                                                                                                                                | GitHub                        | LinkedIn                                            |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | --------------------------------------------------- |
| **Anmol Chawla**   | Frontend Development • UI/UX Design • React + Vite • Dashboard • Login/Signup • AI Assistant • Theme System • Responsive Design • Documentation | https://github.com/anmol396   | https://www.linkedin.com/in/anmol-chawla-b079672b6/ |
| **Drashti Rajgor** | Backend Development • FastAPI APIs • Database Integration • Authentication • AI Services • Backend Testing • System Integration                 | https://github.com/DrashtiRaj | https://www.linkedin.com/in/drashti-r-3437a73b3/    |

### Shared Contributions

* API Integration (Frontend ↔ Backend)
* Testing & Debugging
* System Architecture
* Data Flow Design
* Feature Validation
* Project Collaboration

---

# Support

If you found this project useful:

* ⭐ Star the repository
*  Fork the repository
*  Open issues and suggestions

---
# License

This project is distributed under the [MIT License](LICENSE).  
See the `LICENSE` file for more information.

© 2026 Anmol Chawla & Drashti Rajgor
