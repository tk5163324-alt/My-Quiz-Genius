from django.shortcuts import render, redirect
from .models import Category, Question, Attempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def user_login(request):

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



    return render(

        request,

        "login.html"

    )


# Home page
def dashboard(request):

    if request.user.is_authenticated:


        attempts = Attempt.objects.filter(
            user=request.user
        ).order_by("-created_at") 


        total_quizzes = attempts.count()



        if attempts.exists():

            best_score = max(
                a.percentage
                for a in attempts
            )

        else:

            best_score = 0



        return render(

            request,

            "dashboard.html",

            {

                "username": request.user.username,

                "total_quizzes": total_quizzes,

                "best_score": best_score,

                "attempts": attempts[:5]

            }

        )



    return render(

        request,

        "dashboard.html"

    )



# Start Quiz page

@login_required
def start_quiz(request):


    categories = Category.objects.all()



    if request.method == "POST":



        # Submit quiz

        if "submit_quiz" in request.POST:



            questions = Question.objects.filter(

                id__in=request.POST.getlist("question_id")

            )



            results = []

            score = 0




            for q in questions:



                user_answer = request.POST.get(

                    f"question_{q.id}"

                )



                if user_answer == q.correct_answer:

                    score += 1

                    correct = True


                else:

                    correct = False




                results.append({

                    "question": q,

                    "user_answer": user_answer,

                    "correct": correct

                })





            total_questions = len(results)



            if total_questions > 0:

                percentage = (score / total_questions) * 100


            else:

                percentage = 0





            # Save quiz attempt


            if questions.exists():

                Attempt.objects.create(

                    user=request.user,

                    category=questions.first().category.name,

                    score=score,

                    total_questions=total_questions,

                    percentage=percentage

                )





            return render(

                request,

                "result.html",

                {

                    "results": results,

                    "score": score,

                    "percentage": percentage

                }

            )







        # Start quiz settings


        category_id = request.POST.get("category")


        difficulty = request.POST.get("difficulty")



        question_limit = int(

            request.POST.get("question_limit")

        )





        questions = Question.objects.filter(

            category_id=category_id,

            difficulty=difficulty

        ).order_by('?')[:question_limit]





        return render(

            request,

            "quiz.html",

            {

                "questions": questions

            }

        )






    return render(

        request,

        "start_quiz.html",

        {

            "categories": categories

        }

    )







# Leaderboard page

@login_required
def leaderboard(request):


    attempts = Attempt.objects.all().order_by("-percentage"

    )



    return render(

        request,

        "leaderboard.html",

        {

            "attempts": attempts

        }

    )







# Profile page


@login_required
def profile(request):


    attempts = Attempt.objects.filter(

        user=request.user

    ).order_by("-created_at")




    total_quizzes = attempts.count()




    if attempts.exists():


        best_score = max(

            attempt.percentage

            for attempt in attempts

        )


    else:


        best_score = 0





    return render(

        request,

        "profile.html",

        {


            "username": request.user.username,


            "total_quizzes": total_quizzes,


            "best_score": best_score,


            "attempts": attempts


        }

    )