from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core import validators
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response

from ask_app import helpers
from ask_app.forms import LoginForm, SignupForm
from ask_app.models import Question, Answer, QuestionLike, AnswerLike, Tag
from ask_app.decorators import need_login, need_login_ajax

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

@need_login
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)

def form_login(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
    else:
        form = LoginForm()

    return render(request, 'login.html', {
            'form': form,
        })

def form_signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {
            'form': form,
        })

def base(request):
    return render(request, "base.html")

def ask(request):
    return render(request, 'ask.html')

def error(request):
    return render(request, '404page.html')
