import json
import mimetypes
from statistics import mode
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from teacher import models
from teacher.models import NGO, NGO_Admin, CHW, Content, User
import datetime
from django.db import IntegrityError
from collections import OrderedDict
from django.core.mail import send_mail, send_mass_mail
from .utils import send_async_mail
from django.views.decorators.csrf import csrf_exempt
import calendar
import hashlib
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict

def ngo_admin_home(request):
    if request.method == "POST":
        return redirect("ngo_admin_edit_content")
        
    if request.user.is_authenticated:
        ngo_admin = NGO_Admin.objects.get(user=request.user)
        contents = Content.objects.filter(added_by=ngo_admin)

        campaignDeadlineOver = Content.objects.filter(
            added_by=ngo_admin,
            date__lt=datetime.datetime.now().date()
            )
        
        campaignDeadlineFuture = Content.objects.filter(
            added_by=ngo_admin,
            date__gte=datetime.datetime.now().date()
            )
                
        return render(
            request,
            "teacher/ngo_admin_dashboard.html",
            {
                "is_ngo_admin": True,
                "future_campaign": campaignDeadlineFuture,
                "past_campagin": campaignDeadlineOver,
            },
        )
    else:
        print("Not Authenticated")
        return redirect("login")


def ngo_admin_profile(request):
    if request.method == "POST":
        return redirect("ngo_admin_edit_content")

    if request.user.is_authenticated:
        ngo_admin = NGO_Admin.objects.get(user=request.user)
        ngo_admin_user = ngo_admin.user

        return render(
            request,
            "teacher/ngo_admin_profile.html",
            {
                "is_ngo_admin": True,
                "content": ngo_admin,
                "admin_user": ngo_admin_user
            },
        )
    else:
        print("Not Authenticated")
        return redirect("login")


def update_profile(request):
    failed = False
    success = False
    if request.method == "POST":
        email = request.POST.get("inputEmail")
        name = request.POST.get("inputName")

        print(name)

        selectedUser = User.objects.get(email=email)
        selectedNGOAdmin = NGO_Admin.objects.get(user=selectedUser)
        try:
            selectedNGOAdmin.name = name

            selectedNGOAdmin.save()
            success = True
            failed = False

        except Exception as e:
            print(e)
            success = False
            failed = True

    if request.user.is_authenticated:

        ngo_admin = NGO_Admin.objects.get(user=request.user)
        contents = Content.objects.filter(added_by=ngo_admin)

        campaignDeadlineOver = Content.objects.filter(
            added_by=ngo_admin,
            date__lt=datetime.datetime.now().date()
        )

        campaignDeadlineFuture = Content.objects.filter(
            added_by=ngo_admin,
            date__gte=datetime.datetime.now().date()
        )

        return render(
            request,
            "teacher/ngo_admin_dashboard.html",
            {
                "is_ngo_admin": True,
                "future_campaign": campaignDeadlineFuture,
                "past_campagin": campaignDeadlineOver
            },
        )
    else:
        return redirect("login")

@csrf_exempt
def edit_content(request):
    if request.method == "POST":
        print("Chole Elam")
        print(request.POST.get("id"))
        print(request.POST.get("title"))
        print(request.POST.get("details"))

        selectedCampaign = Content.objects.get(id=request.POST.get("id"))
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))

    return render(
        request,
        "teacher/ngo_admin_edit_content.html",
        {
            "entry": selectedCampaign,
            "current_date": date,
        },
    )

def update_content(request):
    failed = False
    success = False
    if request.method == "POST":
        title = request.POST.get("inputContentTitle")
        url = request.POST.get("inputContentLink")
        details = request.POST.get("inputCampaignDetails")
        date = request.POST.get("inputDate")
        
        print(request.POST.get("id"))

        selectedCampaign = Content.objects.get(id=request.POST.get("id"))
        try:
            selectedCampaign.title = title
            selectedCampaign.associated_link = url
            selectedCampaign.details = details
            selectedCampaign.date = date

            selectedCampaign.save()
            success = True
            failed = False

        except Exception as e:
            print(e)
            success = False
            failed = True

    if request.user.is_authenticated:

        ngo_admin = NGO_Admin.objects.get(user=request.user)
        contents = Content.objects.filter(added_by=ngo_admin)

        campaignDeadlineOver = Content.objects.filter(
            added_by=ngo_admin,
            date__lt=datetime.datetime.now().date()
        )

        campaignDeadlineFuture = Content.objects.filter(
            added_by=ngo_admin,
            date__gte=datetime.datetime.now().date()
        )

        return render(
            request,
            "teacher/ngo_admin_dashboard.html",
            {
                "is_ngo_admin": True,
                "future_campaign": campaignDeadlineFuture,
                "past_campagin": campaignDeadlineOver,
            },
        )
    else:
        return redirect("login")


def create_content(request):
    failed = False
    success = False
    if request.method == "POST":
        title = request.POST.get("inputContentTitle")
        url = request.POST.get("inputContentLink")
        details = request.POST.get("inputCampaignDetails")
        date = request.POST.get("inputDate")

        added_by = NGO_Admin.objects.get(user=request.user)
        try:
            new_content = Content.objects.create(
                title = title,
                details = details,
                associated_link = url,
                added_by = added_by,
                date = date,
            )
            new_content.save()
            success = True
            failed = False

        except Exception as e:
            print(e)
            success = False
            failed = True

    if request.user.is_authenticated:

        year = str(datetime.datetime.now().year)
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        return render(
            request,
            "teacher/ngo_admin_create_content.html",
            {
                "is_ngo_admin": True,
                "current_year": year,
                "current_date": date,
                "success": success,
                "failed": failed,
            },
        )
    else:
        return redirect("login")

def ngo_admin_chw(request):
    if request.method == "POST":
        return redirect("ngo_admin_edit_chw")
        
    if request.user.is_authenticated:
        ngo_admin = NGO_Admin.objects.get(user=request.user)
        chws = CHW.objects.filter(addedBy=ngo_admin)
                
        return render(
            request,
            "teacher/ngo_admin_chw.html",
            {
                "is_ngo_admin": True,
                "health_workers": chws,
            },
        )
    else:
        return redirect("login")

@csrf_exempt
def edit_chw(request):
    if request.method == "POST":
        print(request.POST.get("id"))
        print(request.POST.get("name"))
        print(request.POST.get("age"))
        print(request.POST.get("region"))


        selectedCHW = CHW.objects.get(id=request.POST.get("id"))
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))

        print(selectedCHW.name)
    return render(
        request,
        "teacher/ngo_admin_edit_chw.html",
        {
            "entry": selectedCHW,
            "current_date": date,
        },
    )


def update_chw(request):
    failed = False
    success = False
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("inputName")
        age = request.POST.get("inputAge")
        region = request.POST.get("inputRegion")

        print(request.POST.get("id"))
        print("Haha")

        selectedCHW = CHW.objects.get(id=request.POST.get("id"))
        try:
            selectedCHW.id = id
            selectedCHW.name = name
            selectedCHW.age = age
            selectedCHW.region = region

            selectedCHW.save()
            success = True
            failed = False

        except Exception as e:
            print(e)
            success = False
            failed = True

    if request.user.is_authenticated:

        ngo_admin = NGO_Admin.objects.get(user=request.user)
        chws = CHW.objects.filter(addedBy=ngo_admin)

        return render(
            request,
            "teacher/ngo_admin_chw.html",
            {
                "is_ngo_admin": True,
                "health_workers": chws,
            },
        )
    else:
        return redirect("login")

def create_chw(request):
    failed = False
    success = False
    if request.method == "POST":
        id = request.POST.get("inputID")
        name = request.POST.get("inputName")
        age = request.POST.get("inputAge")
        region = request.POST.get("inputRegion")
        
        added_by = NGO_Admin.objects.get(user=request.user)
        ngo = added_by.ngo

        concat = str(id)+"-"+str(name)+"-"+str(ngo.ngo_name)+"-"+str(added_by.name)
        access_token = hashlib.md5(concat.encode('utf-8')).hexdigest()

        try:
            new_chw = CHW.objects.create(
                id = id,
                name = name,
                age = age,
                region = region,
                access_token=access_token,
                ngo = ngo,
                addedBy = added_by,
            )
            new_chw.save()
            success = True
            failed = False

        except Exception as e:
            print(e)
            success = False
            failed = True
        return render(
            request,
            "teacher/ngo_admin_create_chw.html",
            {
                "is_ngo_admin": True,
                "success": success,
                "failed": failed,
            },
        )

    if request.user.is_authenticated:

        year = str(datetime.datetime.now().year)
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        return render(
            request,
            "teacher/ngo_admin_create_chw.html",
            {
                "is_ngo_admin": True,
                "current_year": year,
                "current_date": date,
                "success": success,
                "failed": failed,
            },
        )
    else:
        return redirect("login")

def super_admin_home(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        ngo_list = NGO.objects.all()

        return render(
            request,
            "teacher/super_admin_dashboard.html",
            {
                "ngo_list" : ngo_list,
                "is_superadmin": request.user.is_superadmin,
            }
        )

def create_ngo(request):
    failed = False
    success = False
    if request.method == "POST":
        name = request.POST.get("inputName")
        shortcode = request.POST.get("inputShortCode")
        contactpoint = request.POST.get("inputContactPoint")

        try:
            new_ngo = NGO.objects.create(
                ngo_name = name,
                ngo_shortCode = shortcode,
                contact_point = contactpoint,
            )
            new_ngo.save()
            success = True
            failed = False

        except Exception as e:
            print(e)
            success = False
            failed = True

    if request.user.is_authenticated and request.user.is_superadmin:
        return render(
            request,
            "teacher/super_admin_create_ngo.html",
            {
                "is_superadmin": request.user.is_superadmin,
                "success": success,
                "failed": failed,
            }
        )
    else:
        return redirect("login")

@csrf_exempt
def edit_ngo(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        print(request.POST.get("name"))
        print(request.POST.get("shortcode"))
        print(request.POST.get("contactpoint"))

        selectedNGO = NGO.objects.get(ngo_name=request.POST.get("name"))

        return render(
            request,
            "teacher/super_admin_edit_ngo.html",
            {
                "is_superadmin": request.user.is_superadmin,
                "entry": selectedNGO,
            },
        )

def update_ngo(request):
    failed = False
    success = False
    if request.method == "POST":
        name = request.POST.get("inputName")
        shortcode = request.POST.get("inputShortCode")
        contactpoint = request.POST.get("inputContactPoint")

        print(request.POST.get("inputContactPoint"))

        selectedNGO = NGO.objects.get(ngo_name=request.POST.get("inputName"))
        print(selectedNGO.contact_point, contactpoint)
        try:
            selectedNGO.ngo_name = name
            selectedNGO.ngo_shortCode = shortcode
            selectedNGO.contact_point = contactpoint

            print(selectedNGO.contact_point, contactpoint)
            selectedNGO.save()
            success = True
            failed = False

        except Exception as e:
            print(e)
            success = False
            failed = True

    if request.user.is_authenticated and request.user.is_superadmin:
        ngo_list = NGO.objects.all()

        return render(
            request,
            "teacher/super_admin_dashboard.html",
            {
                "ngo_list": ngo_list,
                "is_superadmin": request.user.is_superadmin
            }
        )
    else:
        return redirect("login")

def delete_ngo(request, pk):
    failed = False
    success = False

    selectedNGO = NGO.objects.get(ngo_shortCode=pk)
    selectedNGO.delete()
    if request.user.is_authenticated and request.user.is_superadmin:
        ngo_list = NGO.objects.all()
        
        return redirect("/ngo_admin/super_admin_home")

        # return render(
        #     request,
        #     "teacher/super_admin_dashboard.html",
        #     {
        #         "ngo_list": ngo_list,
        #         "is_superadmin": request.user.is_superadmin
        #     }
        # )
    else:
        return redirect("login")

def super_admin_ngo_member(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        ngo_admins = NGO_Admin.objects.all()

        return render(
            request,
            "teacher/super_admin_ngo_member.html",
            {
                "is_superadmin": request.user.is_superadmin,
                "ngo_members": ngo_admins,
            }
        )

def create_ngo_admin(request):
    failed = False
    success = False

    if request.method == "POST":
        email = request.POST.get("inputEmail")
        password = request.POST.get("inputPassword")
        name = request.POST.get("inputName")
        area = request.POST.get("inputRegion")
        ngo = request.POST.get("inputNGO")

        ngoShortCode = ngo.split("-")[1].strip()

        selectedNgo = NGO.objects.get(ngo_shortCode= ngoShortCode)

        try:
            new_user = User.objects.create(
                email = email,
                password = password,
                is_superadmin = False,
            )

            new_user.set_password(password)
            new_user.save()

            new_ngo_admin = NGO_Admin.objects.create(
                user = new_user,
                name = name,
                region = area,
                ngo = selectedNgo,
            )

            new_ngo_admin.save()
            success = True
            failed = False

        except Exception as e:
            print(e)
            success = False
            failed = True

    if request.user.is_authenticated and request.user.is_superadmin:
        ngo_list = NGO.objects.all()

        return render(
            request,
            "teacher/super_admin_create_ngo_admin.html",
            {
                "is_superadmin": request.user.is_superadmin,
                "ngo_list": ngo_list,
                "success": success,
                "failed": failed
            }
        )

@csrf_exempt
def delete_ngo_admin(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        print(request.POST.get("user"))
        selectedUser = User.objects.get(email=request.POST.get("user"))
        selectedNGOAdmin = NGO_Admin.objects.get(user=selectedUser)
        print(selectedNGOAdmin.name)
        selectedNGOAdmin.delete()
        return redirect("/ngo_admin/super_admin_ngo_member")

def verify_access_token(request):
    token = request.GET.get("token")
    try:
        chw = CHW.objects.get(access_token=token)
        return JsonResponse(
            {
                "id":chw.id,
                "name":chw.name,
                "age":chw.age,
                "region":chw.region,
                "ngo":chw.ngo.ngo_name,
                "addedBy":chw.addedBy.name,
            },
            status=200,      
            safe=False
        )
    except CHW.DoesNotExist as e:
        return JsonResponse(
            {
                "response":"Invalid Request",
            },
            status=404,
            safe=False
        )

def get_content(request):
    token = request.GET.get("token")
    try:
        chw = CHW.objects.get(access_token=token)
        ngo_admin = chw.addedBy
        ngo = ngo_admin.ngo
        contents = Content.objects.filter(added_by__ngo=ngo, date__gte=datetime.datetime.now().date())
        content_json = serializers.serialize("json",contents)

        return HttpResponse(
            content_json,
            content_type='application/json',
            status=200,      
        )
    except CHW.DoesNotExist as e:
        return JsonResponse(
            {
                'error': 'The resource was not found'
            },
            status=404,
            safe=False
        )
