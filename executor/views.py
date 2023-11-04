from django.views import generic

from .models import Executor


class IndexView(generic.ListView):
    template_name = "executor/index.html"
    context_object_name = "executors"
    ordering = ["-rating"]
    queryset = Executor.objects.all()


class DetailView(generic.DetailView):
    model = Executor
    template_name = "executor/detail.html"
    context_object_name = "executors"
