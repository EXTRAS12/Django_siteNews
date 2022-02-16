from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView

from .forms import ContactForm, NewsForm, UserLoginForm, UserRegisterForm
from .models import Category, News
from .utils import MyMixin


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')

    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    """Вход(Логин) пользователся"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    """Выход залогиневшегося пользователя"""
    logout(request)
    return redirect('login')


def contact(request):
    """Страничка контакты"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'extra-kent@mail.ru', ['intfloatwork@yandex.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')

    else:
        form = ContactForm()
    return render(request, 'news/test.html', {"form": form})


class HomeNews(ListView, MyMixin):
    """Главная страница"""
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')

        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class ViewNews(DetailView):
    """Страница отдельной статьи"""
    model = News
    context_object_name = 'news_item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class NewsByCategory(ListView, MyMixin):
    """Страница категории"""
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class CreateNews(LoginRequiredMixin, CreateView):
    """Создание своей статьи"""
    form_class = NewsForm
    template_name = 'news/add_news.html'
    raise_exception = True
