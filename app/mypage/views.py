from django.shortcuts import render, redirect
from django.contrib import messages
from wallet.models import Wallet_list, Balance
from decimal import Decimal
from django.db import transaction
from config.utils import page_queryset


def mypage(request):
    return render(request, "mypage/deposit.html")


# 충전신청
def deposit(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        int_amount = int(amount.replace(",", ""))

        if int_amount < 10000:
            messages.warning(request, "최소 충전금액을 확인해주세요")
            return redirect("mypage:deposit")
        else:
            create_wallet = Wallet_list(
                user=request.user,
                amount=int_amount,
                wallet_type="deposit",
                status="pending",
            )
            create_wallet.save()

            messages.success(request, "충전이 완료 되었습니다.")
            return redirect("mypage:amount")

    return render(request, "mypage/deposit.html")


# 환급신청
def refund(request):
    if request.method == "POST":
        amount = Decimal(request.POST.get("amount").replace(",", ""))

        with transaction.atomic():

            wallet = Balance.objects.select_for_update().get(user=request.user)

            if amount > wallet.amount:
                messages.warning(request, "잔액이 부족합니다.")
                return redirect("mypage:refund")

            wallet.amount -= amount
            wallet.save(update_fields=["amount"])

            Wallet_list.objects.create(
                user=request.user,
                amount=amount,
                wallet_type="refund",
                status="pending",
            )

        messages.success(request, "환급 신청이 완료되었습니다.")
        return redirect("mypage:amount")

    return render(request, "mypage/refund.html")


# 신청내역
def amount(request):
    date_range = request.GET.get("date_range")
    wallet_list = Wallet_list.objects.filter(user=request.user).order_by("-id")

    if request.GET and not date_range:
        messages.warning(request, "날짜를 선택해주세요.")
        return redirect("mypage:amount")

    if date_range:
        start_date, end_date = [d.strip() for d in date_range.split("~")]

    page_obj = page_queryset(request, wallet_list)

    context = {"users": page_obj}

    return render(request, "mypage/amount_list.html", context)
