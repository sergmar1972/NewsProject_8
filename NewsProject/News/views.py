from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.views.generic import ListView, DetailView, CreateView
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.info(request, 'Регистрация прошла успешно')
#             return redirect('Login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'News/register.html', {'form': form})

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'Регистрация прошла успешно')
            user=form.save()
            login(request, user)
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form =UserRegisterForm()

    return render(request, 'News/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('Login')

def user_login(request):
    if request.method=='POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect('Home')
    else:
            form=UserLoginForm()
    return render(request, 'News/login.html', {'form': form})


class HomeNews(ListView, MyMixin):
        model = News
        context_object_name = 'news'
        template_name = 'News/home_news_list.html'
        extra_context = {'title':'Главная'}
        paginate_by = 2

        def get_context_data(self, *, object_list=None, **kwargs):
            context=super().get_context_data(**kwargs)
            context['title']= ('Главная страница')

            return context



        def get_queryset(self):
            return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView,MyMixin):
    model= News
    template_name = 'News/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']= Category.objects.get(pk=self.kwargs['category_id'])
        return context



    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model=News
    context_object_name = 'news_item'


class AddNews(CreateView):
    form_class = NewsForm
    template_name = 'News/add_news.html'
    login_url='/admin/'
#
# class RegisterUser(MyMixin, CreateView):
#     form_class =UserCreationForm()
#     template_name = 'News/register.html'
#     context_object_name='Register'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def=self.get_user_context(title = "Регистрация")
#         return dict(list(context.items())+list(c_def.items()))

    # def test(request):
    #     objects = ['john', 'paul', 'george', 'ringo', 'john2', 'paul2', 'george2', 'ringo2']
    #     paginator = Paginator(objects, 2)
    #     page_num = request.GET.get('page', 1)
    #     page_objects = paginator.get_page(page_num)
    #     return render(request, 'News/test.html', {'page_obj': page_objects})

    # def index(request):
    #     news = News.objects.all()
    #     categories = Category.objects.all()
    #     context = {
    #         'news': news,
    #         'title': 'Список новостей',
    #     }
    #     return render(request, 'News/index.html', context=context)


#
# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     categories = Category.objects.all()
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request, 'News/category.html', context=context)


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item =get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item,
#
#     }
#     return render(request, 'News/view_news.html', context=context)


# def add_news(request):
#     if request.method == "POST":
#         form=NewsForm(request.POST)
#         if form.is_valid():
#             # news=News.objects.create(**form.cleaned_data)
#             news=form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'News/add_news.html',{'form':form})