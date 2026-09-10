# auth-service

A centralized authentication microservice built with FastAPI.

## Structure

app/core: configuration and security utilities. app/db: database session and connection setup. app/endpoints: API route handlers. app/models: ORM models. app/schemas: Pydantic request/response schemas. app/main.py: application entrypoint.

## Setup

Install dependencies with `pip install -r requirements.txt`, then run `uvicorn app.main:app --reload`.

## Status

Early-stage project. Core auth flows are implemented; tests and CI are not yet set up.
