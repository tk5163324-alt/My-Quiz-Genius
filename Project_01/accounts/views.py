import django.shortcuts

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from quiz.models import Profile



def register(request):


    if request.method == "POST":


        username = request.POST["username"]

        email = request.POST["email"]

        password = request.POST["password"]




        # Check username already exists

        if User.objects.filter(username=username).exists():


            messages.error(

                request,

                "Username already exists. Please choose another."

            )


            return django.shortcuts.redirect("register")






        # Create user

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password

        )


        user.save()






        # Save profile picture


        profile_pic = request.FILES.get("profile_pic")


        Profile.objects.get_or_create(
        user=user,
        defaults={
        "profile_pic": profile_pic
    }
)

        messages.success(request,

            "Registration successful. Please login."

        )



        return django.shortcuts.redirect("login")






    return django.shortcuts.render(

        request,

        "register.html"

    )








def login_user(request):


    if request.method == "POST":



        username = request.POST["username"]


        password = request.POST["password"]





        user = authenticate(

            username=username,

            password=password

        )






        if user is not None:



            login(

                request,

                user

            )



            return django.shortcuts.redirect("/")

        else:


            messages.error(

                request,

                "Invalid username or password."

            )


    return django.shortcuts.render(

        request,

        "login.html"

    )



def logout_user(request):


    logout(request)


    return django.shortcuts.redirect("/")