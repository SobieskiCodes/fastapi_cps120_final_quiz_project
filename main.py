import json
import pathlib
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    with open(BASE_DIR / "questions.json", "r") as file:
        quiz_data = json.load(file)

    #print(quiz_data)
    context = {
        "request": request,
        "title": "Multiple Choice Quiz",
        "quiz": quiz_data["quiz"]
    }
    response = templates.TemplateResponse("index.html", context)
    return response
