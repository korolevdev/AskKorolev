from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def get_post_params(request):
    result = ['<p>Django!</p>']
    result.append('Post:')
    result.append('<form method="post">')
    result.append('<input type="text" name = "test">')
    result.append('<input type="submit" value="Send">')
    result.append('</form>')

    if request.method == 'POST':
        result.append(request.POST.urlencode())

    if request.method == 'GET':
        if request.GET.urlencode() != '':
            result.append('Get data:')
            #result.append(request.GET.urlencode())
            for key, value in request.GET.items():
                keyvalue=key+" = "+value
                result.append(keyvalue)

    return HttpResponse('<br>'.join(result))
