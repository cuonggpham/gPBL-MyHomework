from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Homework
from .forms import HomeworkForm

def home(request):
    return render(request, 'index.html')

def sign_in(request):
    return render(request, 'view/sign-in.html')
def sign_up(request):
    return render(request, 'view/sign-up.html')

def index_logined(request):
    return render(request, 'view/index-logined.html')

def view_homework(request):
    sort_by = request.GET.get('sort_by','priority')
    if sort_by == 'due_date':
        homework_list = Homework.objects.filter(finished=False).order_by('due_date')
    else:
        homework_list = Homework.objects.filter(finished=False).order_by('priority')
    #finishedがFalseのHomeworkのみをデータベースから持ってくる
    context = { 'homework_list':homework_list }
    return render(request, 'view/view-homework.html', context)

def delete_homework(request):
    if request.method == 'POST':
        homework_id = request.POST.get('homework_id')
        if homework_id:
            homework = get_object_or_404(Homework, id=homework_id)
            homework.delete()
        return redirect('view_homework')

    return render(request, 'error.html', {'message': 'Invalid request method'})

def add_homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            form.save()  # データベースに保存
            return redirect('view_homework')  # 成功後にリダイレクト
    else:
        form = HomeworkForm()
    return render(request, 'view/add-homework.html', {'form': form})

def homework_details(request, id):
    homework = get_object_or_404(Homework, id=id)
    context = {'homework':homework}
    return render(request, 'view/homework-details.html', context)

def finished_homework(request):
    #引数でhomework_idをもらう、その宿題のfinishedを０から１に変える（finished画面だけに表示されるようになる）
    if request.method == 'POST':
        homework_id = request.POST.get('homework_id')
        homework = get_object_or_404 (Homework, id=homework_id)
        homework.finished = True
        homework.save()
    #finishedがTrueのHomeworkのみをデータベースから持ってくる
    finished_list = Homework.objects.filter(finished=True)
    context = { 'finished_list':finished_list }
    return render(request, 'view/finished-homework.html', context)
