from django.db import models


class MarkerPosition(models.Model):
    title = models.CharField(max_length=70, default = "마커") #이름
    content = models.TextField(default = "마커 내용")  #내용
    create_date = models.DateTimeField()  # 생성 날짜
    lat = models.FloatField() # 위도
    lng = models.FloatField() # 경도
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lat', 'lng'],
                name="unique_position",

            ),
        ]