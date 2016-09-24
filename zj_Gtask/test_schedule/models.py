from django.db import models
import django.utils.timezone as timezone

# Create your models here.

#待办事项
class Schedule(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=50)
    #add_time = models.DateTimeField('保存日期',default = timezone.now)
    #mod_time = models.DateTimeField(auto_now = True)
