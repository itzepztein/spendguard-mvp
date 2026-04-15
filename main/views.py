from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, GoalForm
from .models import User, FinancialGoal

def landing(request):
    return render(request, 'main/landing.html')

def setup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        goal_form = GoalForm(request.POST)
        if user_form.is_valid() and goal_form.is_valid():
            # сохраняем пользователя
            user = user_form.save()
            # сохраняем цель, привязывая к пользователю
            goal = goal_form.save(commit=False)
            goal.user = user
            goal.save()
            messages.success(request, 'Данные сохранены!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        user_form = UserForm()
        goal_form = GoalForm()
    return render(request, 'main/setup.html', {
        'user_form': user_form,
        'goal_form': goal_form,
    })

def dashboard(request):
    # Для демо – показываем последнего добавленного пользователя и его первую цель
    try:
        latest_user = User.objects.latest('id')
        goals = FinancialGoal.objects.filter(user=latest_user).order_by('-id')
        first_goal = goals.first() if goals else None
    except User.DoesNotExist:
        latest_user = None
        first_goal = None

    # Заглушка рекомендаций ИИ
    recommendations = [
        {'text': 'Вы тратите на кафе на 30% больше среднего. Попробуйте готовить дома 2 раза в неделю.', 'saving': 2500},
        {'text': 'Подписка на сервисы: отключите неиспользуемые, сэкономите 800 ₽/мес.', 'saving': 800},
        {'text': 'Используйте кэшбэк-карту для повседневных покупок.', 'saving': 500},
    ]
    return render(request, 'main/dashboard.html', {
        'user': latest_user,
        'goal': first_goal,
        'recommendations': recommendations,
    })