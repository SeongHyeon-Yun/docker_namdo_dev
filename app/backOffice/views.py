from django.shortcuts import render, redirect
from accounts.models import User
from wallet.models import Wallet_list, Balance
from django.contrib import messages
from config.utils import page_queryset
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse


# 실시간 알람 완료
def wallet_count_api(request):
    count = Wallet_list.objects.filter(status="pending").count()
    return JsonResponse({"wallet_count": count})


# 메인화면 진행중
def index(request):
    return render(request, "backOffice/index.html")


# 상품관리 진행중
def item_page(request):
    return render(request, "backOffice/fun_item/item_page.html")


# 주문관리 진행중
def order_page(request):
    return render(request, "backOffice/fun_order/order_page.html")


# 배송관리 진행중
def delivery_page(request):
    return render(request, "backOffice/fun_delivery/delivery_page.html")


# 예치금관리 완료
def wallet_page(request):
    _type = request.GET.get("type", "deposit")
    search_type = request.GET.get("status")
    search_value = request.GET.get("search_value")

    wallet_list = Wallet_list.objects.select_related("user").order_by("-id")

    if _type == "deposit":
        wallet_list = wallet_list.filter(wallet_type="deposit", status="pending")

    elif _type == "refund":
        wallet_list = wallet_list.filter(wallet_type="refund", status="pending")

    elif _type == "d_list":
        wallet_list = wallet_list.filter(wallet_type="deposit").exclude(
            status="pending"
        )

    elif _type == "r_list":
        wallet_list = wallet_list.filter(wallet_type="refund").exclude(status="pending")

    if search_type and search_value:
        wallet_list = wallet_list.filter(
            **{f"user__{search_type}__icontains": search_value}
        )

    deposit_count = Wallet_list.objects.filter(
        wallet_type="deposit", status="pending"
    ).count()

    refund_count = Wallet_list.objects.filter(
        wallet_type="refund", status="pending"
    ).count()

    page_obj, query = page_queryset(request, wallet_list, 20)

    if request.method == "POST":
        action = request.POST.get("btn")
        # 신청의 건 가져오기
        wallet_id = request.POST.get("user_id")
        wallet = Wallet_list.objects.get(id=wallet_id)

        # 유저 지갑 가져오기
        user_balance = Balance.objects.get(user_id=wallet.user_id)
        # 신청금액
        appliction_amount = wallet.amount
        # user =
        with transaction.atomic():
            if action == "approve":
                if wallet.wallet_type == "deposit":
                    if wallet.is_dupli == False:
                        # 신청 상태 리스트 변경
                        wallet.status = "approved"
                        wallet.is_dupli = True
                        # 잔고 업데이트
                        user_balance.amount += appliction_amount

                        # 상태 및 잔고 저장
                        user_balance.save()
                        wallet.save()

                        # 완료 후 메세지 전송
                        messages.success(request, "충전이 승인되었습니다.")
                        return redirect("back_office:wallet_page")
                    else:
                        messages.success(request, "이미 처리되었습니다.")
                        return redirect("back_office:wallet_page")
                else:
                    if wallet.is_dupli == False:
                        wallet.status = "approved"
                        wallet.is_dupli = True

                        wallet.save()
                        url = reverse("back_office:wallet_page") + "?type=refund"
                        messages.success(request, "환불이 승인되었습니다.")
                        return redirect(url)
                    else:
                        url = reverse("back_office:wallet_page") + "?type=refund"
                        messages.success(request, "이미 처리되었습니다.")
                        return redirect(url)
            else:
                # 충전 거절
                if wallet.wallet_type == "deposit":
                    if wallet.is_dupli == False:
                        wallet.status = "rejected"
                        wallet.is_dupli = True
                        wallet.save()

                        messages.success(request, "충전 신청이 거절되었습니다.")
                        return redirect("back_office:wallet_page")
                    else:
                        messages.success(request, "이미 처리되었습니다.")
                        return redirect("back_office:wallet_page")
                # 환전 거절
                else:
                    if wallet.is_dupli == False:
                        wallet.status = "rejected"
                        wallet.is_dupli = True

                        user_balance.amount += appliction_amount
                        user_balance.save()
                        wallet.save()

                        url = reverse("back_office:wallet_page") + "?type=refund"

                        messages.success(request, "환불 신청이 거절되었습니다.")
                        return redirect(url)
                    else:
                        url = reverse("back_office:wallet_page") + "?type=refund"

                        messages.success(request, "이미 처리되었습니다.")
                        return redirect(url)

    context = {
        "users": page_obj,
        "type": _type,
        "deposit_count": deposit_count,
        "refund_count": refund_count,
        "query": query,
    }

    return render(request, "backOffice/fun_wallet/wallet_list.html", context)


# 유저관리 완료
def user_page(request):
    status = request.GET.get("status")
    _type = request.GET.get("_type", "all")
    search_value = request.GET.get("search_value")

    users = User.objects.all().order_by("-id")

    # 활성 상태 필터
    if _type == "nomal":
        users = users.filter(is_active=True)
    elif _type == "stop":
        users = users.filter(is_active=False)

    # 검색 버튼 눌렀는데 검색어 없음
    if "search_value" in request.GET and not search_value:
        messages.warning(request, "검색어를 입력하세요")
        return redirect("back_office:user_page")

    # 검색
    if status and search_value:
        users = users.filter(**{f"{status}__icontains": search_value})

    # POST 처리
    if request.method == "POST":
        type_btn = request.POST.get("type_btn")
        user_ids = request.POST.getlist("user_id")

        if type_btn == "active":
            User.objects.filter(id__in=user_ids).update(is_active=True)

        elif type_btn == "stop":
            User.objects.filter(id__in=user_ids).update(is_active=False)

        return redirect("back_office:user_page")

    page_obj, query = page_queryset(request, users, 20)

    context = {
        "users": page_obj,
        "type": _type,
        "query": query,
    }

    return render(request, "backOffice/fun_user/user_page.html", context)
