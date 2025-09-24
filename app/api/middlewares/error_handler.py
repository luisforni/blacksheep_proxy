from blacksheep import Request
from blacksheep.server.responses import json
import httpx
import logging

logger = logging.getLogger("proxy")

async def error_middleware(request: Request, handler):
    try:
        return await handler(request)
    except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout) as ex:
        logger.exception("Upstream connection/timeout error")
        return json({"error": "Bad Gateway", "detail": str(ex)}, status=502)
    except httpx.HTTPError as ex:
        logger.exception("Upstream HTTP error")
        return json({"error": "Bad Gateway", "detail": str(ex)}, status=502)
    except Exception:
        logger.exception("Unhandled error")
        return json({"error": "Internal Server Error"}, status=500)

