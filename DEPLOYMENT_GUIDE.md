# BHASHAAI – PRODUCTION DEPLOYMENT GUIDE

---

## 1. Production Architecture Overview

In a production environment, BhashaAI separates the presentation tier, API application tier, deep learning inference engine, and persistent storage layers to ensure horizontal scalability, fault tolerance, and security.

```
                    ┌─────────────────────────┐
                    │      Client Browser     │
                    └────────────┬────────────┘
                                 │ HTTPS / WSS
                                 ▼
                    ┌─────────────────────────┐
                    │      Cloudflare CDN     │
                    │   (Edge SSL / Caching)  │
                    └────────────┬────────────┘
                                 │
            ┌────────────────────┴────────────────────┐
            ▼                                         ▼
┌─────────────────────────┐               ┌─────────────────────────┐
│     Frontend (Vercel)   │               │   NGINX Reverse Proxy   │
│   React + Vite SPA dist │               │    (Port 80 / 443 SSL)  │
└─────────────────────────┘               └───────────┬─────────────┘
                                                      │ Reverse Proxy
                                                      ▼
                                          ┌─────────────────────────┐
                                          │   Gunicorn + Uvicorn    │
                                          │     FastAPI Workers     │
                                          └───────┬──────────┬──────┘
                                                  │          │
                                 ┌────────────────┘          └───────────────┐
                                 ▼                                           ▼
                    ┌─────────────────────────┐                 ┌─────────────────────────┐
                    │ Managed PostgreSQL 18   │                 │ S3 / Cloudflare R2      │
                    │   (AWS RDS / Supabase)  │                 │ Audio Object Storage    │
                    └─────────────────────────┘                 └─────────────────────────┘
```

---

## 2. Frontend Deployment (Vercel / Netlify / Static CDN)

The frontend is a static Single Page Application (SPA) built using Vite and React.

### Step 2.1: Production Build Configuration
1. In `frontend/`, configure the production API base URL via `.env.production`:
   ```ini
   VITE_API_BASE_URL="https://api.bhashaai.example.com"
   ```
2. Run the production build command:
   ```bash
   cd frontend
   npm run build
   ```
   This generates the compiled bundle in `frontend/dist/`.

### Step 2.2: Deploying to Vercel
1. Install the Vercel CLI:
   ```bash
   npm i -g vercel
   ```
2. Deploy the frontend:
   ```bash
   cd frontend
   vercel --prod
   ```
3. In the Vercel Project Settings:
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Environment Variables:** Set `VITE_API_BASE_URL` to your production backend domain.
4. Configure SPA client-side routing in `vercel.json`:
   ```json
   {
     "rewrites": [
       { "source": "/(.*)", "destination": "/index.html" }
     ]
   }
   ```

---

## 3. Backend Deployment (Docker & Gunicorn + Uvicorn)

### Step 3.1: Production Dockerfile
Create a production `Dockerfile` in the repository root:

```dockerfile
FROM python:3.11-slim

# Install system audio dependencies and FFmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code, ML modules, and migrations
COPY backend /app/backend
COPY ml /app/ml
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY pyproject.toml /app/pyproject.toml

# Create audio storage directories
RUN mkdir -p /app/storage/audio/uploads /app/storage/audio/generated

EXPOSE 8000

# Start Gunicorn with Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "--bind", "0.0.0.0:8000", "--timeout", "120", "backend.app.main:app"]
```

### Step 3.2: Systemd Service (Bare-Metal / Virtual Private Server)
If deploying on an Ubuntu Linux VPS without Docker:

1. Create `/etc/systemd/system/bhashaai.service`:
   ```ini
   [Unit]
   Description=BhashaAI FastAPI ASGI Application
   After=network.target postgresql.service

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/opt/bhashaai
   EnvironmentFile=/opt/bhashaai/.env
   ExecStart=/opt/bhashaai/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 2 --bind 127.0.0.1:8000 --timeout 120 backend.app.main:app
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```
2. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable bhashaai
   sudo systemctl start bhashaai
   ```

---

## 4. Production Database Configuration (PostgreSQL 18)

1. Provision a managed PostgreSQL instance (e.g., AWS RDS, Supabase, Neon, or local PostgreSQL 18 server).
2. Configure environment credentials in `.env`:
   ```ini
   DATABASE_URL="postgresql+asyncpg://bhasha_admin:SecurePassword123!@db.example.com:5432/bhashaai"
   SYNC_DATABASE_URL="postgresql://bhasha_admin:SecurePassword123!@db.example.com:5432/bhashaai"
   ```
3. Run Alembic migrations against production database:
   ```bash
   alembic upgrade head
   ```
4. Verify database indices and connectivity:
   ```bash
   psql -h db.example.com -U bhasha_admin -d bhashaai -c "\dt"
   ```

---

## 5. Reverse Proxy & SSL Configuration (NGINX + Let's Encrypt)

Configure NGINX on your host server to terminate SSL and proxy traffic to Gunicorn/FastAPI:

```nginx
server {
    server_name api.bhashaai.example.com;

    client_max_body_size 25M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support for future streaming translation
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Audio stream timeouts
        proxy_read_timeout 120s;
        proxy_send_timeout 120s;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/api.bhashaai.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.bhashaai.example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
```

Obtain free SSL certificates via Certbot:
```bash
sudo certbot --nginx -d api.bhashaai.example.com
```

---

## 6. Security Hardening & CORS Checklist

- **Environment Secrets:** Generate a cryptographically strong 256-bit secret key for JWT signing:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- **CORS Whitelist:** Update `BACKEND_CORS_ORIGINS` in `.env` to include only verified production domains:
  ```ini
  BACKEND_CORS_ORIGINS='["https://bhashaai.example.com", "https://bhashaai.vercel.app"]'
  ```
- **Upload Restrictions:** Enforce strict file size verification (`MAX_UPLOAD_SIZE_MB=25`) and binary magic-byte validation to prevent arbitrary file upload vulnerabilities.
- **Rate Limiting:** Implement API rate-limiting via NGINX `limit_req_zone` (e.g., 20 requests per minute per IP) to guard against denial-of-service attempts.

---

## 7. Monitoring, Health Checks & Telemetry

- **Health Endpoint:** Query `GET https://api.bhashaai.example.com/health` to verify application uptime, database responsiveness, and model registry availability.
- **Process Monitoring:** Monitor Gunicorn CPU and RAM utilization using `htop` or Prometheus node-exporter to ensure memory consumption stays within the provisioned host thresholds.
