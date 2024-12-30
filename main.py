from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware  # Importing directly from Starlette
import uvicorn
from apps.calculator.route import router as calculator_router
from constants import SERVER_URL, PORT, ENV

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

origins = [
    "https://ipad-calc-fe.vercel.app",  # Frontend origin 1
    "https://ipad-calc-9qjk71gtw-vis-projects-82c0f63d.vercel.app",  # Frontend origin 2
]

app = FastAPI(lifespan=lifespan)

# Adding CORSMiddleware for CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Only allow the listed origins
    allow_credentials=True,  # Allow credentials (cookies, HTTP authentication)
    allow_methods=["*"],  # Allow only GET and POST methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers to the frontend
)

@app.get("/")
async def health():
    return {"message": "Server is running"}

# Include the calculator route with the prefix
app.include_router(calculator_router, prefix="/calculate", tags=["calculate"])

if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_URL, port=int(PORT), reload=(ENV == "dev"))
