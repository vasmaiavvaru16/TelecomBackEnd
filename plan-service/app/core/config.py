"""
File with environment variables and general configuration logic.
`SECRET_KEY`, `ENVIRONMENT` etc. map to env variables with the same names.

Pydantic priority ordering:

1. (Most important, will overwrite everything) - environment variables
2. `.env` file in root folder of project
3. Default values

For project name, version, description we use pyproject.toml
For the rest, we use file `.env` (gitignored), see `.env.example`

`DEFAULT_SQLALCHEMY_DATABASE_URI` and `TEST_SQLALCHEMY_DATABASE_URI`:
Both are ment to be validated at the runtime, do not change unless you know
what are you doing. All the two validators do is to build full URI (TCP protocol)
to databases to avoid typo bugs.

See https://pydantic-docs.helpmanual.io/usage/settings/

Note, complex types like lists are read as json-encoded strings.
"""

from pathlib import Path
from typing import Literal

import tomli
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

PROJECT_DIR = Path(__file__).parent.parent.parent
with open(f"{PROJECT_DIR}/pyproject.toml", "rb") as f:
    PYPROJECT_CONTENT = tomli.load(f)["tool"]["poetry"]


class Settings(BaseSettings):
    # CORE SETTINGS
    ENVIRONMENT: Literal["DEV", "PYTEST", "STG", "PROD"] = "DEV"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
    BACKEND_PORT: int = 8001

    # PROJECT NAME, VERSION AND DESCRIPTION
    PROJECT_NAME: str = PYPROJECT_CONTENT["name"]
    VERSION: str = PYPROJECT_CONTENT["version"]
    DESCRIPTION: str = PYPROJECT_CONTENT["description"]

    # POSTGRESQL DEFAULT DATABASE
    DEFAULT_DATABASE_HOSTNAME: str
    DEFAULT_DATABASE_USER: str
    DEFAULT_DATABASE_PASSWORD: str
    DEFAULT_DATABASE_PORT: str = "3306"
    DEFAULT_DATABASE_DB: str
    DEFAULT_SQLALCHEMY_DATABASE_URI: str = ""

    # POSTGRESQL TEST DATABASE
    TEST_DATABASE_HOSTNAME: str
    TEST_DATABASE_USER: str
    TEST_DATABASE_PASSWORD: str
    TEST_DATABASE_PORT: str
    TEST_DATABASE_DB: str
    TEST_SQLALCHEMY_DATABASE_URI: str = ""

    @validator("DEFAULT_SQLALCHEMY_DATABASE_URI")
    def _assemble_default_db_connection(cls, v: str, values: dict[str, str]) -> str:
        return PostgresDsn.build(
            scheme="mysql+asyncmy",
            user=values["DEFAULT_DATABASE_USER"],
            password=values["DEFAULT_DATABASE_PASSWORD"],
            host=values["DEFAULT_DATABASE_HOSTNAME"],
            port=values["DEFAULT_DATABASE_PORT"],
            path=f"/{values['DEFAULT_DATABASE_DB']}",
        )

    @validator("TEST_SQLALCHEMY_DATABASE_URI")
    def _assemble_test_db_connection(cls, v: str, values: dict[str, str]) -> str:
        return PostgresDsn.build(
            scheme="mysql+asyncmy",
            user=values["TEST_DATABASE_USER"],
            password=values["TEST_DATABASE_PASSWORD"],
            host=values["TEST_DATABASE_HOSTNAME"],
            port=values["TEST_DATABASE_PORT"],
            path=f"/{values['TEST_DATABASE_DB']}",
        )

    class Config:
        env_file = f"{PROJECT_DIR}/.env"
        case_sensitive = True


settings: Settings = Settings()  # type: ignore
