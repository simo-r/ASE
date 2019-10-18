from flakon import JsonBlueprint
from flask import request, jsonify, abort
from hw1service.classes.quiz import Quiz, Question, Answer, NonExistingAnswerError, LostQuizError, CompletedQuizError

quizzes = JsonBlueprint('quizzes', __name__)

_LOADED_QUIZZES = {}  # list of available quizzes
_QUIZNUMBER = 0  # index of the last created quizzes
_POST = 'POST'
_GET = 'GET'
_PUT = 'PUT'
_DELETE = 'DELETE'
_MSG = 'msg'
_COMPLETED_QUIZ = 'completed quiz'
_YOU_LOST = 'you lost!'
_YOU_WON = 'you won 1 million clams!'
_NOT_EXISTING_ANSWER = 'non-existing answer!'
_ANSWERED_QUESTIONS = 'answered_questions'
_TOTAL_QUESTIONS = 'total_questions'


@quizzes.route("/quizzes", methods=[_GET, _POST])
def all_quizzes():
    if _POST == request.method:
        # Create a new quiz exploiting the already provided method.
        result = create_quiz(request)
    elif _GET == request.method:
        # Retrieve all loaded quizzes exploiting the already provided method.
        result = get_all_quizzes(request)

    # This warning situation will never happen because
    # this method will always enter in either the POST or the GET if statement.
    return result


@quizzes.route("/quizzes/loaded", methods=[_GET])
def loaded_quizzes():
    # Return the correct number identified by the variable _LOADED_QUIZZES.
    return jsonify(loaded_quizzes=len(_LOADED_QUIZZES))


@quizzes.route("/quiz/<id>", methods=[_GET, _DELETE])
def single_quiz(id):
    global _LOADED_QUIZZES
    result = ""
    # Check if the quiz is an existing one: raises an HTTPException automatically.
    exists_quiz(id)
    if _GET == request.method:
        # Retrieve a quiz <id> from the _LOADED_QUIZZES variable.
        var = _LOADED_QUIZZES[id]
        result = var.serialize()

    elif _DELETE == request.method:
        # Delete a quiz and get back the number of
        # answered questions and total number of questions.
        quiz = _LOADED_QUIZZES[id]
        result = {_ANSWERED_QUESTIONS: quiz.currentQuestion, _TOTAL_QUESTIONS: len(quiz.questions)}
        del _LOADED_QUIZZES[id]

    return jsonify(result)


@quizzes.route("/quiz/<id>/question", methods=[_GET])
def play_quiz(id):
    global _LOADED_QUIZZES
    result = ""

    # Check if the quiz is an existing one: raises an HTTPException automatically.
    exists_quiz(id)

    if _GET == request.method:
        # Retrieve the next question in a quiz,
        # handle exceptions returning a proper JSON for each exception.
        try:
            result = _LOADED_QUIZZES[id].getQuestion()
        except CompletedQuizError:
            result = {_MSG: _COMPLETED_QUIZ}
        except LostQuizError:
            result = {_MSG: _YOU_LOST}

    return jsonify(result)


@quizzes.route("/quiz/<id>/question/<answer>", methods=[_PUT])
def answer_question(id, answer):
    global _LOADED_QUIZZES
    result = ""
    # Check if the quiz is an existing one: raises an HTTPException automatically.
    exists_quiz(id)

    # Retrieve the quiz identified by id.
    quiz = _LOADED_QUIZZES[id]

    # Check if a quiz is lost or completed and act consequently
    # I exploited the isOpen() method which checks for both
    # and raises exceptions and returns proper JSON response if needed.
    try:
        quiz.isOpen()
    except CompletedQuizError:
        return jsonify({_MSG: _COMPLETED_QUIZ})
    except LostQuizError:
        return jsonify({_MSG: _YOU_LOST})

    if _PUT == request.method:
        # Check the answer provided by the user
        # and handle exceptions returning a proper JSON response.
        try:
            result = quiz.checkAnswer(answer)
        except CompletedQuizError:
            result = _YOU_WON
        except LostQuizError:
            result = _YOU_LOST
        except NonExistingAnswerError:
            result = _NOT_EXISTING_ANSWER
    return jsonify({_MSG: result})


############################################
# USEFUL FUNCTIONS BELOW (use them, don't change them)
############################################

def create_quiz(request):
    global _LOADED_QUIZZES, _QUIZNUMBER

    json_data = request.get_json()
    qs = json_data['questions']
    questions = []
    for q in qs:
        question = q['question']
        answers = []
        for a in q['answers']:
            answers.append(Answer(a['answer'], a['correct']))
        question = Question(question, answers)
        questions.append(question)

    _LOADED_QUIZZES[str(_QUIZNUMBER)] = Quiz(_QUIZNUMBER, questions)
    _QUIZNUMBER += 1

    return jsonify({'quiznumber': _QUIZNUMBER - 1})


def get_all_quizzes(request):
    global _LOADED_QUIZZES

    return jsonify(loadedquizzes=[e.serialize() for e in _LOADED_QUIZZES.values()])


def exists_quiz(id):
    if int(id) > _QUIZNUMBER:
        abort(404)  # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not (id in _LOADED_QUIZZES):
        abort(410)  # error 410: Gone, i.e. it existed but it's not there anymore
