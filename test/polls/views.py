from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.template.loader import get_template
from .utils import render_to_pdf

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
    

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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