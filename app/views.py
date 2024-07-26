from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Homework

def home(request):
    return render(request, 'index.html')

def sign_in(request):
    return render(request, 'view/sign-in.html')
def sign_up(request):
    return render(request, 'view/sign-up.html')

def index_logined(request):
    return render(request, 'view/index-logined.html')

def view_homework(request):
    #引き数でhomework_idが来た場合のみにこのif文を実行（そのhomeworkを削除）
    if request.method == 'POST':
        homework_id = request.POST.get('homework_id')
        if homework_id:
            homework = get_object_or_404(Homework, id=homework_id)
            homework.delete()
    #finishedがFalseのHomeworkのみをデータベースから持ってくる
    homework_list = Homework.objects.filter(finished=False)
    context = { 'homework_list':homework_list }
    return render(request, 'view/view-homework.html', context)

def add_homework(request):
    return render(request, 'view/add-homework.html')

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
