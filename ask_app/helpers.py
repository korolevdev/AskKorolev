from django.http import HttpResponse
import json

# response ajax
class HttpResponseAjax(HttpResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(
                content = json.dumps(kwargs),
                content_type = 'application/json',
                )


# response ajax with error
class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(
                status = 'error', code = code, message = message
                )
