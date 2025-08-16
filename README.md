# python-services 🚀

## Overview

**python-services** is a microservices-based project built with FastAPI, focusing on modular service architecture for handling user management, order processing, and stock inventory. Each service is independently deployable, communicates via HTTP, and maintains its own database. The project is suitable for learning, prototyping, or as a base for scalable solutions in e-commerce, logistics, or similar domains. 🛒📦👤

## Folder Structure

```
python-services/
├── order_service/
│   ├── app/
│   │   ├── api/             # API routes for order operations
│   │   ├── config/          # Database config (SQLAlchemy)
│   │   ├── middleware/      # Logger and other middlewares
│   │   ├── model/           # Order ORM models
│   │   ├── schema/          # Pydantic schemas for orders
│   │   ├── service/         # Core business logic (order management)
│   │   └── util/            # Remote calls, logging, etc.
│   └── main.py              # FastAPI entrypoint
│
├── user_service/
│   ├── app/
│   │   ├── api/             # API routes for user/auth
│   │   ├── config/          # Database config
│   │   ├── middleware/      # Logger/auth middlewares
│   │   ├── models/          # User ORM models
│   │   ├── schemas/         # Schemas for user data
│   │   ├── service/         # User and auth business logic
│   │   └── utils/           # Logging
│   └── main.py              # FastAPI entrypoint
│
├── stock-service/
│   ├── app/
│   │   ├── api/             # Stock API routes
│   │   ├── config/          # Database config
│   │   ├── middleware/      # Logger middlewares
│   │   └── util/            # Logging
│   └── main.py              # FastAPI entrypoint
│
└── README.md                # Project documentation
```

## Services

- **User Service 👤**: Handles user registration, authentication, login/logout, and manages user data.
- **Order Service 🛒**: Allows users to create and manage orders. Integrates with stock-service to check and decrease inventory.
- **Stock Service 📦**: Manages stock levels. Provides APIs for checking availability and updating inventory.

## Docker & Deployment 🐳

Each service includes a `Dockerfile` for containerization, ensuring isolated environments and reproducible builds. The Docker setup uses multi-stage builds for efficiency and security:

- **Builder stage**: Installs Python dependencies.
- **Runtime stage**: Copies the app code and sets up a FastAPI server with an unprivileged user.

To build and run a service (example for `user_service`):

```sh
docker build -t user_service ./user_service
docker run -p 8000:8000 user_service
```

Each service exposes a `/healthz` endpoint for health checks, making them suitable for orchestration (Docker Compose, Kubernetes, etc.). ✅

## Technologies Used

- **Python 3.12 🐍**
- **FastAPI ⚡** (web framework)
- **SQLAlchemy** (ORM/database layer)
- **httpx** (async HTTP client for service-to-service calls)
- **Docker** (containerization)

## Getting Started

1. Clone the repository:
    ```sh
    git clone https://github.com/FoxerBN/python-services.git
    cd python-services
    ```
2. Build and run each service using Docker as shown above, or run locally with Python and install dependencies from `requirements.txt` in each service directory.

## How Services Communicate

- Services communicate via RESTful APIs. 🔗
- Example: When creating an order, `order_service` calls `stock-service` to verify inventory and decrease stock.

## Health and Logging

- Each service uses logging (see `util/logger.py` in each service). 📄
- Health endpoints (`/healthz`) are provided for monitoring. 🩺

## License

This project is provided for educational and prototyping purposes. Please check with the repository owner for licensing details. 😊
