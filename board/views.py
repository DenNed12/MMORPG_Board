from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DetailView, DeleteView
from .models import Post,Reply
from .filters import PostFilter
from .forms import PostForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import User
from django.core.mail import send_mail


email = "deonissl@yandex.ru"


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


# @login_required()
# def add_reply(request,pk):
#     post = get_object_or_404(Post, pk =pk)
#     reply = Reply.objects.filter(postReply = post)
#     if request.method == 'POST':
#         form = ReplyForm(request.POST)
#         if form.is_valid():
#             repl = form.save(commit=False)
#             repl.postReply = post
#             repl.postUser = request.user
#             repl.save()
#     else:
#         form = ReplyForm()
#
#     return render(request, 'board/post_detail.html', {'post': post, 'form': form, 'reply': reply})


class AddReply(LoginRequiredMixin, CreateView):
    raise_exception = True
    model = Reply
    form_class = ReplyForm
    template_name = 'board/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReplyForm
        return context

    def post(self,request, *args,**kwargs):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if form.is_valid():
            reply = form.save(commit=False)
            reply.authorReply = self.request.user
            reply.post_id = self.kwargs['pk']
            reply.post = post
            reply.save()
            author = User.objects.get(pk=post.author_id)
            send_mail(
                subject='Отклик на объявление',
                message=f'На объявление {post} был добавлен отклик {reply.text} пользователем {self.request.user}.\n'
                        f'Прочитать отклик:\nhttp://127.0.0.1:8000/posts/{reply.post.id}',
                from_email=email,
                recipient_list=[author.email],
            )
        return redirect('/board/post_detail.html')


class PostDetail(AddReply,DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name ='post'



class Replies(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'board/replies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Reply.objects.filter(authorReply_id=self.request.user.id)
        context['filterset'] = PostFilter(self.request.GET, queryset, request=self.request.user.id)
        return context