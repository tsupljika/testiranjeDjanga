from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.template.loader import get_template
from .utils import render_to_pdf
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def home(request):
    context = {}
    return render(request, 'polls/main.html', context)

def registerView(request):
    if request.user.is_authenticated:
        return redirect('polls:index')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created.')
            return redirect('polls:login')
        else:
            messages.error(request, 'Could not create new user.')

    context = {'form' : form}
    return render(request, 'polls/register.html', context)

def loginView(request):
    if request.user.is_authenticated:
        return redirect('polls:index')

    if request.method == 'POST':
        username = request.post.get('username')
        password = request.post.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            messages.info(request, 'Username or password is incorrect.')

    context = {}
    return render(request, 'polls/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('polls:home')

@method_decorator(login_required, name='dispatch')
class ReportView(generic.DetailView):
    model = Question
    template_name = 'polls/report.html'

def pdfView(request, question_id):
    template = get_template('polls/report.html')
    context = {
        "question" : get_object_or_404(Question, pk=question_id)
    }
    html = template.render(context)
    pdf = render_to_pdf('polls/report.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename='Report.pdf'"
        download = request.GET.get("download")
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
    
@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

@method_decorator(login_required, name='dispatch')
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))