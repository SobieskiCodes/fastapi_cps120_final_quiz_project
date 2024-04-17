#===========================================================
#
#  Title:       Multiple Choice Quiz
#  Author(s):   Marshall Blaser, Gloria Yarandi, Kasey Garant, Justin Sobieski
#  Date:        4/15/2024
#  Description:
#       A quick example of how to make a multiple choice quiz
#       using FastAPI and Jinja2Templates with python.
#===========================================================
import json
import pathlib
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from random import shuffle
import uvicorn


app = FastAPI()
BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    with open(BASE_DIR / "questions.json", "r") as question_file:
        quiz_data = json.load(question_file)

    for question in quiz_data["quiz"]:
        shuffle(question["options"])

    context = {
        "request": request,
        "title": "Multiple Choice Quiz",
        "quiz": quiz_data["quiz"]
    }

    response = templates.TemplateResponse("index.html", context)
    return response


@app.post('/submit_quiz', response_class=HTMLResponse)
async def submit_quiz(request: Request):
    form_data = await request.form()
    user_answers = dict(form_data)

    with open(BASE_DIR / "questions.json", "r") as question_file:
        quiz_data = json.load(question_file)

    score = 0
    for question in quiz_data["quiz"]:
        if user_answers.get(str(question["question"])) == question["answer"]:
            score += 1

    result = f"You got {score} out of {len(quiz_data['quiz'])} questions right."
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
