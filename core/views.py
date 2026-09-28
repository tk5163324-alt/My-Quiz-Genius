from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Profile, Question, QuizAttempt


# ============================================================
# HOME
# ============================================================

def base(request):
    return render(request, "index.html")


# ============================================================
# GENERATE QUIZ
# ============================================================

@login_required
def generate(request):

    if request.method == "POST":

        subject = request.POST.get("subject")
        difficulty = request.POST.get("difficulty")
        total_questions = int(
            request.POST.get("total_questions", 150)
        )

        questions = Question.objects.filter(
            subject=subject,
            difficulty=difficulty
        ).order_by("?")[:total_questions]

        if not questions.exists():
            return render(request, "generate.html", {
                "error": "No questions available for this selection."
            })

        request.session["quiz_questions"] = list(
            questions.values_list("id", flat=True)
        )

        request.session["quiz_index"] = 0
        request.session["wrong_questions"] = []

        return redirect("/quiz/")

    return render(request, "generate.html")


# ============================================================
# SHOW QUIZ QUESTION
# ============================================================

@login_required
def quiz(request):

    question_ids = request.session.get(
        "quiz_questions",
        []
    )

    index = request.session.get(
        "quiz_index",
        0
    )

    # No quiz started
    if not question_ids:
        return redirect("/generate/")

    # Quiz completed
    if index >= len(question_ids):

        score = request.session.get(
            "quiz_score",
            0
        )

        total = len(question_ids)

        # Save quiz attempt
        QuizAttempt.objects.create(
            user=request.user,
            score=score,
            total_questions=total
        )

        # Clear quiz session
        request.session.pop("quiz_questions", None)
        request.session.pop("quiz_index", None)
        request.session.pop("quiz_score", None)
        request.session.pop("quiz_subject", None)
        request.session.pop("quiz_difficulty", None)

        wrong_questions = request.session.get(
            "wrong_questions",
            []
        )
        
        return render(request, "result.html", {
            "score": score,
            "total": total,
            "wrong_questions": wrong_questions
        })
        
    # Get current question
    question_id = question_ids[index]

    question = Question.objects.filter(
        id=question_id
    ).first()

    # Question not found
    if question is None:
        return redirect("/generate/")

    return render(request, "quiz.html", {
        "question": question,
        "current": index + 1,
        "total": len(question_ids)
    })


# ============================================================
# SUBMIT ANSWER
# ============================================================

@login_required
def submit_answer(request):

    if request.method != "POST":
        return redirect("/quiz/")

    answer = request.POST.get(
        "answer",
        ""
    ).strip()

    question_ids = request.session.get(
        "quiz_questions",
        []
    )

    index = request.session.get(
        "quiz_index",
        0
    )

    score = request.session.get(
        "quiz_score",
        0
    )

    # Make sure quiz exists
    if not question_ids:
        return redirect("/generate/")

    # Make sure index is valid
    if index >= len(question_ids):
        return redirect("/quiz/")

    # Get current question
    question = Question.objects.filter(
        id=question_ids[index]
    ).first()

    if question:

        correct_answer = str(
            question.answer
        ).strip()

        if answer.lower() == correct_answer.lower():

            score += 1

        else:

            wrong_questions = request.session.get(
                "wrong_questions",
                []
            )

            wrong_questions.append({
                "question": question.question,
                "your_answer": answer,
                "correct_answer": correct_answer
            })

            request.session["wrong_questions"] = wrong_questions

    # Update score
    request.session["quiz_score"] = score

    # Move to next question
    request.session["quiz_index"] = index + 1

    return redirect("/quiz/")

# ============================================================
# LEADERBOARD
# ============================================================

def leaderboard(request):

    attempts = QuizAttempt.objects.select_related(
        "user"
    ).order_by(
        "-score",
        "-created_at"
    )

    return render(request, "leaderboard.html", {
        "attempts": attempts
    })


# ============================================================
# PROFILE
# ============================================================

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(request, "profile.html", {
        "profile": profile
    })


# ============================================================
# REGISTER
# ============================================================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check username
        if User.objects.filter(
            username=username
        ).exists():

            return render(request, "register.html", {
                "error": "Username already exists."
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create profile
        Profile.objects.get_or_create(
            user=user
        )

        # Login user
        login(request, user)

        return redirect("/")

    return render(request, "register.html")


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/")

        return render(request, "login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "login.html")


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    attempts = QuizAttempt.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    total_quizzes = attempts.count()

    return render(request, "dashboard.html", {
        "profile": profile,
        "total_quizzes": total_quizzes,
        "attempts": attempts
    })


# ============================================================
# LOGOUT
# ============================================================

def logout_view(request):

    logout(request)

    return redirect("/")