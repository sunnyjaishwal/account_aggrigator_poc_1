from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Form
from fastapi import UploadFile
from fastapi import File
from fastapi import Query
from fastapi import Body
from fastapi import Path
from fastapi import Cookie
from fastapi import Header
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    '''This is the root endpoint of the FastAPI application.
    It returns a simple HTML response with a welcome message.
    '''
    return HTMLResponse(content="<h1>Welcome to the FastAPI application!</h1>")

@app.get("/airlines")
def get_airlines():
    '''This endpoint returns a list of airlines.
    It is a simple GET request that returns a JSON response.
    '''
    airlines = [
        {"id": 1, "name": "American Airlines"},
        {"id": 2, "name": "Delta Airlines"},
        {"id": 3, "name": "United Airlines"},
    ]
    return airlines

Depends()
