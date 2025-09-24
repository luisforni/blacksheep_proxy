import argparse
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=False)

def parse_args():
    parser = argparse.ArgumentParser(description="Run BlackSheep proxy server.")
    parser.add_argument("--host", default="0.0.0.0", help="Host bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port (default: 8080)")
    parser.add_argument("--reload", action="store_true", help="Enable autoreload (dev)")
    parser.add_argument("--log-level", default="info", help="Log level (debug, info, warning, error)")
    parser.add_argument("--proxy-headers", action="store_true", help="Respect X-Forwarded-* headers")
    return parser.parse_args()

def main():
    args = parse_args()
    app_path = "app.main:app"
    uvicorn.run(
        app_path,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
        proxy_headers=args.proxy_headers,
    )

if __name__ == "__main__":
    main()
