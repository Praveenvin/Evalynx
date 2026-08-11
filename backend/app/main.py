from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from app.api.resume_screening import (
    router as resume_screening_router,
)

from app.api.mock_interview import (
    router as mock_interview_router,
)

from app.api.course_recommendation import (
    router as course_recommendation_router,
)

app = FastAPI(
    title="Evalynx API",
    description=(
        "AI-powered resume screening and mock interview platform"
    ),
    version="1.0.0",
)


# -------------------------------------------------------------------
# CORS
# -------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------
# API Routers
# -------------------------------------------------------------------

app.include_router(
    resume_screening_router
)

app.include_router(
    mock_interview_router
)

app.include_router(
    course_recommendation_router
)


# -------------------------------------------------------------------
# Root
# -------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Evalynx API is running"
    }


# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -------------------------------------------------------------------
# Custom OpenAPI
#
# FastAPI 0.141+ can describe UploadFile arrays as:
# string + contentMediaType=application/octet-stream.
#
# We convert those items to:
# string + format=binary
#
# This makes Swagger UI display the actual file upload control.
# -------------------------------------------------------------------

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Evalynx API",
        version="1.0.0",
        description=(
            "AI-powered resume screening and mock interview platform."
        ),
        routes=app.routes,
    )

    schemas = (
        openapi_schema
        .get("components", {})
        .get("schemas", {})
    )

    for schema in schemas.values():

        properties = schema.get(
            "properties",
            {},
        )

        for property_schema in properties.values():

            if property_schema.get("type") != "array":
                continue

            items = property_schema.get(
                "items",
                {},
            )

            if (
                items.get("type") == "string"
                and items.get("contentMediaType")
                == "application/octet-stream"
            ):

                items.pop(
                    "contentMediaType",
                    None,
                )

                items["format"] = "binary"

    openapi_schema["openapi"] = "3.0.3"

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi