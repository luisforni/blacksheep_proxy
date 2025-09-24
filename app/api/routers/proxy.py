from urllib.parse import urlsplit
from blacksheep import Request, Response
from app.core.di import container
from app.core.config import settings
from app.core.security import decode_token

SAFE_HOP_HEADERS_REQ = {
    b"host", b"connection", b"keep-alive", b"proxy-authenticate",
    b"proxy-authorization", b"te", b"trailers", b"transfer-encoding", b"upgrade",
}

SAFE_HOP_HEADERS_RESP = {
    b"connection", b"keep-alive", b"proxy-authenticate", b"proxy-authorization",
    b"te", b"trailers", b"transfer-encoding", b"upgrade", b"content-length",
}

WHITELIST_RESP = {
    b"content-type", b"cache-control", b"etag", b"last-modified",
    b"set-cookie", b"location", b"vary", b"content-encoding", b"date",
}

def _extract_user_sub_from_auth(request: Request) -> str | None:
    auth = request.headers.get_first(b"authorization")
    if not auth:
        return None
    try:
        token = auth.decode().split(" ", 1)[1].strip()
        claims = decode_token(token)
        return str(claims.get("sub")) if claims and "sub" in claims else None
    except Exception:
        return None

def _filtered_request_headers(req: Request) -> dict[bytes, bytes]:
    headers = {k: v for k, v in req.headers.items() if k.lower() not in SAFE_HOP_HEADERS_REQ}
    if not settings.FORWARD_AUTHORIZATION and b"authorization" in headers:
        headers.pop(b"authorization", None)
    sub = _extract_user_sub_from_auth(req)
    if sub:
        headers[b"x-user-sub"] = sub.encode()
    return headers

def register_proxy_routes(app):
    @app.router.route("/api/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE","HEAD"])
    async def proxy_any(request: Request, path: str):
        headers = _filtered_request_headers(request)
        body = await request.read()
        method = request.method
        from urllib.parse import urlsplit
        full_url = str(request.url)
        qs = urlsplit(full_url).query
        query = qs if qs else None
        resp = await container.upstream.request(
            method=method,
            path="/" + path,
            headers=headers,
            query=query,
            body=body,
        )
        raw_headers = getattr(resp.headers, "raw", None)
        SAFE_HOP_HEADERS_RESP = {
            b"connection", b"keep-alive", b"proxy-authenticate", b"proxy-authorization",
            b"te", b"trailers", b"transfer-encoding", b"upgrade", b"content-length",
        }
        if raw_headers is not None:
            out_headers = [(k, v) for (k, v) in raw_headers if k.lower() not in SAFE_HOP_HEADERS_RESP]
        else:
            out_headers = [
                (k.encode(), v.encode())
                for (k, v) in resp.headers.items()
                if k.lower().encode() not in SAFE_HOP_HEADERS_RESP
            ]
        out_headers = [(k, v) for (k, v) in out_headers if k.lower() != b"content-type"]
        content_type = None
        if raw_headers is not None:
            for k, v in raw_headers:
                if k.lower() == b"content-type":
                    content_type = v.decode(errors="replace")
                    break
        else:
            ct = resp.headers.get("content-type")
            if ct:
                content_type = str(ct)
        raw_headers = getattr(resp.headers, "raw", None)
        SAFE_HOP_HEADERS_RESP = {
            b"connection", b"keep-alive", b"proxy-authenticate", b"proxy-authorization",
            b"te", b"trailers", b"transfer-encoding", b"upgrade", b"content-length",
        }
        if raw_headers is not None:
            out_headers = [(k, v) for (k, v) in raw_headers if k.lower() not in SAFE_HOP_HEADERS_RESP]
        else:
            out_headers = [
                (k.encode(), v.encode())
                for (k, v) in resp.headers.items()
                if k.lower().encode() not in SAFE_HOP_HEADERS_RESP
            ]
        out_headers = [(k, v) for (k, v) in out_headers if k.lower() != b"content-type"]
        content_type = None
        if raw_headers is not None:
            for k, v in raw_headers:
                if k.lower() == b"content-type":
                    content_type = v.decode(errors="replace")
                    break
        else:
            ct = resp.headers.get("content-type")
            if ct:
                content_type = str(ct)
        raw_body = getattr(resp, "content", None)
        if raw_body is None:
            body_bytes = b""
        elif isinstance(raw_body, (bytes, bytearray, memoryview)):
            body_bytes = bytes(raw_body)
        elif isinstance(raw_body, str):
            enc = getattr(resp, "encoding", None) or "utf-8"
            body_bytes = raw_body.encode(enc, errors="replace")
        else:
            body_bytes = str(raw_body).encode("utf-8", errors="replace")
        bs_response = Response(resp.status_code)
        for k, v in out_headers:
            bs_response.add_header(k, v)
        if content_type:
            bs_response.add_header(b"content-type", content_type.encode("utf-8", errors="replace"))
        bs_response.body = body_bytes
        return bs_response

