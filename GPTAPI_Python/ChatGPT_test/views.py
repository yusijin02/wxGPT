from django.shortcuts import render
from django.http import JsonResponse
import openai
import time
import hashlib
import json
import Key


def ChatGPT_test(request):
    try:
        openai.api_key = Key.Api_Key
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{'role': 'user', 'content': '请介绍你自己'}]
        )
        res_dict = dict(res)
        result = {
            'code': '200',
            'state': 'successful',
            'input': {
                'model': 'gpt-3.5-turbo',
                'message': [{'role': 'user', 'content': '请介绍你自己'}],
            },
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


