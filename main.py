from fastapi import FastAPI
from app.api import api_router
from fastapi.middleware.cors import CORSMiddleware


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
