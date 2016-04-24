from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response

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

questions = []
for i in xrange(30):
    questions.append({
        'title': 'Why i cant jump on 10 meters? (Question # {})'.format(i),
        'body': 'Actually the question has already been set',
        'nickname': "Nickname{}".format(i),
        'id': i,
    })

def getpagintator(parametr, request, nums_on_list):
    paginator = Paginator(parametr, nums_on_list)
    page = request.GET.get('page')
    try:
        questions1 = paginator.page(page)
    except PageNotAnInteger:
        questions1 = paginator.page(1)
    except EmptyPage:
        questions1 = paginator.page(paginator.num_pages)
    return questions1

def index(request, page):
    questions1 = getpagintator(questions, request, 4)
    return render_to_response('index.html', {"questions1": questions1})
    # return render(request, 'index.html', {"questions": questions[:5]}, page)
    
def base(request):
    return render(request, "base.html")

def ask(request):
    return render(request, 'ask.html')

def question(request, question_id):
    context = RequestContext(request, {
        'que_id': question_id,
    })
    return render(request, 'question.html', {'questions': questions, "context": context})

def hot(request):
    questions1 = getpagintator(questions, request, 3)
    return render(request, 'hot.html', {'questions1': questions1,})

def error_not_found(request):
    return render(request, '404.html')

def error_server(request):
    return render(request, '500.html')

def login(request):
    return render(request, 'login.html')

def tag(request, htag, page):
    context = RequestContext(request, {
        'hash_tag': htag,
        "n_page": page,
    })
    questions1 = getpagintator(questions, request, 4)
    return render(request, 'tag.html', {'questions1': questions1, "context": context})


def signup(request):
    return render(request, 'signup.html')

def error(request):
    return render(request, '404page.html')
