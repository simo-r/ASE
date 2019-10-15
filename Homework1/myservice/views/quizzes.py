from flakon import JsonBlueprint
from flask import request, jsonify, abort
from myservice.classes.quiz import Quiz, Question, Answer, NonExistingAnswerError, LostQuizError, CompletedQuizError

quizzes = JsonBlueprint('quizzes', __name__)

_LOADED_QUIZZES = {}  # list of available quizzes
_QUIZNUMBER = 0  # index of the last created quizzes
_MSG = 'msg'


@quizzes.route("/quizzes", methods=['GET', 'POST'])
def all_quizzes():
    if 'POST' == request.method:
        # Create a new quiz exploiting the already provided method.
        result = create_quiz(request)
    elif 'GET' == request.method:
        # Retrieve all loaded quizzes exploiting the already provided method.
        result = get_all_quizzes(request)

    # This warning situation will never happen because
    # this method will always enter in either the POST or the GET if statement.
    return result


@quizzes.route("/quizzes/loaded", methods=['GET'])
def loaded_quizzes():
    # Return the correct number identified by the variable _LOADED_QUIZZES.
    # return jsonify({'loaded_quizzes': len(_LOADED_QUIZZES)})
    return jsonify(loaded_quizzes=len(_LOADED_QUIZZES))


@quizzes.route("/quiz/<id>", methods=['GET', 'DELETE'])
def single_quiz(id):
    global _LOADED_QUIZZES
    result = ""
    # Check if the quiz is an existing one: raises an HTTPException automatically.
    exists_quiz(id)
    if 'GET' == request.method:
        # Retrieve a quiz <id> from the _LOADED_QUIZZES variable.
        var = _LOADED_QUIZZES[id]
        result = var.serialize()

    elif 'DELETE' == request.method:
        # Delete a quiz and get back the number of
        # answered questions and total number of questions.
        quiz = _LOADED_QUIZZES[id]
        result = {"answered_questions": quiz.currentQuestion, "total_questions": len(quiz.questions)}
        del _LOADED_QUIZZES[id]

    return jsonify(result)


@quizzes.route("/quiz/<id>/question", methods=['GET'])
def play_quiz(id):
    global _LOADED_QUIZZES
    result = ""

    # Check if the quiz is an existing one: raises an HTTPException automatically.
    exists_quiz(id)

    if 'GET' == request.method:
        # Retrieve the next question in a quiz,
        # handle exceptions returning a proper JSON for each exception.
        try:
            result = _LOADED_QUIZZES[id].getQuestion()
        except CompletedQuizError:
            result = {_MSG: 'completed quiz'}
        except LostQuizError:
            result = {_MSG: 'you lost!'}

    return jsonify(result)


@quizzes.route("/quiz/<id>/question/<answer>", methods=['PUT'])
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
        return jsonify({_MSG: "completed quiz"})
    except LostQuizError:
        return jsonify({_MSG: "you lost!"})

    if 'PUT' == request.method:
        # Check the answer provided by the user
        # and handle exceptions returning a proper JSON response.
        try:
            result = quiz.checkAnswer(answer)
        except CompletedQuizError:
            result = 'you won 1 million clams!'
        except LostQuizError:
            result = 'you lost!'
        except NonExistingAnswerError:
            result = 'non-existing answer!'
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
