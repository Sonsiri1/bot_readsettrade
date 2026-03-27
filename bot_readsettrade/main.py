from fastapi import FastAPI
from api.analysts_api import router as analysts_router
from api.auth_api import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysts_router, prefix="/api", tags=["Stocks"])
app.include_router(auth_router, prefix="/api", tags=["Auth"])