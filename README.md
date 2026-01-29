# Job Application Tracker

A modern, full-stack web application for tracking job applications with an intuitive UI built with Vue.js and PrimeVue.

## 🚀 Features (Phase 1 - MVP)

- ✅ **Complete CRUD Operations**: Create, read, update, and delete job applications
- ✅ **Rich Data Tracking**: Company name, position, location, job type/level, status, dates, notes
- ✅ **Modern UI**: Built with PrimeVue v4 components and Aura theme
- ✅ **Data Persistence**: PostgreSQL database with automatic schema creation
- ✅ **Containerized**: Fully Dockerized application with single-command deployment
- ✅ **Production Ready**: Gunicorn WSGI server, nginx reverse proxy, health monitoring

## 📋 Prerequisites

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Bun** (optional, for local frontend development)

## 🏃 Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd /root/projects/JobApplicationTracker

# Generate environment configuration
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

The setup script will:
- Auto-generate secure passwords and secret keys
- Prompt for application host (default: `localhost:8080`)
- Prompt for optional Google Tag Manager ID
- Create a `.env` file with all configuration

### 2. Start the Application

```bash
# Build and start all services
docker compose up --build
```

This will start:
- **PostgreSQL 16** database
- **Flask backend** with Gunicorn (Python 3.12)
- **Vue 3 frontend** with PrimeVue v4
- **Nginx** reverse proxy

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:8080
```

## 🛠️ Development

### Backend Development

```bash
# View backend logs
docker compose logs -f backend

# Access backend container
docker compose exec backend bash

# Run database migrations (if needed)
docker compose exec backend python -c "from app.database import db; from app import create_app; app = create_app(); app.app_context().push(); db.create_all()"
```

### Frontend Development

For local development with hot-reload:

```bash
cd frontend
bun install
bun run dev
```

The dev server will start at `http://localhost:5173` with API proxying to the backend.

### Database Access

```bash
# Access PostgreSQL CLI
docker compose exec postgres psql -U tracker_user -d job_tracker

# Backup database
docker exec job_tracker_postgres pg_dump -U tracker_user job_tracker > backup.sql

# Restore database
docker exec -i job_tracker_postgres psql -U tracker_user job_tracker < backup.sql
```

## 🏗️ Architecture

### Tech Stack

**Backend:**
- Python 3.12
- Flask (web framework)
- SQLAlchemy (ORM)
- PostgreSQL 16 (database)
- Gunicorn (WSGI server)

**Frontend:**
- Vue 3 (framework)
- PrimeVue v4 (UI library, Aura theme)
- Vite (build tool)
- Bun (package manager)
- Axios (HTTP client)

**Infrastructure:**
- Docker & Docker Compose
- Nginx (reverse proxy)
- Single Docker network (`job_tracker_network`)

### Directory Structure

```
JobApplicationTracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py       # Flask app factory
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models.py         # Database models
│   │   └── routes.py         # API endpoints
│   ├── Dockerfile
│   ├── requirements.txt
│   └── gunicorn.conf.py
├── frontend/
│   ├── src/
│   │   ├── components/       # Vue components
│   │   ├── services/         # API service
│   │   ├── App.vue          # Root component
│   │   └── main.js          # Vue app entry
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
├── nginx/
│   ├── nginx.conf.template  # Nginx config with env vars
│   └── Dockerfile
├── scripts/
│   └── setup_env.sh         # Environment setup script
├── .env.example             # Environment variables template
├── docker-compose.yml       # Docker orchestration
└── README.md
```

## 🔌 API Endpoints

All API endpoints are prefixed with `/api/`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/applications` | List all applications |
| POST | `/api/applications` | Create new application |
| GET | `/api/applications/<id>` | Get single application |
| PUT | `/api/applications/<id>` | Update application |
| DELETE | `/api/applications/<id>` | Delete application |

### Example API Calls

```bash
# Health check
curl http://localhost:8080/api/health

# Create application
curl -X POST http://localhost:8080/api/applications \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "position_title": "Senior Developer",
    "location": "Remote",
    "job_type": "Full-time",
    "status": "Applied"
  }'

# List all applications
curl http://localhost:8080/api/applications
```

## 🛑 Stopping the Application

```bash
# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes all data)
docker compose down -v
```

## 🐛 Troubleshooting

### Issue: Port 8080 already in use

```bash
# Find and kill process using port 8080
lsof -ti:8080 | xargs kill -9

# Or change APP_HOST in .env to use different port
```

### Issue: Database connection failed

```bash
# Check if PostgreSQL is running
docker compose ps postgres

# View PostgreSQL logs
docker compose logs postgres

# Restart PostgreSQL
docker restart postgres
```

### Issue: Frontend not loading

```bash
# Rebuild nginx container
docker compose up --build nginx

# Check nginx logs
docker compose logs nginx
```

## 📚 Environment Variables

All configuration is managed through the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_HOST` | Application hostname | `localhost:8080` |
| `POSTGRES_DB` | Database name | `job_tracker` |
| `POSTGRES_USER` | Database user | `tracker_user` |
| `POSTGRES_PASSWORD` | Database password | Auto-generated |
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `BACKEND_CORS_ORIGIN` | CORS origin | `http://localhost:8080` |
| `GTM_ID` | Google Tag Manager ID | Empty |

## 🔐 Security Notes

- Never commit `.env` to version control
- Auto-generated secrets use cryptographically secure random generation
- CORS is configured to only allow requests from configured origin
- Input validation on both frontend and backend

## 🚧 Roadmap

### Phase 2: Document Management (Upcoming)
- Resume and cover letter uploads
- Document storage in Docker volumes
- File download functionality

### Phase 3: AI Integration (Planned)
- OpenAI job description parsing
- Automatic field extraction
- AI-powered resume/cover letter feedback

### Phase 4: Authentication (Planned)
- JWT-based authentication
- User session management
- Protected routes

### Phase 5: Advanced Features (Planned)
- In-browser PDF/DOCX viewing
- Analytics dashboard
- Advanced filtering and search

## 📄 License

This project is proprietary.

## 🤝 Contributing

This is a personal project. For inquiries, please contact the repository owner.