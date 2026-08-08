from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.api.resume_screening import (
    router as resume_screening_router,
)


app = FastAPI(
    title="Evalynx API",
    description=(
        "AI-powered resume screening and mock interview platform"
    ),
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    resume_screening_router
)


@app.get("/")
def root():
    return {
        "message": "Evalynx API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


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

    schemas = openapi_schema.get(
        "components",
        {},
    ).get(
        "schemas",
        {},
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