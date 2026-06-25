# DevOps Dashboard

A lightweight container monitoring dashboard built to demonstrate core DevOps skills.

## 🖥 Demo

> Dashboard auto-refreshes every 10 seconds and displays all running Docker containers.

![Dashboard Screenshot](docs/screenshot.png)

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python / Flask | Web application |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| GitLab CI/CD | Automated pipeline (test → build → deploy) |
| GitLab Runner | Self-hosted CI executor |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |
| Kubernetes (minikube) | Container orchestration |
| kubectl | Kubernetes CLI |

## 🏗 Architecture
Git Push

│

▼

GitLab CI/CD Pipeline

├── test   → installs dependencies, checks imports

├── build  → builds Docker image

└── deploy → stops old container, runs new one

│

▼

DevOps Dashboard

(Flask + Docker SDK)

├── /          → Container list UI

├── /metrics   → Prometheus metrics

├── /api/containers → REST API

└── /health    → Health check

│

▼

Prometheus → Grafana

(scrapes /metrics every 15s)
## 🚀 Quick Start

**Requirements:** Docker, Docker Compose

```bash
git clone https://github.com/miha-creator/devops-dashboard.git
cd devops-dashboard
docker compose up --build
```

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:5001 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

Grafana login: `admin` / `admin`

## 📁 Project Structure
devops-dashboard/

├── app/

│   ├── app.py              # Flask application

│   └── requirements.txt    # Python dependencies

├── monitoring/

│   └── prometheus.yml      # Prometheus scrape config

├── Dockerfile              # Container image definition

├── docker-compose.yml      # Full stack setup

├── .gitlab-ci.yml          # CI/CD pipeline

└── README.md
## ⚙️ CI/CD Pipeline

Every `git push` triggers the pipeline:

1. **test** — verifies all dependencies install correctly
2. **build** — builds Docker image tagged with commit SHA
3. **deploy** — replaces running container with new image

## 📊 Metrics

Exposed at `/metrics` for Prometheus:

- `docker_containers_running` — number of running containers
- `docker_containers_total` — total containers
- `dashboard_requests_total` — total HTTP requests to dashboard

## 📌 What I Learned

- Setting up a self-hosted GitLab instance with Docker Compose
- Configuring and registering GitLab Runner
- Writing multi-stage CI/CD pipelines
- Using Docker SDK for Python to inspect containers at runtime
- Debugging Docker networking between containers
- Instrumenting a Flask app with Prometheus metrics
- Building Grafana dashboards from custom metrics

## ☸️ Kubernetes

Приложение задеплоено в локальный кластер minikube с 2 репликами.

### Запуск в Kubernetes

```bash
# Запустить кластер
minikube start --driver=docker

# Собрать образ внутри minikube
eval $(minikube docker-env)
docker build -f Dockerfile.k8s -t devops-dashboard-k8s:latest .

# Задеплоить
kubectl apply -f k8s/

# Открыть в браузере
minikube service devops-dashboard --url
```

### Полезные команды

```bash
kubectl get pods                          # список подов
kubectl get services                      # список сервисов
kubectl logs <pod-name>                   # логи пода
kubectl delete pod <pod-name>             # удалить под (k8s пересоздаст автоматически)
kubectl scale deployment devops-dashboard --replicas=3  # масштабирование
```

### Что демонстрирует

- Deployment с 2 репликами
- Self-healing — при удалении пода k8s автоматически создаёт новый
- NodePort Service для доступа извне кластера
- Передача переменных окружения через Downward API (имя пода, namespace)
