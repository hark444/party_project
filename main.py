from fastapi import FastAPI
from app.api import api_router
from logging.config import dictConfig
from app.logger import log_config
from fastapi.middleware.cors import CORSMiddleware

dictConfig(log_config)

application = FastAPI()

origins = [
    "http://localhost:3000",
]


application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application.include_router(api_router)
