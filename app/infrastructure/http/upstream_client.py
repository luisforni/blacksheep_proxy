import asyncio
from typing import Mapping
import httpx

class UpstreamClient:
    def __init__(self, base_url: str, timeout: float, retry_attempts: int, retry_backoff: float):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.retry_backoff = retry_backoff
        self._client = httpx.AsyncClient(
            timeout=timeout,
            base_url=self.base_url,
            follow_redirects=True,
        )

    async def request(
        self,
        method: str,
        path: str,
        headers: Mapping[bytes, bytes],
        query: str | bytes | None,
        body: bytes | None,
    ):
        attempt = 0
        last_exc: Exception | None = None

        url = path if path.startswith("/") else f"/{path}"
        if query:
            query_str = query.decode() if isinstance(query, bytes) else str(query)
            url = f"{url}?{query_str}"

        while attempt <= self.retry_attempts:
            try:
                resp = await self._client.request(
                    method=method,
                    url=url,
                    headers={k.decode(): v.decode() for k, v in headers.items()},
                    content=body,
                )
                return resp
            except Exception as ex:
                last_exc = ex
                await asyncio.sleep(self.retry_backoff * (2 ** attempt))
                attempt += 1

        raise last_exc

    async def aclose(self):
        await self._client.aclose()
