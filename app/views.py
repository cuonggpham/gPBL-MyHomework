from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Homework
from .forms import HomeworkForm

def home(request):
    return render(request, 'index.html')

def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index_logined')  # 成功後にリダイレクトする URL
    else:
        form = AuthenticationForm()
    return render(request, 'view/sign-in.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index_logined')  # 成功後にリダイレクトする URL
    else:
        form = UserCreationForm()
    return render(request, 'view/sign-up.html', {'form': form})

def index_logined(request):
    return render(request, 'view/index-logined.html')

@login_required
def view_homework(request):
    sort_by = request.GET.get('sort_by','priority')
    if sort_by == 'due_date':
        homework_list = Homework.objects.filter(user=request.user, finished=False).order_by('due_date')
    else:
        homework_list = Homework.objects.filter(user=request.user, finished=False).order_by('priority')
    #finishedがFalseのHomeworkのみをデータベースから持ってくる
    context = { 'homework_list':homework_list }
    return render(request, 'view/view-homework.html', context)

@login_required
def delete_homework(request):
    if request.method == 'POST':
        homework_id = request.POST.get('homework_id')
        if homework_id:
            homework = get_object_or_404(Homework, id=homework_id, user=request.user,)
            homework.delete()
        return redirect('view_homework')

    return render(request, 'error.html', {'message': 'Invalid request method'})

@login_required
def add_homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.user = request.user
            homework.save()
            return redirect('view_homework')  # 成功後にリダイレクト
    else:
        form = HomeworkForm()
    return render(request, 'view/add-homework.html', {'form': form})

@login_required
def homework_details(request, id):
    homework = get_object_or_404(Homework, id=id, user=request.user)
    context = {'homework':homework}
    return render(request, 'view/homework-details.html', context)

@login_required
def finished_homework(request):
    #引数でhomework_idをもらう、その宿題のfinishedを０から１に変える（finished画面だけに表示されるようになる）
    if request.method == 'POST':
        homework_id = request.POST.get('homework_id')
        if homework_id:
            homework = get_object_or_404 (Homework, id=homework_id, user=request.user)
            homework.finished = True
            homework.save()
    #finishedがTrueのHomeworkのみをデータベースから持ってくる
    finished_list = Homework.objects.filter(user=request.user, finished=True)
    context = { 'finished_list':finished_list }
    return render(request, 'view/finished-homework.html', context)
