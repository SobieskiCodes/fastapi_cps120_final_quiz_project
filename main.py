import json
import pathlib
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from random import shuffle

app = FastAPI()
BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    with open(BASE_DIR / "questions.json", "r") as question_file:
        quiz_data = json.load(question_file)

    # Shuffle the options for each question
    for question in quiz_data["quiz"]:
        shuffle(question["options"])

    context = {
        "request": request,
        "title": "Multiple Choice Quiz",
        "quiz": quiz_data["quiz"]
    }

    #print(quiz_data)
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
        #print('users answer:', user_answers.get(str(question["question"])), ', the answer:', question["answer"])
        if user_answers.get(str(question["question"])) == question["answer"]:
            score += 1

    result = f"You got {score} out of {len(quiz_data['quiz'])} questions right."
    # i think i'd rather pop up or highlight the correct answers / questions vs a new page, but its a lot of work / javascript
    return templates.TemplateResponse("result.html", {"request": request, "result": result})
