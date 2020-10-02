from django.db import models


class JobRoleType(models.TextChoices):
    DIRECTOR = 'DIR', 'Director'
    PRODUCER = 'PDR', 'Producer'
