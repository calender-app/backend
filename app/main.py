from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .apis import events
from fastapi.exceptions import RequestValidationError
import logging

from .middlewares.errorHandler import validation_error_handler
from .middlewares.tokenAuth import check_bearer_token

app = FastAPI()
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Middleware to check for a bearer token


# apply basic middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# apply validation_error_handler middleware
app.add_exception_handler(RequestValidationError, validation_error_handler)

# apply the token auth middleware

# Register routes
# app.middleware("http")(check_bearer_token)

app.include_router(events.router)
