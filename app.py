from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_code"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

Responses_key = "responses"


@app.route('/')
def show_survey_start():
    return render_template('survey_start.html', survey=survey)

@app.route('/begin', method=["POST"])
def start_survey():
    session[Responses_key] = []

    return redirect('/questions/0')

@app.route('/answer', method=["POST"])
def handle_question():
    choice = request.form['answer']
    responses = session[Responses_key]
    responses.append(choice)
    session[Responses_key]= responses

    if (len(responses)== len(survey.questions)):
        return redirect("/complete")
    else:
        redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(Responses_key)

    if (responses is None):
        return redirect('/')
    if(len(responses)== len(survey.questions)):
        return redirect("/complete")
    if (len(responses) !== qid):
        flash(f"INVALID QUESTION ID: {qid}!")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("questions.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    return render_template("completion.html")
