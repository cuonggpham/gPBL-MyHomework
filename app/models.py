from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Homework(models.Model):
    user = models.ForeignKey(User, null=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200) #宿題名
    note = models.TextField(blank=True, default='') #メモ
    due_date = models.DateField() #期限
    difficulty = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]) #難易度
    priority = models.IntegerField(default=0, editable=False) #自動的に計算する優先度
    finished = models.BooleanField(default=False) #完了した宿題かどうか

    def save(self, *args, **kwargs):
        # priorityの計算、(入力された期限ー今の時間)＊(５－入力された難易度)
        now = timezone.now()
        time_difference = (self.due_date - now.date()).days
        self.priority = time_difference * (5 - self.difficulty)
        super().save(*args, **kwargs)

    def __str__(self):
        #管理画面で宿題の名前が表示されるように設定している
        return self.name