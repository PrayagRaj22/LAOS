<div align="center">

# LAOS — Linux Automation & Observability System

![LAOS Banner](https://img.shields.io/badge/LAOS-Linux%20Automation%20%26%20Observability-00e5a0?style=for-the-badge&logo=linux&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-3+-003b57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-fcc624?style=flat-square&logo=linux&logoColor=black)](https://kernel.org)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=flat-square)]()

**A production-grade Linux server monitoring and automation platform.**
Real-time metrics · Log rotation · Automated backups · Alerting · Cron management

[Features](#-features) · [Architecture](#-architecture) · [Getting Started](#-getting-started) · [Development Guide](#-development-guide) · [Modules](#-project-modules) · [Contributing](#-contributing)

</div>

---

## 📖 Overview

LAOS is a self-hosted, production-ready Linux server observability system built from the ground up. It monitors your server's vital signs in real time, automates routine maintenance tasks, and delivers alerts before problems become outages.

This project is built as a full learning journey — from raw `/proc` filesystem reads all the way up to a live WebSocket-powered React dashboard — covering every layer of a real production system. Backend first, frontend later.

> **Learning Goal:** Understand every line of code running on your server. No black boxes.

---

## ✨ Features

| Category | Feature | Status |
|---|---|---|
| **Monitoring** | CPU usage, frequency, per-core stats | 🔄 In Progress |
| **Monitoring** | RAM, swap, memory pressure | 🔄 In Progress |
| **Monitoring** | Disk usage per partition, I/O rates | 🔄 In Progress |
| **Monitoring** | Network RX/TX throughput, connections | 🔄 In Progress |
| **Monitoring** | Process list, top consumers | 🔄 In Progress |
| **Automation** | Log rotation with configurable schedules | 📋 Planned |
| **Automation** | Automated backups via rsync | 📋 Planned |
| **Automation** | Cron job management (create/enable/disable) | 📋 Planned |
| **Alerting** | Threshold-based alert rules | 📋 Planned |
| **Alerting** | Email notifications via SMTP | 📋 Planned |
| **Alerting** | Slack webhook notifications | 📋 Planned |
| **Dashboard** | Real-time React UI via WebSocket | 📋 Planned |
| **Dashboard** | 90-day uptime history | 📋 Planned |
| **System** | Runs as a systemd service | 📋 Planned |
| **System** | HTTPS via Nginx reverse proxy | 📋 Planned |

> ✅ Done · 🔄 In Progress · 📋 Planned

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         LAOS System                             │
│                                                                  │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│   │    AGENT     │    │     API      │    │    UI (planned)  │  │
│   │              │    │              │    │                  │  │
│   │  collectors/ │───▶│  FastAPI     │◀──▶│  Next.js 14+     │  │
│   │  cpu.py      │    │  + WebSocket │    │  TypeScript      │  │
│   │  memory.py   │    │              │    │  (Module 11+)    │  │
│   │  disk.py     │    │  routes/     │    │                  │  │
│   │  network.py  │    │  metrics     │    └──────────────────┘  │
│   │              │    │  alerts      │                          │
│   │  automation/ │    │  cron        │                          │
│   │  logrotate   │    │  backups     │                          │
│   │  backup      │    │              │                          │
│   │  cron_mgr    │    │  database.py │                          │
│   │              │    │  models.py   │                          │
│   │  alerts/     │    │              │                          │
│   │  rules.py    │───▶│  SQLite DB   │                          │
│   │  notify.py   │    │  laos.db     │                          │
│   └──────────────┘    └──────────────┘                          │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐                                              │
│   │  Linux /proc │                                              │
│   │  Filesystem  │                                              │
│   │  (raw data)  │                                              │
│   └──────────────┘                                              │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
/proc/stat, /proc/meminfo          SQLite            WebSocket
/proc/net/dev, /proc/diskstats ──▶ laos.db ──▶ FastAPI ──▶ Next.js UI (planned M11)
        │                                         │
        │                                         ▼
   psutil library                          Alert Engine
   (Python wrapper)                      (email / Slack)
```

---

## 📁 Project Structure

```
laos/
│
├── agent/                          # Server-side data collection & automation
│   ├── __init__.py
│   ├── collectors/                 # Each file reads exactly ONE system metric
│   │   ├── __init__.py
│   │   ├── cpu.py                  # CPU usage, frequency, per-core data
│   │   ├── memory.py               # RAM, swap, memory pressure
│   │   ├── disk.py                 # Partition usage, I/O read/write rates
│   │   └── network.py             # RX/TX bytes, packets, active connections
│   │
│   ├── automation/                 # Scripts that perform maintenance actions
│   │   ├── __init__.py
│   │   ├── logrotate.py           # Wrapper around Linux logrotate
│   │   ├── backup.py              # rsync-based backup automation
│   │   └── cron_manager.py        # Read/write/toggle system crontab entries
│   │
│   └── alerts/                    # Threshold monitoring and notifications
│       ├── __init__.py
│       ├── rules.py               # Define and evaluate alert conditions
│       └── notify.py              # Send alerts via email and Slack
│
├── api/                           # HTTP + WebSocket server (FastAPI)
│   ├── __init__.py
│   ├── main.py                    # App entry point, registers all routes
│   ├── database.py                # SQLite connection, session management
│   ├── models.py                  # SQLAlchemy table definitions
│   └── routes/                   # One file per feature domain
│       ├── metrics.py             # GET /metrics, WS /ws
│       ├── alerts.py              # GET/POST /alerts
│       ├── cron.py                # GET/POST/DELETE /cron
│       └── backups.py             # GET/POST /backups
│
├── ui/                            # Next.js frontend dashboard (planned — Module 11+)
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   ├── hooks/                 # Custom React hooks (useWebSocket, etc.)
│   │   ├── pages/                 # Page-level components
│   │   └── App.jsx
│   └── package.json               # Not scaffolded yet
│
├── config/
│   └── settings.py                # All configuration loaded from .env
│
├── data/
│   ├── logs/                      # LAOS application logs
│   └── backups/                   # Backup files destination
│
├── tests/                         # Unit and integration tests
│   ├── test_collectors.py
│   ├── test_alerts.py
│   └── test_api.py
│
├── .env                           # ⚠ Secrets — NEVER commit to Git
├── .env.example                   # Safe template — commit this instead
├── .gitignore
├── requirements.txt               # Pinned Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Check |
|---|---|---|
| Python | 3.10+ | `python3 --version` |
| Git | Any | `git --version` |
| Linux | Any modern distro | `uname -r` |

> Node.js will be added to prerequisites when we reach Module 11 (Frontend).

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/laos.git
cd laos
```

**2. Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
# Your prompt will show (venv) — always activate before working
```

**3. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your actual values
nano .env
```

**5. Initialize the database**
```bash
python3 -c "from api.database import init_db; init_db()"
```

**6. Start the API server**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**7. Test the API is running**
```bash
curl http://localhost:8000/metrics/latest
```

> Frontend setup instructions will be added in Module 11 (Next.js).

---

## ⚙️ Configuration

All configuration lives in `.env`. Copy `.env.example` to get started:

```bash
# ── Server ────────────────────────────────────────
HOST=0.0.0.0
PORT=8000

# ── Collection ────────────────────────────────────
COLLECT_INTERVAL=5          # How often to read metrics (seconds)

# ── Alert Thresholds ──────────────────────────────
CPU_THRESHOLD=85.0          # Alert when CPU exceeds this %
RAM_THRESHOLD=85.0          # Alert when RAM exceeds this %
DISK_THRESHOLD=90.0         # Alert when any partition exceeds this %

# ── Email Alerts ──────────────────────────────────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=your_app_password   # Use App Password, not real password
ALERT_EMAIL=alerts@yourdomain.com

# ── Slack Alerts ──────────────────────────────────
SLACK_WEBHOOK=https://hooks.slack.com/services/...

# ── Backups ───────────────────────────────────────
BACKUP_DEST=data/backups
BACKUP_KEEP_DAYS=7
```

> ⚠️ **Security:** Never put real credentials in `.env.example`. That file is committed to Git. Only `.env` holds real secrets, and it is gitignored.

---

## 🧩 Project Modules

This project is built module by module. Each module has a clear goal, teaches specific concepts, and produces working, tested code.

### 🐍 Backend — Python + FastAPI

| # | Module | Concepts Taught | Status |
|---|---|---|---|
| 1 | Environment & Project Structure | venv, Git, project architecture, config patterns | ✅ Complete |
| 2 | The `/proc` Filesystem & psutil | Linux internals, metric collection, data types | 🔄 Current |
| 3 | SQLite — Storing Metrics | SQLAlchemy, schema design, time-series data | 📋 Upcoming |
| 4 | FastAPI — The API Layer | REST design, Pydantic models, dependency injection | 📋 Upcoming |
| 5 | WebSockets — Real-time Stream | Async Python, connection manager, live broadcasting | 📋 Upcoming |
| 6 | Log Rotation Automation | logrotate, subprocess, scheduled Python tasks | 📋 Upcoming |
| 7 | Backup System | rsync, file I/O, retention policy, cron trigger | 📋 Upcoming |
| 8 | Alert Engine | Rule evaluation engine, SMTP, Slack webhooks | 📋 Upcoming |
| 9 | Cron Job Manager | python-crontab, crontab syntax, API integration | 📋 Upcoming |
| 10 | systemd Service | Unit files, service management, auto-restart on boot | 📋 Upcoming |

### 🎨 Frontend — Next.js + TypeScript

| # | Module | Concepts Taught | Status |
|---|---|---|---|
| 11 | Next.js Project Setup | App Router, TypeScript, Tailwind CSS, project structure | 📋 Upcoming |
| 12 | Dashboard Layout & Design System | Components, layouts, theme tokens, reusable UI | 📋 Upcoming |
| 13 | Connecting to the API | fetch, SWR/React Query, API routes, error handling | 📋 Upcoming |
| 14 | Real-time WebSocket Client | useWebSocket hook, live metric state, reconnection logic | 📋 Upcoming |
| 15 | Charts & Data Visualisation | Recharts, time-series graphs, sparklines, gauges | 📋 Upcoming |
| 16 | Alerts, Cron & Backup UI | Forms, modals, optimistic updates, toast notifications | 📋 Upcoming |

### 🚀 Production

| # | Module | Concepts Taught | Status |
|---|---|---|---|
| 17 | Auth & Security | HTTP Basic Auth / JWT, middleware, protected routes | 📋 Upcoming |
| 18 | Nginx + HTTPS | Reverse proxy config, Let's Encrypt, SSL termination | 📋 Upcoming |
| 19 | Deployment & Final Polish | PM2 / systemd for Next.js, env per environment, go-live checklist | 📋 Upcoming |

---

## 📝 Development Guide

### Branch Strategy

```bash
main          # Always stable — only merge completed, tested modules
dev           # Active development branch
feat/module-2 # One branch per module or feature
fix/cpu-oob   # One branch per bug fix
```

```bash
# Starting a new module
git checkout -b feat/module-2-collectors

# When module is complete and tested
git checkout dev
git merge feat/module-2-collectors
git push origin dev

# When dev is stable and reviewed
git checkout main
git merge dev
```

### Code Style

```bash
# Format Python code (install once)
pip install black isort

# Run before every commit
black .
isort .
```

Python conventions used in this project:

```python
# ✅ Good — clear, typed, documented
def get_cpu_usage(interval: float = 1.0) -> dict:
    """
    Read current CPU usage statistics.

    Args:
        interval: Sampling interval in seconds. Higher = more accurate.

    Returns:
        dict with keys: percent, per_core, frequency_mhz, load_avg
    """
    ...

# ❌ Bad — no types, no docs, unclear name
def get_cpu(x):
    ...
```

---

## 🧪 Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run a specific module's tests
python3 -m pytest tests/test_collectors.py -v

# Run with coverage report
python3 -m pytest tests/ --cov=agent --cov-report=term-missing
```

---

## 📊 API Reference

Once the server is running, interactive docs are available at:

```
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
```

### Key Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/metrics/latest` | Latest snapshot of all metrics |
| `GET` | `/metrics/history?hours=1` | Historical metrics for charting |
| `WS` | `/ws` | WebSocket — real-time metric stream |
| `GET` | `/alerts` | All active alerts |
| `POST` | `/alerts/{id}/ack` | Acknowledge an alert |
| `GET` | `/cron` | List all cron jobs |
| `POST` | `/cron` | Create a new cron job |
| `PATCH` | `/cron/{name}/toggle` | Enable or disable a cron job |
| `GET` | `/backups` | List backup history |
| `POST` | `/backups/run` | Trigger a backup immediately |

---

## 🛡️ Security Notes

- All secrets stored in `.env` — never committed to Git
- `.env.example` contains only placeholder values
- API authentication added in Module 12
- HTTPS enforced in production via Nginx + Let's Encrypt
- Never run LAOS exposed to public internet without auth

---

## 🗺️ Roadmap

**Backend**
- [x] Module 01 — Project structure and configuration
- [ ] Module 02 — Metrics collection (CPU, RAM, disk, network)
- [ ] Module 03 — Time-series storage in SQLite
- [ ] Module 04 — REST API with FastAPI
- [ ] Module 05 — Real-time WebSocket stream
- [ ] Module 06 — Log rotation automation
- [ ] Module 07 — rsync backup system
- [ ] Module 08 — Alert engine with email + Slack
- [ ] Module 09 — Cron job manager
- [ ] Module 10 — systemd service deployment

**Frontend**
- [ ] Module 11 — Next.js + TypeScript project setup
- [ ] Module 12 — Dashboard layout and design system
- [ ] Module 13 — Connecting to the FastAPI backend
- [ ] Module 14 — Real-time WebSocket client
- [ ] Module 15 — Charts and data visualisation
- [ ] Module 16 — Alerts, Cron and Backup UI

**Production**
- [ ] Module 17 — Auth and security
- [ ] Module 18 — Nginx + HTTPS
- [ ] Module 19 — Deployment and final polish
- [ ] Docker container support *(stretch goal)*
- [ ] Multi-server support *(stretch goal)*

---

## 📚 Learning Resources

| Topic | Resource |
|---|---|
| Python `psutil` | https://psutil.readthedocs.io |
| FastAPI docs | https://fastapi.tiangolo.com |
| FastAPI WebSockets | https://fastapi.tiangolo.com/advanced/websockets |
| SQLAlchemy | https://docs.sqlalchemy.org |
| python-crontab | https://pypi.org/project/python-crontab |
| logrotate man page | `man logrotate` |
| Linux `/proc` filesystem | https://www.kernel.org/doc/html/latest/filesystems/proc.html |
| Next.js docs | https://nextjs.org/docs |
| Next.js App Router | https://nextjs.org/docs/app |
| TypeScript handbook | https://www.typescriptlang.org/docs/handbook/intro.html |
| Tailwind CSS | https://tailwindcss.com/docs |
| Recharts | https://recharts.org/en-US |
| SWR (data fetching) | https://swr.vercel.app |
| Conventional Commits spec | https://www.conventionalcommits.org |
| systemd unit files | https://systemd.io/WRITING_UNIT_FILES |
| Nginx reverse proxy | https://nginx.org/en/docs/beginners_guide.html |

---

## 🤝 Contributing

This is a learning project built step by step. To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Follow Conventional Commits format (`feat:`, `fix:`, `docs:`, etc.)
4. Write tests for new code
5. Open a Pull Request against `dev` — not `main`

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built from scratch · Fedora · Python 3.12 · FastAPI · Next.js (coming Module 11)

**Module 1 of 19 complete**

</div>