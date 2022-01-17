from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from teacher.models import NGO, NGO_Admin, CHW, Content, User
from django.core import serializers
import datetime
from django.db import IntegrityError
from collections import OrderedDict
from django.core.mail import send_mail, send_mass_mail
from .utils import send_async_mail
from django.views.decorators.csrf import csrf_exempt
import calendar
import hashlib

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
        return redirect("login")

@csrf_exempt
def edit_content(request):
    if request.method == "POST":
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
        print("Haha")

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

def teacher_course(request):
    if request.user.is_authenticated:
        teacher = Teacher.objects.get(user=request.user)
        committes = Committee.objects.filter(teachers=teacher)
        courses = Course.objects.filter(teacher=teacher)

        deadlines = Deadline.objects.none()
        for course in courses:
            deadlines |= Deadline.objects.filter(course=course)

        year = datetime.datetime.now().year
        modalData = {}
        courseSubmissionDue = {}

        for course in courses:
            courseSubmissionDue[course.course_code] = 0
            for deadline in deadlines:
                if str(course.course_code) == str(deadline.course.course_code):
                    if course.course_code in modalData:
                        modalData[course.course_code].append(deadline)
                        print(deadline.status)
                        if deadline.status.lower() == "incomplete":
                            courseSubmissionDue[course.course_code] += 1
                    else:
                        modalData[course.course_code] = list()
                        modalData[course.course_code] = [deadline]
                        if deadline.status.lower() == "incomplete":
                            courseSubmissionDue[course.course_code] += 1
        print(courseSubmissionDue)
        print(courses)
        isHead = teacher.is_head

        return render(
            request,
            "teacher/teacher_course.html",
            {
                "courses": courses,
                "is_committee": len(committes) > 0,
                "deadlines": deadlines,
                "modal_data": modalData,
                "course_submissions": courseSubmissionDue,
                "current_year": str(year),
                "is_head": isHead,
            },
        )
    else:
        return redirect("login")

def teacher_committee(request):
    if request.method == "POST":
        return redirect("committee_edit_deadline")

    if request.user.is_authenticated:
        teacher = Teacher.objects.get(user=request.user)
        committes = Committee.objects.filter(teachers=teacher)
        courses = Course.objects.filter(committee__in=committes)
        year = str(datetime.datetime.now().year)

        members = dict()
        for committee in committes:
            committeeMembers = committee.teachers.all()
            if committee.year == str(year):
                for member in committeeMembers:
                    if committee.committee_id in members:
                        members[committee.committee_id].append(member.name)
                    else:
                        members[committee.committee_id] = [member.name]
        members = OrderedDict(sorted(members.items(), reverse=True))

        deadlines = Deadline.objects.none()
        for course in courses:
            deadlines |= Deadline.objects.filter(
                course=course,
            )
        modalData = {}
        courseSubmissionDue = {}
        for course in courses:
            courseSubmissionDue[course.course_code] = 0
            for deadline in deadlines:
                if str(course.course_code) == str(deadline.course.course_code):
                    if course.course_code in modalData:
                        modalData[course.course_code].append(deadline)
                        courseSubmissionDue[course.course_code] += 1
                    else:
                        modalData[course.course_code] = list()
                        modalData[course.course_code] = [deadline]
                        courseSubmissionDue[course.course_code] += 1
        courses = courses.order_by("-year")
        isHead = teacher.is_head

        return render(
            request,
            "teacher/teacher_committee.html",
            {
                "courses": courses,
                "is_committee": len(committes) > 0,
                "deadlines": deadlines,
                "modal_data": modalData,
                "course_submissions": courseSubmissionDue,
                "committee_members": members,
                "is_head": isHead,
            },
        )
    else:
        return redirect("login")


def teacher_head(request):
    if request.method == "POST":
        deadline_date = request.POST.get("date")
        deadline_details = request.POST.get("details")
        deadline_code = request.POST.get("code")

        year = datetime.datetime.now().year
        year = str(year)

        course = Course.objects.get(course_code=deadline_code, year=year)

        date = datetime.datetime.strptime(deadline_date, "%B %d, %Y")
        date = str(date)
        date = date.split(" ")[0]

        intended_deadline = Deadline.objects.get(
            date=date, details=deadline_details, course=course
        )
        intended_deadline.status = "Completed"
        intended_deadline.save()

    if request.user.is_authenticated:
        teacher = Teacher.objects.get(user=request.user)
        committees = Committee.objects.filter(teachers=teacher)

        courses = Course.objects.filter(teacher=teacher)

        year = datetime.datetime.now()

        deadlinesDue = Deadline.objects.none()
        missedDeadlines = Deadline.objects.none()
        all_courses = Course.objects.all()
        for course in all_courses:
            deadlinesDue |= Deadline.objects.filter(
                course=course, status="incomplete", date__gte = year,
            )
            deadlinesDue |= Deadline.objects.filter(
                course=course, status="Incomplete", date__gte = year,
            )
            missedDeadlines |= Deadline.objects.filter(
                course=course, status="incomplete", date__lt = year,
            )
            missedDeadlines |= Deadline.objects.filter(
                course=course, status="Incomplete", date__lt = year,
            )

        isHead = teacher.is_head

        return render(
            request,
            "teacher/teacher_head.html",
            {
                "deadlines": deadlinesDue,
                "is_committee": True if len(committees) > 0 else False,
                "is_head": isHead,
                "missed_deadlines": missedDeadlines,
            },
        )
    else:
        return redirect("login")


def create_course(request):
    failed = False
    success = False
    if request.method == "POST":
        course_code = request.POST.get("inputCode")
        course_title = request.POST.get("inputCourseName")
        course_credit = request.POST.get("inputCredit")
        course_type = request.POST.get("inputCourseType")
        primary_teacher = request.POST.get("inputTeacher")
        second_setter = request.POST.get("inputSecondSetter")
        year = request.POST.get("inputYear")
        committee = request.POST.get("inputCommittee")
        committee_qset = Committee.objects.get(
            committee_id=committee,
        )
        primary_teacher_code = Teacher.get_code(primary_teacher)
        primary_teacher_qset = Teacher.objects.get(teacher_code=primary_teacher_code)
        second_teacher_code = Teacher.get_code(second_setter)
        second_teacher_qset = Teacher.objects.get(teacher_code=second_teacher_code)
        try:
            new_course = Course.objects.create(
                course_code=course_code,
                course_title=course_title,
                course_credit=course_credit,
                course_type=course_type,
                year=year,
                committee=committee_qset,
            )
            new_course.teacher.add(primary_teacher_qset, second_teacher_qset)
            new_course.save()
            success = True

            user_primary = primary_teacher_qset.user
            user_secondary = second_teacher_qset.user

            # --------- Sending Email ---------------#
            mail_body = f"""Dear Instructor,  
                            You have been assigned to the new course {course_title}, under the committee {committee}.
                            Course Details : 
                            - Title : {course_title} 
                            - Credit : {course_credit}
                            - Year : {year}
                            - Instructor : {primary_teacher_qset.name}
                            - Secondary Setter : {second_teacher_qset.name} / {user_secondary.email}
                            """
            mail_body = [x.strip() for x in mail_body.splitlines()]
            mail_body = "\n".join(mail_body).strip()
            automated_mail = (
                "SUST COURSE TRACKER",
                mail_body,
                "from@example.com",
                [user_primary.email, user_secondary.email],
            )
            send_async_mail(automated_mail)

        except IntegrityError as e:
            failed = True
            print("Failed")

    if request.user.is_authenticated:
        teacher = Teacher.objects.get(user=request.user)
        teacherList = Teacher.objects.all()
        committees = Committee.objects.filter(teachers=teacher)
        currentYear = str(datetime.datetime.now().year)

        isHead = teacher.is_head
        return render(
            request,
            "teacher/create_course.html",
            {
                "is_committee": True,
                "teacher_list": teacherList,
                "committees": committees,
                "current_year": currentYear,
                "success": success,
                "failed": failed,
                "is_head": isHead,
            },
        )
    else:
        return redirect("login")


def create_deadline(request):
    failed = False
    success = False
    if request.method == "POST":
        course_code = request.POST.get("inputCourse")
        deadline_date = request.POST.get("inputDate")
        deadline_details = request.POST.get("inputDetails")
        year = str(datetime.datetime.now().year)
        course = Course.objects.get(course_code=course_code, year=year)
        teachers = course.teacher.all()
        try:
            new_deadline = Deadline.objects.create(
                date=deadline_date,
                details=deadline_details,
                course=course,
            )
            new_deadline.save()
            success = True
            failed = False

            # #--------- Sending Email ---------------#
            reciever_emails = [teacher.user.email for teacher in teachers]
            mail_body = f"""Dear Instructor,
                            A new deadline has been assigned to your course {course_code}.
                            Due : {deadline_date}
                            Details : {deadline_details}
                            """
            mail_body = [x.strip() for x in mail_body.splitlines()]
            mail_body = "\n".join(mail_body).strip()
            automated_mail = (
                "SUST COURSE TRACKER",
                mail_body,
                "from@example.com",
                reciever_emails,
            )
            send_async_mail(automated_mail)
        except:
            success = False
            failed = True

    if request.user.is_authenticated:
        teacher = Teacher.objects.get(user=request.user)
        committees = Committee.objects.filter(teachers=teacher)
        courses = Course.objects.none()
        for committee in committees:
            courses |= Course.objects.filter(committee=committee)

        year = str(datetime.datetime.now().year)
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        isHead = teacher.is_head
        return render(
            request,
            "teacher/create_deadline.html",
            {
                "is_committee": True,
                "courses": courses,
                "current_year": year,
                "success": success,
                "failed": failed,
                "current_date": date,
                "success": success,
                "failed": failed,
                "is_head": isHead,
            },
        )
    else:
        return redirect("login")

def create_committee(request):
    failed = False
    success = False
    if request.method == "POST":
        committee_members = request.POST.getlist("inputMembers")
        semester = request.POST.get("inputSemester")
        checkExists = Committee.objects.filter(semester=semester, year=str(datetime.datetime.now().year)).count()
        try:
            if checkExists:
                raise IntegrityError("Committee Already exists")
            new_committee = Committee.objects.create(
                semester=semester,
            )

            for member in committee_members:
                member_code = Teacher.get_code(member)
                member_qset = Teacher.objects.get(teacher_code=member_code)
                new_committee.teachers.add(member_qset)
            new_committee.save()
            success = True
            failed = False
        except IntegrityError:
            failed = True
            success = False

    
    if request.user.is_authenticated:
        teacher = Teacher.objects.get(user=request.user)
        isHead = teacher.is_head
        if isHead:
            teachers = Teacher.objects.all()
            return render(
                request,
                "teacher/create_committee.html",
                {
                    "is_committee": True,
                    "success": success,
                    "failed": failed,
                    "is_head": isHead,
                    "teacher_list": teachers,
                },
            )
        else:
            return redirect("landing")
    else:
        return redirect("login")

@csrf_exempt
def edit_deadline(request):
    month_dict={
        "Jan.": "01",
        "Feb.": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "Aug.": "08",
        "Sept.": "09",
        "Oct.": "10",
        "Nov.": "11",
        "Dec.": "12",
    }
    date = None
    details = None
    status = None
    code = None
    success = False
    failed = False
    if request.method == "POST":
        if request.POST["from"]=="committee":
            date = request.POST.get("date")
            details = request.POST.get("details")
            status = request.POST.get("status")
            code = request.POST.get("code")
            month = date.split(" ")[0]
            month = month_dict[month]
            date_numb = date.split(" ")[1]
            date_numb = date_numb.split(",")[0]
            year = date.split(" ")[2]            
            date = str(year)+"-"+str(month)+"-"+str(date_numb)

        if request.POST["from"]=="deadline":
            date = request.POST.get("old_date")
            details = request.POST.get("old_details")
            status = request.POST.get("old_status")
            new_date = request.POST.get("inputDate")
            new_details = request.POST.get("inputDetails")
            new_status = request.POST.get("status")
            new_code = request.POST.get("inputCourse")
            new_year = new_date.split("-")[0]            
            try:
                course = Course.objects.get(
                    course_code=new_code, 
                    year=new_year)

                edit_deadline = Deadline.objects.get(
                    date=date,
                    details=details,
                    course=course,
                    status=status,
                )
                
                edit_deadline.date = new_date
                edit_deadline.details = new_details
                edit_deadline.status = new_status

                edit_deadline.save()

                date = new_date
                details = new_details
                status = new_status
                code = new_code
                success = True
                failed = False
            except:
                failed = True
                success = False


    if request.user.is_authenticated:
        teacher = Teacher.objects.get(user=request.user)
        year = str(datetime.datetime.now().year)
        isHead = teacher.is_head
        
        if date and details and status and code:
            return render(
                request, 
                "teacher/edit_deadlines.html",
                {
                    "is_committee": True,
                    "current_year": year,
                    "current_date": date,
                    "is_head": isHead,
                    "course_name" : code,
                    "details": details,
                    "status": status,
                    "success": success,
                    "failed": failed,
                }
                )
        else:
            return redirect("teacher_committee")
    else:
        return redirect("login")