from datetime import date
from statistics import mode
import django.dispatch
from django.db import models

from customuser.models import User
from .utils import get_random_id

class NGO(models.Model):
    ngo_name = models.CharField(max_length=50, blank=False, unique=True)
    ngo_shortCode = models.CharField(max_length=10, blank=False, unique=True)
    contact_point = models.CharField(max_length=32)

    def __str__(self):
        return self.ngo_shortCode

class NGO_Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=254, null=True, blank=True)
    region = models.CharField(max_length=64)
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - " + self.ngo.ngo_name

class CHW(models.Model):
    id = models.CharField(max_length=20, blank=False)
    name = models.CharField(max_length=128)
    age = models.IntegerField()
    region = models.CharField(max_length=20)
    access_token = models.CharField(max_length=128, blank=False, primary_key=True)
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    addedBy = models.ForeignKey(NGO_Admin, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name + "_" + self.id

class Content(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(blank=False, max_length=1024)
    details = models.TextField(blank=True, max_length=2056)
    tags = models.TextField(blank=True, max_length=512,default='')
    associated_link = models.CharField(blank=True, max_length=512,default='')

    added_by = models.ForeignKey(
        NGO_Admin,
        on_delete=models.SET_DEFAULT,
        default="unassigned",
    )
    date = models.DateField(auto_now=False, auto_now_add=False)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ("date",)

    def __str__(self):
        return str(self.id) + "-" + str(self.title)

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(blank=False, max_length=1024)
    quizzes = models.TextField(blank=True, max_length=8192)
    tags = models.TextField(blank=True, max_length=512,default='')

    added_by = models.ForeignKey(
        NGO_Admin,
        on_delete=models.SET_DEFAULT,
        default="unassigned",
    )
    date = models.DateField(auto_now=False, auto_now_add=False)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ("date",)

    def __str__(self):
        return str(self.id) + "-" + str(self.title)
