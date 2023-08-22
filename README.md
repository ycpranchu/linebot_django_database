Linebot + Django Database 實作
===

- targets: Linebot + Django framework, database implementation.
- previous post: https://github.com/ycpranchu/linebot_django
- [Django official document](https://docs.djangoproject.com/en/4.2/topics/db/models/)

Overview
---

- Each model is a Python class that subclasses django.db.models.Model.
- Each attribute of the model represents a database field.
- With all of this, Django gives you an automatically-generated database-access API.

建立資料表：models.py
---

舉例 `Person` 資料，屬性為 `first_name` 以及 `last_name`：

```python=
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

執行上述 `Person` model 將會創造一個資料表如下：

```python=
CREATE TABLE myapp_person (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);
```

同理，若我們想從 Linebot 中記錄用戶 ID 以及訊息內容：

```python=
from django.db import models

# Create your models here.
class user_message(models.Model):
    uid = models.CharField(max_length=50, null=False, primary_key=True)  # user id
    name = models.CharField(max_length=50, blank=True, null=False) # LINE 名字
    message = models.CharField(max_length=600, blank=True, null=False) # 文字訊息紀錄
    time = models.DateTimeField(auto_now=True) # 日期時間

    def __str__(self):
        return self.name # print the user name in terminal
```


- `time = models.DateTimeField(auto_now=True)`，當 `auto_now` 為 `true` 時，不僅意味著該欄位的預設值為當前時間，而是表示該欄位將被「強制」更新為當前時間，無法在程式中手動為該欄位賦值，且該欄位在管理員界面中是唯讀的。
- `__str__()`: A Python “magic method” that returns a string representation of any object. This is what Python and Django will use whenever a model instance needs to be coerced and displayed as a plain string. Most notably, this happens when you display an object in an interactive console or in the admin.

後台資料：admin.py
---

from models.py import the database table

```python=
from django.contrib import admin

# Register your models here.
from example.models import *

class user_message_admin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'message', 'time')
admin.site.register(user_message, user_message_admin)
```

### 更新資料庫

```bash=
python manage.py makemigrations
python manage.py migrate
```

資料表操作：views.py
---

將 models.py 資料表匯入 views.py

```python3=
from example.models import *
```

修改 views.py 主要 codespace

```python3
if isinstance(event, MessageEvent):
    uid = event.source.user_id
    profile = line_bot_api.get_profile(uid)
    name = profile.display_name
    text = event.message.text

    message=[]
    if not user_message.objects.filter(uid=uid).exists():
        user_message.objects.create(uid=uid, name=name, message=text)
        message.append(TextSendMessage(text='資料新增完畢'))
    else:
        user_message.objects.filter(uid=uid, name=name).update(message=text, time=datetime.datetime.now())
        # obj = user_message.objects.get(uid=uid)
        # obj.message = text
        # obj.save()                
        message.append(TextSendMessage(text='資料修改完畢'))

    line_bot_api.reply_message(event.reply_token, message)
```

登入 `http://127.0.0.1:8000/admin`，資料新增成功

![Alt text](static/image1.png)

### 關於 `DateTimeField` 自動更新

操作經過 model 層，會自動更新 current time

```python3=
obj = user_message.objects.get(uid=uid)
obj.message = text
obj.save()
```

使用 filter 的 update，因為直接調用 sql 語法，不通過 model 層，需呼叫 `datetime.datetime.now()` 函式更新

```python3=
user_message.objects.filter(uid=uid, name=name).update(message=text, time=datetime.datetime.now())
```

![Alt text](static/image2.png)

Database CRUD (create, read, update, delete)
---

### Create data:

```python3=
Table_name.objects.create(data=data)
```

### Read data:

```python3=
# return list
Table_name.objects.filter(data=data)

# return only one object
Table_name.objects.get(data=data)
```

### Update data:

```python3=
Table_name.objects.filter(data=data, name=name).update(text=new_text)
```

### Delete data:

```python3=
Table_name.objects.filter(data=data).delete()
Table_name.objects.all().delete()
```
