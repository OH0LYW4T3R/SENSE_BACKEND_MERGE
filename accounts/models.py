from django.db import models


# Create your models here.
class KakaoUser(models.Model):
    kakao_id = models.CharField(verbose_name="Kakao Name", max_length=128)
    nickname = models.CharField(verbose_name="Sense NickName", max_length=128)
    post_count = models.IntegerField(verbose_name="Post Count")

class Post(models.Model):
    title = models.CharField(verbose_name="Title", max_length=128)
    content = models.CharField(verbose_name="content", max_length=128)
    report_count = models.IntegerField(verbose_name="Report Count")
    kakao_user = models.ForeignKey(to='KakaoUser', on_delete=models.CASCADE)
