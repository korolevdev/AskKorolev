from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from ask_app.models import Question, Answer, QuestionLike, AnswerLike, Tag

def error_not_found(request):
    return render(request, '404.html')

def error_server(request):
    return render(request, '500.html')
    
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

def new(request, page):
    questions_query = Question.objects.list_new()

    questions = getpagintator(questions_query, request, 4)
    return render(request, 'index.html', {'questions': questions})
    
def hot(request):
    questions_query = Question.objects.list_hot()

    questions = getpagintator(questions_query, request, 4)
    return render(request, 'hot.html', {'questions': questions})

def tag(request, htag, page):
    context = RequestContext(request, {
        'hash_tag': htag,
    })

    try:
        tag = Tag.objects.get_by_title(htag)
    except Tag.DoesNotExist:
        raise Http404()

    questions_query = Question.objects.list_tag(tag)

    questions = getpagintator(questions_query, request, 4)
    return render(request, 'tag.html', {'questions': questions, "context": context})

def question(request, question_id):
    try:
        ques = Question.objects.get_single(int(question_id))
    except Question.DoesNotExist:
        raise Http404()

    return render(request, 'question.html', {'question': ques})

def base(request):
    return render(request, "base.html")

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def error(request):
    return render(request, '404page.html')
