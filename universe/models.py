from django.db import models
from .enums import JobRoleType


class Movie(models.Model):
    """ Model for every Movie of the StarWars universe """
    name = models.CharField(max_length=100, blank=False, null=False)
    opening_crawl = models.TextField(blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Character(models.Model):
    """ Model for every character in StarWars movies """
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Planet(models.Model):
    """ Model for every planet imagined in StarWars """
    name = models.CharField(max_length=100, blank=False, null=False)
    movies = models.ManyToManyField(Movie,
                                    related_name='planets')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Person(models.Model):
    """ Interface for all real human persons involved in StarWars
        as Directors, stuff, producers, actors. """
    name = models.CharField(max_length=100, null=False, blank=False)
    job_role = models.CharField(max_length=3, null=False, blank=False,
                                choices=JobRoleType.choices,
                                default=JobRoleType)
    movies = models.ManyToManyField(Movie, related_name='persons')

    class Meta:
        ordering = ['job_role']

    def __str__(self):
        return f'{self.name} - {self.get_job_role_display()}'
