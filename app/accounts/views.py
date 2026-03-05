from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import UserForm
from .models import User


def index(request):
    return render(request, "accounts/index.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user_pw = request.POST.get("user_pw")

        user = authenticate(request, username=username, password=user_pw)

        if user is not None:
            login(request, user)
            print("로그인 완료")
            return redirect("accounts:index")
        else:
            messages.warning(request, "아이디 또는 비밀번호를 확인해주세요")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")


def logout_page(request):
    logout(request)
    return render(request, "accounts/index.html")


def join_page(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        print(form.errors)
        print(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # 아직 DB 저장 X
            user.set_password(form.cleaned_data["password1"])  # ✅ 해시 저장
            user.save()
            messages.success(request, "회원가입이 완료 되었습니다.")
            return redirect("accounts:login")

    else:
        form = UserForm()
        print(request.POST)
        print(form.errors)
    return render(request, "accounts/join.html", {"form": form})


def join_check_page(request):
    return render(request, "accounts/join_check.html")


def id_search(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        users = User.objects.filter(phone=phone, email=email)

        return render(request, "accounts/id_search_result.html", {"users": users})

    return render(request, "accounts/id_search.html")


def pw_search(request):
    if request.method == "POST":
        id = request.POST.get("id")
        email = request.POST.get("email")

        user = User.objects.filter(username=id, email=email).first()

        if user:
            request.session["session_username"] = user.username

            return render(request, "accounts/pw_search_result.html", {"user": user})

    return render(request, "accounts/pw_search.html")


def pw_search_result(request):
    return render(request, "accounts/pw_search_result.html")


def pw_change(request):
    if request.method == "POST":
        username = request.session["session_username"]
        pw_1 = request.POST.get("pw_1")
        pw_2 = request.POST.get("pw_2")

        user = User.objects.get(username=username)

        try:
            validate_password(pw_1)
        except ValidationError as e:
            for error in e.messages:
                messages.warning(request, error)
            return redirect("accounts:pw_search_result")

        if pw_1 != pw_2:
            messages.warning(request, "비밀번호가 일치 하지 않습니다.")
            return redirect("accounts:pw_search_result")

        else:
            user.set_password(pw_1)
            user.save()

            del request.session["session_username"]

            messages.success(request, "비밀번호가 변경되었습니다.")
            return redirect("accounts:login")

    return render(request, "accounts/pw_search_result.html")
