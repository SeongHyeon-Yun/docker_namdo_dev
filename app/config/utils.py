from django.core.paginator import Paginator


def page_queryset(request, queryset, per_page=20):
    page = request.GET.get("page")

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)

    # 기존 쿼리스트링 유지 (page 제거)
    query = request.GET.copy()
    query.pop("page", None)

    query_string = query.urlencode()

    return page_obj, query_string
