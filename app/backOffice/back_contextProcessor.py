from wallet.models import Wallet_list


# 에치금 메뉴 카운터
def wallet_count(request):
    wallet_list = Wallet_list.objects.filter(status="pending").count()
    return {"wallet_count": wallet_list}
