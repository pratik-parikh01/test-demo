# Demo Microservices

Two microservices that communicate over a shared Docker network:

| Service | Language | Port | Responsibility |
|---------|----------|------|----------------|
| `python-service` | Python / Flask | 5001 | Users |
| `node-service` | Node.js / Express | 3000 | Products |

The users service calls the products service when you hit `/users/:id/products`, demonstrating inter-service communication inside Docker Compose.

---

## Project layout

```
demo/
├── docker-compose.yml
├── python-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── node-service/
    ├── app.js
    ├── package.json
    └── Dockerfile
```

---

## Running with Docker Compose

```bash
# Build images and start both services in the background
docker compose up --build -d

# Tail logs (Ctrl-C to stop tailing, containers keep running)
docker compose logs -f

# Stop and remove containers
docker compose down
```

Both services are ready when `docker compose ps` shows them as `running (healthy)`.

---

## API reference

### Users service — `http://localhost:5001`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/users` | List all users |
| GET | `/users/:id` | Get a single user |
| GET | `/users/:id/products` | Get a user with their products (calls node-service) |

### Products service — `http://localhost:3000`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/products` | List all products |
| GET | `/products?owner_id=:id` | Filter products by owner |
| GET | `/products/:id` | Get a single product |

---

## Quick smoke-test

```bash
# Health checks
curl http://localhost:5001/health
curl http://localhost:3000/health

# List resources
curl http://localhost:5001/users
curl http://localhost:3000/products

# Cross-service call: user 1 with their products
curl http://localhost:5001/users/1/products
```

---

## Running services individually (without Docker)

**Python service**

```bash
cd python-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PRODUCTS_SERVICE_URL=http://localhost:3000 flask run --port 5001
```

**Node service**

```bash
cd node-service
npm install
node app.js
```
# test-demo
# test-demo
