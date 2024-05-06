from django.db import models


class FavouriteCity(models.Model):
    cognito_user = models.CharField(max_length=100, null=True)
    city_name = models.CharField(max_length=50, null=True)


    def __str__(self) -> str:
        return self






