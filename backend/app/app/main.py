from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette_prometheus import PrometheusMiddleware, metrics

from app.api.api_v1.api import api_router
from app.core import config
from app.db.session import Session


def init_app():
    app_ = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")

    # CORS
    origins = []

    # Set all CORS enabled origins
    if config.BACKEND_CORS_ORIGINS:
        origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
        for origin in origins_raw:
            use_origin = origin.strip()
            origins.append(use_origin)
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        app_.add_middleware(PrometheusMiddleware)

    api_router.add_route("/metrics/", metrics)
    app_.include_router(api_router, prefix=config.API_V1_STR)
    return app_


app = init_app()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response
