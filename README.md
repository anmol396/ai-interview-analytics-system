# HR Analytics Platform

> A production-ready system delivering intelligent candidate insights, automated scoring, and a real-time interactive assistant for hiring teams.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://reactjs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Project Overview

This platform empowers recruitment processes with data-driven workflows, ensuring HR teams can manage candidates efficiently while gaining deep insights through natural language interactions. It bridges the gap between structured database records and generative language models.


## Features

- **Dashboard Overview** — Live statistics: total candidates, pass/fail rates, and today's activity
- **Candidate Management** — Full CRUD operations for HR records
- **Analyst Assistant** — Chat-based interface for data-driven hiring insights and recommendations
- **Automated Scoring** — Calculates total candidate scores from multi-stage assessments (Written, Technical, PM, HR)
- **JWT Authentication** — Secure login and signup with token-based session management
- **Multi-LLM Routing** — Intelligently routes queries between primary and fallback providers
- **Health Monitoring** — Live database connectivity check and reconnection endpoint

## Architecture

The platform relies on a multi-layered design. The React frontend communicates with a Python backend, which handles authentication, processing logic, and routing queries either to the database or external language models.

## Data Pipeline

When a user submits a query through the assistant, the request is validated, classified by intent, and branched. Structured intents are translated into SQL for exact data retrieval, while unstructured queries fall back to generative models. Both paths merge to return a formatted JSON payload rendered in the UI.

## Tech Stack

| Layer       | Technology                                      |
|-------------|------------------------------------------------|
| Backend     | FastAPI, SQLAlchemy, Pydantic, python-dotenv    |
| Frontend    | React (Vite), Axios, Tailwind CSS, Recharts     |
| Database    | MySQL                                           |
| LLM         | Google Gemini API, Groq API                     |
| Auth        | JWT (`python-jose`), Passlib (`bcrypt`)         |

## Project Structure

```
ai-interview-system/
├── backend/
│   ├── routes/          # API endpoints
│   ├── schemas/         # Pydantic request/response models
│   ├── services/        # Processing logic & LLM integrations
│   ├── tests/           # Verification scripts
│   ├── database.py      # Connection & retry logic
│   ├── main.py          # Application entry point
│   └── models.py        # SQLAlchemy ORM models
├── frontend/
│   ├── src/             # React application source code
│   ├── index.html       # Vite entry point
│   ├── package.json     # Node dependencies
│   ├── tailwind.config.js
│   └── vite.config.js
├── .env.example         # Environment variable template
├── requirements.txt     # Python dependencies
└── run.py               # Backend launcher
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL 8.0+ (local or hosted)
- A Google API key ([get one here](https://ai.google.dev/))
- A Groq API key ([get one here](https://console.groq.com/))

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-interview-system.git
cd ai-interview-system
```

## Environment Setup

Copy the template and fill in your credentials:

```bash
cp .env.example .env
```

Ensure your `.env` contains valid configuration (no secrets are stored in `.env.example`):

| Variable              | Description                                      |
|-----------------------|--------------------------------------------------|
| `DATABASE_URL`        | Connection string (SQLAlchemy format)            |
| `VITE_API_BASE_URL`   | Backend base URL (used by the frontend)          |
| `API_BASE_URL`        | Backend base URL (used by the backend)           |
| `GOOGLE_API_KEY`      | Primary LLM API key                              |
| `GROQ_API_KEY`        | Fallback LLM API key                             |
| `SECRET_KEY`          | Secret key for JWT token signing                 |

## Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Start Backend Server

```bash
# From the project root
python run.py
```

- **Backend URL:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

- **Frontend URL:** http://localhost:5173

## API Endpoints

### Authentication
| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| `POST` | `/auth/signup`       | Register a new user account              |
| `POST` | `/auth/token`        | Login and receive a JWT access token     |

### Candidates
| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| `GET`  | `/candidates/`       | List all records                         |
| `POST` | `/candidates/`       | Add a new evaluation                     |
| `PUT`  | `/candidates/{id}`   | Update an existing record                |
| `DELETE` | `/candidates/{id}` | Delete a record                          |

### Analytics
| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| `GET`  | `/dashboard-stats`   | Retrieve dashboard statistics            |

### AI Assistant
| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| `POST` | `/chat`              | Chat with the Analyst                    |

### Health
| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| `GET`  | `/health`            | Check database and API status            |
| `POST` | `/reconnect-db`      | Trigger a MySQL reconnection attempt     |

## Testing

Verification scripts are available in `backend/tests/`:

```bash
# Verify SDK migration
python backend/tests/verify_gemini_migration.py

# Verify Groq connectivity
python backend/tests/groq_verification.py

# Run full pipeline self-test
python backend/tests/ai_self_test.py
```

## Future Enhancements

- [ ] Resume (PDF) upload and parsing
- [ ] Role-based access control (Admin / HR / Viewer)
- [ ] Email notifications for status changes
- [ ] Advanced trend graphs
- [ ] Docker + Docker Compose support



## License

This project is licensed under the [MIT License](LICENSE).

## UI Screenshots

- **Login Page**  
  ![Login](docs/login.png)
- **Signup Page**  
  ![Signup](docs/signup.png)
- **Dashboard Overview**  
  ![Dashboard](docs/dashboard.png)
- **AI Assistant Interface**  
  ![AI Assistant](docs/ai-assistant.png)
- **About Page (Data Pipeline)**  
  ![About](docs/about.png)
