from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login
# Create your views here.


class UserRegisterView(CreateView):
    """
    Представление для регистрации пользователей
    """
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('landing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация пользователя'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Дополнительная логика после успешной регистрации
        user = self.object
        login(self.request, user)  # Автоматический вход после регистрации
        messages.success(self.request, f"Вы успешно зарегистрированы и вошли в систему, {user.username}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Если пользователь уже авторизован, перенаправляем на главную страницу
            messages.success(request, "Вы уже авторизованы.")
            return redirect('landing')
        return super().dispatch(request, *args, **kwargs)
    

class UserLoginView(LoginView):
    """
    Представление для входа пользователей
    """
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True  # Перенаправление авторизованных пользователей

    def get_success_url(self):
        messages.success(self.request, f"Вы успешно вошли в систему, {self.request.user.username}.")
        next_url = self.request.GET.get('next')
        return next_url or reverse_lazy('landing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход пользователя'
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Неверное имя пользователя или пароль.")
        return super().form_invalid(form)
    

class UserLogoutView(LogoutView):
    """
    Представление для выхода пользователей
    """
    next_page = reverse_lazy('landing')  # Перенаправление после выхода

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Если пользователь авторизован, выводим сообщение об успешном выходе
            messages.info(request, "Вы успешно вышли из системы.")
        return super().dispatch(request, *args, **kwargs)