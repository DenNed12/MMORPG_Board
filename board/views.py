from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DetailView, DeleteView
from .models import Post,Reply
from .filters import PostFilter
from .forms import PostForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
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


class CreatePost(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_create_form.html'
    #context_object_name = 'create_post'


class EditPost(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_update_form.html'
    context_object_name = 'edit_post'


class DeletePost(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'board/post_confirm_delete.html'
    #context_object_name = 'delete_post'


@login_required()
def add_reply(request,pk):
    post = get_object_or_404(Post, pk =pk)
    reply = Reply.objects.filter(postReply = post)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            repl = form.save(commit=False)
            repl.postReply = post
            repl.postUser = request.user
            repl.save()
    else:
        form = ReplyForm()

    return render(request, 'board/post_detail.html', {'post': post, 'form': form, 'reply': reply})