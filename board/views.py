from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DetailView
from .models import Post,Reply
from .filters import PostFilter
# Create your views here.
def index(request):
    return redirect('/board')

class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name ='post'