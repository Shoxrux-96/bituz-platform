from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import auth


app = FastAPI(
    title="Bituz Platform API",
    version="1.0.0",
    description="API for Bituz Platform"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth.route)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Bituz Platform API"}

