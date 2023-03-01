from pydantic import BaseSettings
from .base import env


class ApiSettings(BaseSettings):
    OPT_IN_LINK = env.str("OPT_IN_LINK")


api_settings = ApiSettings()
