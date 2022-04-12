import json
from ntpath import join
from django.utils.deprecation import MiddlewareMixin
import json

class Md1(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            request.data = data

    def process_response(self, rquest, response):
        return response