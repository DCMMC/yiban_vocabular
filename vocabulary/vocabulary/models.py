from django.db import models
import json


class YibanUser(models.Model):
    yiban_user_id = models.CharField(max_length=64, primary_key=True)
    # 今天背单词数
    today = models.IntegerField()
    # 历史背单词数, json 数据
    history = models.CharField(max_length=10000, default=json.dumps({}))
