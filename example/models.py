from django.db import models

# Create your models here.
class user_message(models.Model):
    uid = models.CharField(max_length=50, null=False, primary_key=True)  # user id
    name = models.CharField(max_length=50, blank=True, null=False) # LINE 名字
    message = models.CharField(max_length=600, blank=True, null=False) # 文字訊息紀錄
    time = models.DateTimeField(auto_now=True) # 日期時間

    def __str__(self):
        return self.name # print the user name in terminal