# blacksheep_proxy

Es una API Proxy con autenticación en BlackSheep que se interpone entre el frontend y el o los backends. Incluye JWT, forwarding de rutas, CORS, rate-limit básico, reintentos al upstream y passthrough de cabeceras seguras.

Crear fichero `.env` en la raiz del directorio.

```bash
# === App ===
APP_NAME=proxy-gw
DEBUG=true

# === JWT ===
JWT_SECRET=super_secret_change_me
JWT_EXPIRES_MIN=60

# === Upstream (backend real) ===
UPSTREAM_BASE_URL=http://127.0.0.1:8000
FORWARD_AUTHORIZATION=true
TIMEOUT_SECONDS=15
RETRY_ATTEMPTS=2
RETRY_BACKOFF=0.25

# === CORS ===
CORS_ALLOW_ORIGINS=*
CORS_ALLOW_HEADERS=*
CORS_ALLOW_METHODS=*
```

## Instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install --upgrade pip       # Windows: python -m pip install --upgrade pip 
pip install -r requirements.txt
```

---

## Correr el proxy

```bash
python server.py --reload
```

---

## Correr el docker

```bash
docker build -t blacksheep-proxy:0.1.0 .

docker run --name blacksheep_proxy \
  --env-file .env \
  -p 8080:8080 \
  blacksheep-proxy:0.1.0
```

Si el upstream no está en Docker, cambiar en .env:

```bash
UPSTREAM_BASE_URL=http://host.docker.internal:8000
```

---

## Probar

Crear backend de pruebas.

```bash
cd example_backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install fastapi uvicorn     # Windows: python -m pip install --upgrade pip
uvicorn main:app --port 8000
```

Ejecutar.

```bash
# Obtener token
curl -s -X POST http://localhost:8080/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@example.com","password":"admin123"}'

# Usar el token (reemplaza XXX por el access_token devuelto)
curl -H "Authorization: Bearer XXX" http://localhost:8080/api/health
```
