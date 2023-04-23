from django.http import JsonResponse


def demo(request):
    # 获取参数并构造返回值
    a = request.GET.get('a')
    b = request.GET.get('b')
    result = {
        'title': '测试通过',
        'a': a,
        'b': b,
    }
    return JsonResponse(result)

