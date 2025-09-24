from app.core.config import settings
from app.infrastructure.http.upstream_client import UpstreamClient

class Container:
    def __init__(self):
        self.settings = settings
        self.upstream = UpstreamClient(
            base_url=str(settings.UPSTREAM_BASE_URL),
            timeout=settings.TIMEOUT_SECONDS,
            retry_attempts=settings.RETRY_ATTEMPTS,
            retry_backoff=settings.RETRY_BACKOFF,
        )

container = Container()
