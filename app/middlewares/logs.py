import http
import math
import time

from fastapi import Request, Response, status
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import Message

from app.depends import provider
from app.log import log

DISABLED_ROUTES = ["/metrics", "/docs", "/openapi.json", "/favicon.ico", "/ping"]


class LoggingMiddleware:
    @staticmethod
    async def get_protocol(request: Request) -> str:
        protocol = str(request.scope.get("type", ""))
        http_version = str(request.scope.get("http_version", ""))
        return f"{protocol.upper()}/{http_version}"

    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        async def receive() -> Message:
            return {"type": "http.request", "body": body}

        request._receive = receive  # noqa: SLF001

    def _get_client_ip(self, request: Request) -> str:
        if request.headers.get("X-Forwarded-For"):
            ips = request.headers["X-Forwarded-For"].split(",")
            return ips[0].strip()

        if request.headers.get("X-Real-IP"):
            return request.headers["X-Real-IP"]

        if request.client:
            return request.client.host
        return "unknown"

    async def get_body(self, request: Request) -> bytes:
        body = await request.body()
        await self.set_body(request, body)
        return body

    async def __call__(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ):
        start_time = time.time()
        exception_object = None
        try:
            response = await call_next(request)
        except Exception as ex:  # noqa: BLE001
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = ex
            response_headers = {}
        else:
            response_headers = dict(response.headers.items())
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        if any(e in request.url.path for e in DISABLED_ROUTES):
            return response

        duration: int = math.ceil((time.time() - start_time) * 1000)
        if exception_object:
            level = "ERROR"
        elif response.status_code >= status.HTTP_400_BAD_REQUEST:
            level = "WARN"
        else:
            level = "INFO"
        cu = provider.current_user
        log(
            level=level,
            method=request.method,
            path=request.url.path,
            ip=self._get_client_ip(request),
            status=response.status_code,
            size=int(response_headers.get("content-length", 0)),
            duration=duration,
            exception=exception_object,
            raw_detail=response_body.decode(errors="ignore"),
            user=cu.to_dict() if cu else None,
        )
        provider.set_current_user(user=None)
        return response
