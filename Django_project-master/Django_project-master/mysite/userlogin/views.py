from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from .forms import UserForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import(
    authenticate,
    login as django_login,
    logout as django_logout,
)


def index(request):
    if not request.user.is_authenticated:
        data = {"username":request.user, "is_authenticated":request.user.is_authenticated}
    else:
        data = {"last_login":request.user.last_login, "username":request.user.username,
        "password":request.user.password,"is_authenticated":request.user.is_authenticated}
    return render(request, "userlogin/index.html", context= {"data":data}
    )
@csrf_exempt
def signup(request):
    print("----------singup()--------------")
    if request.method =="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            django_login(request, new_user)
            return redirect("/")
        else:
            return render_to_response("userlogin/index.html",{"msg":"회원 가입 실패, 다시시도해주세요"})
    else:
        form = UserForm()
        return render(request, "userlogin/signup.html",{"form" : form})
    return render(request, "userlogin/index.html")


def login_check(request):
    if request.method =="POST":
        form = LoginForm(request.POST)
        name = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(username=name, password=pwd)
        if user is not None:
            django_login(request, user)
            return redirect("/")
        else:
            return render_to_response("userlogin/index.html.",{"msg":"로그인 실패, 다시시도해주세요"})
    else:
        form = LoginForm()
        return render(request, "userlogin/login.html", {"form":form})

def logout(request):
    django_logout(request)
    return redirect("/")