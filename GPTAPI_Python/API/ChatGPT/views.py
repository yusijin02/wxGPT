from django.http import JsonResponse
import openai
import time
import hashlib
import json
import Key


def ChatGPT(request):
    # 获取参数
    # -------安全校验---------
    # 时间戳
    t = request.GET.get('t')
    # 加密参数
    s = request.GET.get('s')
    # 用户参数
    k = request.GET.get('k')

    # -------提交参数---------
    model = request.GET.get('model')
    messages = request.GET.get('messages')



    # ============== 验证安全参数 ==================
    if t is None or s is None or k is None:
        result = {
            'code': '404',
            'state': 'Not Found',
            'res': {},
        }
        return JsonResponse(result)
    timestamp = time.time()
    if timestamp - t > 600 or t - timestamp > 300:
        result = {
            'code': '400',
            'state': 'TimeError',
            'res': {},
        }
        return JsonResponse(result)

    if k not in Key.Key:
        result = {
            'code': '401',
            'state': 'UserError',
            'res': {},
        }
        return JsonResponse(result)
    string = k + t
    hash_object = hashlib.sha256()
    hash_object.update(string.encode())
    hash_value = hash_object.hexdigest()
    if hash_value != s:
        result = {
            'code': '403',
            'state': 'Forbidden',
            'res': {},
        }
        return JsonResponse(result)

    if model is None or messages is None:
        result = {
            'code': '402',
            'state': 'model and messages must not be None',
            'res': {},
        }
        return JsonResponse(result)
    try:
        openai.api_key = Key.Api_Key
        res = openai.Completion.create(
            model=model,
            messages=eval(messages),
        )
        res_dict = json.loads(res)
        result = {
            'code': '200',
            'state': 'successful',
            'res': res_dict,
        }
        return JsonResponse(result)
    except Exception as e:
        result = {
            'code': '405',
            'state': 'OpenaiApiError',
            'res': str(e),
        }
        return JsonResponse(result)





