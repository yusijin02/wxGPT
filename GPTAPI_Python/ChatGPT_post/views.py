from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import time
import hashlib
import json
import Key


@csrf_exempt
def ChatGPT_post(request):
    if request.method == 'POST':
        # 获取参数
        data = json.loads(request.body)
        t = data.get('t', None)
        s = data.get('s', None)
        k = data.get('k', None)
        model = data.get('model', None)
        messages = data.get('messages', None)
        max_tokens = data.get('max_tokens', None)
        temperature = data.get('temperature', 1.0)

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
        string = k + str(t)
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
        if not (max_tokens is None):
            try:
                max_tokens = int(max_tokens)
            except Exception:
                result = {
                    'code': '402',
                    'state': 'max_token must be int',
                    'res': {},
                }
                return JsonResponse(result)

        try:
            openai.api_key = Key.Api_Key
            res = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            res_dict = dict(res)
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
    else:
        return JsonResponse({'errorMessage': '仅接受POST请求'})