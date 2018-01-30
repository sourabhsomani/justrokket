# python imports
import json
import datetime
from postmarker.core import PostmarkClient
import random, string
# django imports
from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, View, FormView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages import  add_message
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.shortcuts import render
# app imports
from main import models
from qa.models import Question,Answer
from main import forms
from string import Template
# from ccavutil import encrypt,decrypt
# from twilio.rest import TwilioRestClient
from main import utils
from .utils import send_mail
from django.template import Context, loader
import sys
import math






from django.db import transaction

class Screen6(TemplateView):
    template_name = "screen6.html"

    def get(self, request, *args, **kwargs):
        self.send_mail()
        return super(Screen6, self).get(request, *args, **kwargs)

    def get_selection(self):
        return models.Selection.objects.get(id=self.kwargs['pk'])

    def get_order_obj(self):
        return models.Order.objects.get(selection=self.get_selection())

    def get_profile_obj(self):
        return models.Profile.objects.get(user=self.request.user)

    def send_mail(self):
        profile_obj = self.get_profile_obj()
        order_obj = self.get_order_obj()
        selection = self.get_selection()
        request = self.request
        # Email to college
        email_template = models.EmailTemplate.objects.filter(type="COLLEGE_EMAIL").first()
        subject = email_template.subject
        message = email_template.html
        message = message.replace("*|NAME|*", request.user.email)
        # message = message.replace("*|GOVT_ID_TYPE|*", profile_obj.id_type)
        # message = message.replace("*|GOVT_ID|*", profile_obj.id_no)
        message = message.replace("*|GENDER|*", profile_obj.gender)
        if profile_obj.dob:
            message = message.replace("*|DOB|*", profile_obj.dob.strftime('%m/%d/%Y'))
        message = message.replace("*|ADDRESS|*", profile_obj.get_address())
        message = message.replace("*|VERIFIED_EMAIL|*", profile_obj.user.email)
        message = message.replace("*|VERIFIED_MOBILE|*", profile_obj.user.profile.mobile)
        message = message.replace("*|AMOUNT|*", str(order_obj.amount))
        message = message.replace("*|NEXT_SELECTION_STEPS|*", selection.college_qualification.next_selection_steps)
        message = message.replace("*|SELECTION_WITHIN_DAYS|*", str(selection.college_qualification.nst_closure_within))
        message = message.replace("*|COURSE_SELECTED|*", selection.course_name)
        message = message.replace("*|INSTITUTION_ADDRESS|*", selection.college.institution_address())
        message = message.replace("*|SESSION|*", selection.college_qualification.session.get_session())
        message = message.replace("*|SCHOLARSHIP|*", selection.scholarship)
        message = message.replace("*|STUDENT_NAME|*", request.user.profile.name)
        send_mail(
            subject=subject,
            message=message,
            recipient_list=[str(selection.college.email)],
        )

        email_template = models.EmailTemplate.objects.filter(type="PURCHASEDSCHL").first()
        subject = email_template.subject
        message = email_template.html
        message = message.replace("*|NAME|*", request.user.email)
        message = message.replace("*|INSTITUTION_NAME|*", selection.college.name)
        message = message.replace("*|INSTITUTION_ADDRESS|*", selection.college.institution_address())
        message = message.replace("*|COURSE_SELECTED|*", selection.course_name)
        message = message.replace("*|SESSION|*", selection.college_qualification.session.get_session())
        message = message.replace("*|STUDENT_NAME|*", profile_obj.name)
        message = message.replace("*|COURSE_NAME|*", selection.course_name)
        message = message.replace("*|SCHOLARSHIP|*", selection.scholarship)
        message = message.replace("*|FINAL_FEE|*", selection.final_fee)
        message = message.replace("*|SELECTION_WITHIN_DAYS|*", str(selection.college_qualification.nst_closure_within))
        message = message.replace("*|NEXT_SELECTION_STEPS|*", str(selection.college_qualification.next_selection_steps))
        send_mail(
            subject=subject,
            message=message,
            recipient_list=[str(request.user.email)],
        )
        if profile_obj.parent_email and profile_obj.parent_email != "":
            email_template = models.EmailTemplate.objects.filter(type="PARENTEMAIL").first()
            subject = email_template.subject
            message = email_template.html
            message = message.replace("*|NAME|*", request.user.email)
            message = message.replace("*|INSTITUTION_NAME|*", selection.college.name)
            message = message.replace("*|INSTITUTION_ADDRESS|*", selection.college.institution_address())
            message = message.replace("*|COURSE_SELECTED|*", selection.course_name)
            message = message.replace("*|SESSION|*", selection.college_qualification.session.get_session())
            message = message.replace("*|STUDENT_NAME|*", profile_obj.name)
            message = message.replace("*|COURSE_NAME|*", selection.course_name)
            message = message.replace("*|SCHOLARSHIP|*", selection.scholarship)
            message = message.replace("*|FINAL_FEE|*", str(selection.final_fee))
            message = message.replace("*|SELECTION_WITHIN_DAYS|*",
                                      str(selection.college_qualification.nst_closure_within))
            message = message.replace("*|NEXT_SELECTION_STEPS|*",
                                      str(selection.college_qualification.next_selection_steps))
            send_mail(
                subject=subject,
                message=message,
                recipient_list=[str(request.user.profile.parent_email)],
            )


class BlogView(TemplateView):
    template_name = "blog.html"

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class BlogdetailsView(TemplateView):
    template_name = "blog-details.html"

    def get_context_data(self, **kwargs):
        context = super(BlogdetailsView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context



class admissions1(TemplateView):
    from django.db.models import Q
    template_name = "allprofile.html"
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['experts'] = models.Profile.objects.filter(~Q(user_type="A"))
        print(context['experts'])
        return context


class HomeViewNew(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super(HomeViewNew, self).get_context_data(**kwargs)
        context['experts'] = models.Profile.objects.filter(~Q(user_type="A"))[:15] 
        context['applicants'] = models.Profile.objects.filter(Q(user_type="A"))[:4]
        return context

    def get(self, request, *args, **kwargs):
        self.college_code()
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return super(HomeViewNew, self).get(request, *args, **kwargs)
        
    

    def get_p_colleges(self):
        return models.PartnerCollege.objects.filter(homepage_display=True)

    def get_rokketeers(self):
        return models.Rokketeer.objects.filter(homepage_display=True)

    def college_code(self):
        for college in models.College.objects.all():
            if not college.code:
                college.code = college.name[:2].upper() + str(college.id)
                college.save()


class HomeView(TemplateView):
    template_name = "admission.html"

    def get(self, request, *args, **kwargs):
        self.college_code()
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_cities(self):
        return models.City.objects.all()

    def get_categories(self):
        cats = []
        for item in models.Qualification.objects.all():
            cats.append({'category': item.course_category})
        return cats

    def get_courses(self):
        return models.Course.objects.all()

    def get_qualifying_exams(self):
        return models.QualifyingExam.objects.all()

    def get_c_exams(self):
        return models.CompetitiveExam.objects.all()

    def get_user(self):
        if self.request.user.is_authenticated:
            return self.request.user

    def get_p_colleges(self):
        return models.PartnerCollege.objects.filter(homepage_display=True)

    def get_rokketeers(self):
        return models.Rokketeer.objects.filter(homepage_display=True)

    def college_code(self):
        for college in models.College.objects.all():
            if not college.code:
                college.code = college.name[:2].upper() + str(college.id)
                college.save()


class ExplorePost(FormView):
    form_class = forms.ExploreForm

    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)
        print(self.request.POST)
        response = super(ExplorePost, self).form_invalid(form)
        return response

    def form_valid(self, form):
        print("Form is valid")
        print(self.request.POST)
        print(self.request.POST.get("course"))
        screen_6_text = ""
        level = self.request.POST.get("level")
        city = self.request.POST.get("city")
        course_type = self.request.POST.getlist("course_type")[0]
        try:
            course = models.Course.objects.get(search_code=self.request.POST.get("course"))
        except Exception as e:
            course = models.Qualification.objects.get(search_code=self.request.POST.get('course'))
        q_exm = self.request.POST.get("q_exm") # if self.request.POST.get("q_exm") else models.QualifyingExam.objects.first().id #FIXME: Why was this done?
        q_exm_score = int(math.floor(float(self.request.POST.get("q_exm_score")))) if self.request.POST.get("q_exm_score") else 0

        if q_exm == "" or q_exm_score == 0:
            # create Event1
            screen_6_text = utils.SCREEN_6_TEXT
        compt_exm_type_1 = self.request.POST.get("compt_exm_type_1")
        compt_exm_score_1 = int(math.floor(float(self.request.POST.get("compt_exm_score_1")))) if self.request.POST.get("compt_exm_score_1") else 0
        compt_exm_type_2 = self.request.POST.get("compt_exm_type_2")
        compt_exm_score_2 = int(math.floor(float(self.request.POST.get("compt_exm_score_2")))) if self.request.POST.get("compt_exm_score_2") else 0
        compt_exm_type_3 = self.request.POST.get("compt_exm_type_3")
        compt_exm_score_3 = self.request.POST.get("compt_exm_score_3")
        compt_exm_type_4 = self.request.POST.get("compt_exm_type_4")
        compt_exm_score_4 = self.request.POST.get("compt_exm_score_4")
        compt_exm_type_5 = self.request.POST.get("compt_exm_type_5")
        compt_exm_score_5 = self.request.POST.get("compt_exm_score_5")
        check_course_obj = models.Course.objects.filter(name=course_type)
        if len(check_course_obj):
            course_type = "cor"
            course = course.id
        check_qualification_obj = models.Qualification.objects.filter(course_category=course_type)
        if len(check_qualification_obj):
            course_type = "cat"
            course = course.course_category
        a = models.Search.objects.create(
            level=level,
            city=city,
            course_type=course_type,
            course=course,
            q_exm=q_exm,
            q_exm_score=q_exm_score,
            compt_exm_score_1=compt_exm_score_1,
            compt_exm_score_2=compt_exm_score_2,
            compt_exm_score_3=compt_exm_score_3,
            compt_exm_score_4=compt_exm_score_4,
            compt_exm_score_5=compt_exm_score_5,
            compt_exm_type_1=compt_exm_type_1,
            compt_exm_type_2=compt_exm_type_2,
            compt_exm_type_3=compt_exm_type_3,
            compt_exm_type_4=compt_exm_type_4,
            compt_exm_type_5=compt_exm_type_5,
            screen_6_text=screen_6_text
        )
        return HttpResponseRedirect("/explore/"+str(a.id))


class Explore(TemplateView):
    template_name = "colleges.html"

    def get(self, request, *args, **kwargs):
        if request.session.get('next'):
            del request.session['next']
        self.request.session['next'] = request.get_full_path()
        print("Search!", self.request.session)
        return super(Explore, self).get(request, *args, **kwargs)

    def get_search(self):
        return self.kwargs['id']

    def get_max_value(self):
        value = 0
        for item in self.get_results():
            print(item)
            if int(item['final_fee']) > value:
                value = item['final_fee']
        return value + 1

    def sort_colleges(self, colleges):
        array1 = []
        for college in colleges:
            if int(college.pop_score) == 5:
                print("Sorted amd added colleges with pop score 5")
                array1.append(college)

        # Make QS out of array1
        array1IDs = []
        for college in array1:
            array1IDs.append(college.id)

        array1QS = models.College.objects.filter(id__in=array1IDs).order_by('-seats', '-weight')
        array1 = list(array1QS)

        array1_1 = []
        for college in colleges:
            if int(college.pop_score) == 4:
                print("Sorted amd added colleges with pop score 4")
                array1_1.append(college)

        # Make QS out of array1
        array1_1IDs = []
        for college in array1_1:
            array1_1IDs.append(college.id)

        array1_1QS = models.College.objects.filter(id__in=array1_1IDs).order_by('-seats', '-weight')
        array1_1 = list(array1_1QS)

        array2 = []
        for college in colleges:
            if int(college.pop_score) == 3:
                print("Sorted amd added colleges with pop score 3")
                array2.append(college)

        # Make QS out of array2
        array2IDs = []
        for college in array2:
            array2IDs.append(college.id)

        array2QS = models.College.objects.filter(id__in=array2IDs).order_by('-seats', '-weight')
        array2 = list(array2QS)

        array3_5 = []
        for college in colleges:
            if int(college.weight) == 5 and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt 5 and pop score not 3 4 or 5")
                array3_5.append(college)

        # Make QS our of array 3_5
        array3_5IDs = []
        for college in array3_5:
            array3_5IDs.append(college.id)

        array3_5QS = models.College.objects.filter(id__in=array3_5IDs).order_by('-pop_score')
        array3_5 = list(array3_5QS)

        array3_4 = []
        for college in colleges:
            if int(college.weight) == 4 and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt 4 and pop score not 3 4 or 5")
                array3_4.append(college)

        # Make QS our of array 3_4
        array3_4IDs = []
        for college in array3_4:
            array3_4IDs.append(college.id)

        array3_4QS = models.College.objects.filter(id__in=array3_4IDs).order_by('-pop_score')
        array3_4 = list(array3_4QS)

        array3_3 = []
        for college in colleges:
            if int(college.weight) == 3 and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt 3 and pop score not 3 4 or 5")
                array3_4.append(college)

        # Make QS our of array 3_3
        array3_3IDs = []
        for college in array3_3:
            array3_3IDs.append(college.id)

        array3_3QS = models.College.objects.filter(id__in=array3_3IDs).order_by('-pop_score')
        array3_3 = list(array3_3QS)

        array3_2 = []
        for college in colleges:
            if int(college.weight) == 2 and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt 2 and pop score not 3 4 or 5")
                array3_2.append(college)

        # Make QS our of array 3_2
        array3_2IDs = []
        for college in array3_2:
            array3_2IDs.append(college.id)

        array3_2QS = models.College.objects.filter(id__in=array3_2IDs).order_by('-pop_score')
        array3_2 = list(array3_2QS)

        array3_1 = []
        for college in colleges:
            if int(college.weight) in [0, 1] and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt 0 or 1 and pop score not 3 4 or 5")
                array3_1.append(college)

        # Make QS our of array 3_1
        array3_1IDs = []
        for college in array3_1:
            array3_1IDs.append(college.id)

        array3_1QS = models.College.objects.filter(id__in=array3_1IDs).order_by('-pop_score')
        array3_1 = list(array3_1QS)

        array3_m1 = []
        for college in colleges:
            if int(college.weight) == -1 and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt -1 and pop score not 3 4 or 5")
                array3_m1.append(college)

        # Make QS our of array 3_1
        array3_m1IDs = []
        for college in array3_m1:
            array3_m1IDs.append(college.id)

        array3_m1QS = models.College.objects.filter(id__in=array3_m1IDs).order_by('-pop_score')
        array3_m1 = list(array3_m1QS)


        array3_m2 = []
        for college in colleges:
            if int(college.weight) == -2 and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt -2 and pop score not 3 4 or 5")
                array3_m2.append(college)

        # Make QS our of array 3_1
        array3_m2IDs = []
        for college in array3_m2:
            array3_m2IDs.append(college.id)

        array3_m2QS = models.College.objects.filter(id__in=array3_m2IDs).order_by('-pop_score')
        array3_m2 = list(array3_m2QS)

        array3_m3 = []
        for college in colleges:
            if int(college.weight) == -3 and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt -3 and pop score not 3 4 or 5")
                array3_m3.append(college)

        # Make QS our of array 3_1
        array3_m3IDs = []
        for college in array3_m3:
            array3_m1IDs.append(college.id)

        array3_m3QS = models.College.objects.filter(id__in=array3_m3IDs).order_by('-pop_score')
        array3_m3 = list(array3_m3QS)

        array3_m4 = []
        for college in colleges:
            if int(college.weight) == -4 and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt -4 and pop score not 3 4 or 5")
                array3_m4.append(college)

        # Make QS our of array 3_1
        array3_m4IDs = []
        for college in array3_m4:
            array3_m1IDs.append(college.id)

        array3_m1QS = models.College.objects.filter(id__in=array3_m1IDs).order_by('-pop_score')
        array3_m4 = list(array3_m1QS)

        array3_m5 = []
        for college in colleges:
            if int(college.weight) == -5 and int(int(college.pop_score)) not in [3, 4, 5]:
                print("Sorted amd added colleges with wt -5 and pop score not 3 4 or 5")
                array3_m5.append(college)

        # Make QS our of array 3_1
        array3_m5IDs = []
        for college in array3_m5:
            array3_m5IDs.append(college.id)

        array3_m5QS = models.College.objects.filter(id__in=array3_m5IDs).order_by('-pop_score')
        array3_m5 = list(array3_m5QS)

        array4 = []
        for college in array1:
            array4.append(college)
        for college in array1_1:
            array4.append(college)
        for college in array2:
            array4.append(college)
        for college in array3_5:
            array4.append(college)
        for college in array3_4:
            array4.append(college)
        for college in array3_3:
            array4.append(college)
        for college in array3_2:
            array4.append(college)
        for college in array3_1:
            array4.append(college)
        for college in array3_m1:
            array4.append(college)
        for college in array3_m2:
            array4.append(college)
        for college in array3_m3:
            array4.append(college)
        for college in array3_m4:
            array4.append(college)
        for college in array3_m5:
            array4.append(college)

        array5 = []
        for college in colleges:
            if college not in array4 and college.pop_score == 2:
                print("Sorted score and added colleges with pop score 2 ")
                array5.append(college)

        array5IDs = []
        for college in array5:
            array5IDs.append(college.id)

        array5QS = models.College.objects.filter(id__in=array5IDs).order_by('-weight', '-seats')
        array5 = list(array5QS)

        array6 = []
        for college in colleges:
            if college not in array4 and college.pop_score == 1:
                print("Sorted score and added colleges with pop score 1")
                array6.append(college)

        array6IDs = []
        for college in array6:
            array6IDs.append(college.id)

        array6QS = models.College.objects.filter(id__in=array5IDs).order_by('-pop_score', '-weight', '-seats')
        array6 = list(array6QS)

        for college in array5:
            array4.append(college)
        for college in array6:
            array4.append(college)

        print("Array before make unique ", array4)

        def distinct_list(seq):  # Order preserving
            seen = set()
            return [x for x in seq if x not in seen and not seen.add(x)]

        array9 = array4
        array4 = distinct_list(array9)
        print("Sorted Results ", array4)
        return array4

    def score(self, search, ga, **kwargs):

        print("q_exm", search.q_exm_score)
        print("c_exm_1", search.compt_exm_score_1)
        print("c_exm_2", search.compt_exm_score_2)

        if search.q_exm_score == '0' and search.compt_exm_score_1 == '0' and search.compt_exm_score_2 == '0':
            print("No exam data entered, default to L")
            return "L"

        score = 0

        if search.q_exm:
            q_exm = models.QualifyingExam.objects.get(id=int(search.q_exm))
        else:
            q_exm = models.QualifyingExam.objects.first()
        if str(search.q_exm_score) == "0" and not ga:
            print("Lowest Band")
            # return "L"  #If this is not done, then if a user does not enter a q_exm but enters a c_exm, he is assigend L.
        if ga:
            print("Replacing q_exm with GA object", q_exm)
            print(kwargs.get("college"))
            q_exm = models.GAScore.objects.filter(college=models.College.objects.get(id=kwargs.get("college")), q_exam=q_exm).first()
            print("Replaced q_exm with GA object", q_exm)
        if q_exm is not None and q_exm.score_type != "Rank":
            if not ga and int(search.q_exm_score) <= int(q_exm.l_cutoff):
                score = 1
            elif int(q_exm.l_cutoff) <= int(search.q_exm_score) < int(q_exm.m_cutoff):
                score = 1
            elif int(q_exm.m_cutoff) <= int(search.q_exm_score) < int(q_exm.h_cutoff):
                score = 2
            elif int(search.q_exm_score) >= int(q_exm.h_cutoff):
                score = 3
        elif q_exm is not None and q_exm.score_type == "Rank":
            if not ga and int(search.q_exm_score) > int(q_exm.h_cutoff):
                score = 1
            elif int(q_exm.m_cutoff) <= int(search.q_exm_score):
                score = 1
            elif int(q_exm.m_cutoff) > int(search.q_exm_score) > int(q_exm.h_cutoff):
                score = 2
            elif int(search.q_exm_score) < int(q_exm.h_cutoff):
                score = 3

        print("Score assigned based on QE is ", score)

        _score = 0
        if search.compt_exm_type_1 and search.compt_exm_score_1:
            c = models.CompetitiveExam.objects.get(id=int(search.compt_exm_type_1))
            if ga:
                c = models.GAScore.objects.filter(college=models.College.objects.get(id=kwargs.get("college")), c_exam=c).first()
            if c is not None and c.score_type != "Rank":
                if not ga and int(search.q_exm_score) < int(q_exm.l_cutoff):
                    score = 1
                elif int(c.l_cutoff) <= int(search.compt_exm_score_1) < int(c.m_cutoff):
                    _score = 1
                elif int(c.m_cutoff) <= int(search.compt_exm_score_1) < int(c.h_cutoff):
                    _score = 2
                elif int(search.compt_exm_score_1) >= int(c.h_cutoff):
                    _score = 3
                if _score > score:
                    score = _score
            elif c is not None and c.score_type == "Rank":
                if not ga and int(search.q_exm_score) > int(q_exm.h_cutoff):
                    _score = 1
                elif int(c.m_cutoff) <= int(search.compt_exm_score_1) and int(search.compt_exm_score_1) < int(c.h_cutoff):
                    _score = 1
                elif int(c.m_cutoff) > int(search.compt_exm_score_1) > int(c.l_cutoff):
                    _score = 2
                elif int(search.compt_exm_score_1) < int(c.l_cutoff):
                    _score = 3
                if _score > score:
                    score = _score
            else:
                score = _score

        if search.compt_exm_type_2 and search.compt_exm_score_2:
            c = models.CompetitiveExam.objects.get(id=int(search.compt_exm_type_2))
            if ga:
                c = models.GAScore.objects.filter(college=models.College.objects.get(id=kwargs.get("college")), c_exam=c).first()
            if c is not None and c.score_type != "Rank":
                if int(c.l_cutoff) <= int(search.compt_exm_score_2) < int(c.m_cutoff):
                    _score = 1
                elif int(c.m_cutoff) <= int(search.compt_exm_score_2) < int(c.h_cutoff):
                    _score = 2
                elif int(search.compt_exm_score_2) >= int(c.h_cutoff):
                    _score = 3
                elif not ga and int(search.q_exm_score) < int(q_exm.l_cutoff):
                    score = 1
                if _score > score:
                    score = _score
            elif c is not None and c.score_type == "Rank":
                if int(c.m_cutoff) <= int(search.compt_exm_score_2) and int(search.compt_exm_score_2) < int(c.h_cutoff):
                    _score = 1
                elif int(c.m_cutoff) > int(search.compt_exm_score_2) > int(c.l_cutoff):
                    _score = 2
                elif int(search.compt_exm_score_2) < int(c.l_cutoff):
                    _score = 3
                elif not ga and int(search.q_exm_score) > int(q_exm.h_cutoff):
                    _score = 1
                if _score > score:
                    score = _score
            else:
                score = _score

        #NOTE: Compt exams 3 4 and 5 were removed in future versions of the app, and hence the following blocks of code are not updated.

        if search.compt_exm_type_3 and search.compt_exm_score_3:
            c = models.CompetitiveExam.objects.get(id=int(search.compt_exm_type_3))
            if ga:
                c = models.GAScore.objects.filter(college=models.College.objects.get(id=kwargs.get("college")), c_exam=c).first()
            if c is not None:
                if int(c.l_cutoff) <= int(search.compt_exm_score_1) < int(c.m_cutoff):
                    _score = 1
                elif int(c.m_cutoff) <= int(search.compt_exm_score_1) < int(c.h_cutoff):
                    _score = 2
                elif int(search.compt_exm_score_1) >= int(c.h_cutoff):
                    _score = 3
                if _score > score:
                    score = _score
            else:
                score = _score

        if search.compt_exm_type_4 and search.compt_exm_score_4:
            c = models.CompetitiveExam.objects.get(id=int(search.compt_exm_type_4))
            if ga:
                c = models.GAScore.objects.filter(college=models.College.objects.get(id=kwargs.get("college")), c_exam=c).first()
            if c is not None:
                if int(c.l_cutoff) <= int(search.compt_exm_score_1) < int(c.m_cutoff):
                    _score = 1
                elif int(c.m_cutoff) <= int(search.compt_exm_score_1) < int(c.h_cutoff):
                    _score = 2
                elif int(search.compt_exm_score_1) >= int(c.h_cutoff):
                    _score = 3
                if _score > score:
                    score = _score
            else:
                score = _score

        if search.compt_exm_type_5 and search.compt_exm_score_5:
            c = models.CompetitiveExam.objects.get(id=int(search.compt_exm_type_5))
            if ga:
                c = models.GAScore.objects.filter(college=models.College.objects.get(id=kwargs.get("college")), c_exam=c).first()
            if c is not None:
                if int(c.l_cutoff) <= int(search.compt_exm_score_1) < int(c.m_cutoff):
                    _score = 1
                elif int(c.m_cutoff) <= int(search.compt_exm_score_1) < int(c.h_cutoff):
                    _score = 2
                elif int(search.compt_exm_score_1) >= int(c.h_cutoff):
                    _score = 3
                if _score > score:
                    score = _score
            else:
                score = _score

        # convert score lmh #
        if score == 1:
            score = "L"
        elif score == 2:
            score = "M"
        elif score == 3:
            score = "H"

        return score


    def get_results(self):
        search = models.Search.objects.get(id=int(self.kwargs['id']))
        course = search.course
        course_type = search.course_type

        ## Scholarship Determination ##

        # Get Qualification Objects #
        q_objects = []
        if course_type == "cor":
            for q in models.Qualification.objects.all():
                for c in q.courses.all():
                    if c.id == int(course):
                        q_objects.append(q)
            print("Type selected is COR and the list of q_objs is ", q_objects)

            for q in q_objects:
                print("q.level ", q.level, " search.level ", search.level)
                if q.level != search.level:
                    q_objects.remove(q)
                    print("Removed ", q)
            print("List after level filter ", q_objects)

        else:
            print("Type selected is CAT")
            q_obj = models.Qualification.objects.filter(course_category=search.course) #FIXME: Did Nikhil change this?
            # q_objects.append(q_obj)
            q_objects = list(q_obj)
            print("q_obj", q_obj)


        # Add seats according to query to college model #
        for college in models.College.objects.all():
            _cc_objects = models.CollegeCourse.objects.filter(college=college, approval_period__date_from__lte=datetime.datetime.now().date(),
                                                             approval_period__date_to__gte=datetime.datetime.now().date(), qualification__in=q_objects)
            total_seats = 0
            for _cc_object in _cc_objects:
                if _cc_object.seats:
                    total_seats += _cc_object.seats
            for cqualification in models.CollegeQualification.objects.filter(college=college, qualification__in=q_objects):
                if cqualification.seats:
                    total_seats += cqualification.seats
            college.seats = total_seats
            college.save()
            print("Total seats ", total_seats, " was added to college object.")

        print("Getting Score")
        score = self.score(search, False)
        print("score returned is ", score)

        print("course ", course, "course_type", course_type, "city", search.city)

        # First, get all colleges, not held, and level
        colleges = []
        for college in models.College.objects.filter(hold=False, qualifications__level=search.level).distinct():
            flag = False
            for _q in college.qualifications.all():
                if _q in q_objects:
                    print(_q, " is in college.qualifications.all() ", college.qualifications.all())
                    flag = True
            if flag:
                colleges.append(college)
        print("Colleges List initial :", colleges)

        for college in colleges:
            if search.q_exm_score == "0" and search.compt_exm_score_1 == "0" and search.compt_exm_score_2 == "0" and college.category == "GA":
                colleges.remove(college)

                ##The above exclusion is being done because if a student does not enter any scores, any GA colleges should not be returned. #FIXME: This might cause problems, not sure how.

        # Filter by Qualification, if type selected is qualification
        if course_type == "cat":
            for college in colleges:
                flag = False
                for qualification_ in college.qualifications.all():
                    if qualification_ in q_objects:
                        flag = True
                if not flag:
                    colleges.remove(college)

        '''# Now, if a college has a particular Qualification, but college qualification object does not exist, remove.
        for qualification in q_objects:
            for college in colleges:
                qs = models.CollegeQualification.objects.filter(college=college, qualification=qualification).first()
                if qs is None:
                    print college.name, " is being removed because CQ object for ", qualification, " does not exist."
                    colleges.remove(college)'''

        # Now, remove college if course is selected but CC does not exist.
        if course_type == "cor":
            for college in colleges:
                qs = models.CollegeCourse.objects.filter(college=college, course=models.Course.objects.get(id=search.course)).first()
                if qs is None:
                    print(college.name, " is being removed because CC object for course ", course, " does not exist.")
                    colleges.remove(college)

        # Filter by Course, if type selected is course
        if course_type == "cor":
            for college in colleges:
                flag = False
                for qualification in college.qualifications.all():
                    for _course in qualification.courses.all():
                        if _course.id == int(course):
                            flag = True
                if not flag:
                    colleges.remove(college)

        print("Going to sort following list of colleges: ", colleges)
        array4 = self.sort_colleges(colleges)

        json = []

        print("### Starting Result Population ###")
        print(array4, "array4")
        if course_type == "cor":
            for college in array4:
                print(college, " is in hand.")
                # Get CollegeCourse Object #
                if course_type == "cor":
                    cc_objects = models.CollegeCourse.objects.filter(college=college, course=course, approval_period__date_from__lte=datetime.datetime.now().date(), approval_period__date_to__gte=datetime.datetime.now().date())
                if len(cc_objects) == 0:
                    print("Did not find CC object, skipping college: ", college)
                    continue  # Skip entire for loop

                print(cc_objects, "CC Objects")
                schl = 0
                for cc_obj in cc_objects:
                    print(cc_obj, " is in hand.")
                    # Get CollegeQualification Object #
                    print("Looking for CQ object for ", college, cc_obj.qualification)
                    cq = models.CollegeQualification.objects.filter(college=college, qualification=cc_obj.qualification, approval_period__isnull=False).first() #FIXME: Will this always be one?
                    print(cq, "CQ was found")
                    if cq is not None and cq.qualification.level == search.level:
                        print(cq, "CQ")
                        '''if cq.approval_period.date_from < datetime.datetime.now().date() < cq.approval_period.date_to:
                            print "college ", college, " is not in approval period. Skipping. "
                            continue'''

                        course_name = cc_obj.qualification.qualification + " with specialization in " + cc_obj.course.name

                        schl = 0
                        if not college.category == "GA":
                            print("College is not of type GA")
                            if score == "L":
                                schl = cc_obj.schl_l
                            elif score == "M":
                                schl = cc_obj.schl_m
                            elif score == "H":
                                schl = cc_obj.schl_h
                            print("schl calculated is ", schl)
                        elif college.category == "GA":
                            print("College is of type GA, recalculating score.")
                            ga_score = self.score(search, True, **{'college': college.id})
                            print("New GA score is", ga_score)
                            if ga_score == "L":
                                schl = cc_obj.schl_l
                            elif ga_score == "M":
                                schl = cc_obj.schl_m
                            elif ga_score == "H":
                                schl = cc_obj.schl_h
                            print("schl calculated is ", schl)

                        # Determine the fee #
                        fee = cc_obj.fee

                        # Determine total seats #
                        if cc_obj:
                            if cc_obj.seats and cc_obj.seats > 0:
                                seats = cc_obj.seats
                                decrement_from = "cc"
                            elif cc_obj.seats == 0:
                                seats = -1
                            else:
                                if cq.seats and cq.seats > 0:
                                    seats = cq.seats
                                    decrement_from = "cq"
                                else:
                                    seats = -1

                        # Make images array #
                        images = []
                        for image in college.images.all():
                            try:
                                '''images.append({'url': image.image.url, 'height': image.image.height, 'width': image.image.width})'''
                                images.append({'url': image.image.url, 'height': '100%', 'width': '100%'})
                            except:
                                print("Error")

                        if True:
                            s_fee = float(fee) - ((float(schl) / 100.0) * float(fee))
                            if cq is not None and seats != -1:
                                json.append({'id': college.id, 'name': college.name, 'street1': college.street_1, 'campus': college.campus,
                                             'street2': college.street_2,
                                             'city': college.city, 'state': college.state, 'pin': college.pin,
                                             'country': 'India', 'course_name': course_name, 'logo': college.logo.url,
                                             'images': images,
                                             'website': college.website, 'session_start': cq.session_start, 'cost': fee, 'fee_unit': cc_obj.time_unit,
                                             'scholarship': schl,
                                             'final_fee': int(s_fee), 'college_qualification': cq.id, 'seats': seats, 'lat': college.lat, 'long': college.long,
                                             'city_lat': college.city.lat, 'city_long': college.city.long,
                                             'city_id': college.city.id, 'decrement_from': decrement_from, 'cc_obj': cc_obj.id,'college_quality_index':cq.college_quality_index})
                        print("college was not populated because cq is None ", college)
                        print("bool schl", bool(schl), schl)

        elif course_type == "cat":
            for college in array4:
                print(college, " is in hand.")

                # Get CollegeQualification Object #
                for q_obj__ in q_objects:
                    cq = models.CollegeQualification.objects.filter(qualification=q_obj__, college=college, qualification__level=search.level).first()

                    print(cq, "CQ was found")
                    if cq is not None:
                        print(cq, "CQ")

                        course_name = cq.qualification

                        schl = 0
                        if not college.category == "GA":
                            print("College is not of type GA")
                            if score == "L":
                                schl = cq.schl_l
                            elif score == "M":
                                schl = cq.schl_m
                            elif score == "H":
                                schl = cq.schl_h
                            print("schl calculated is ", schl)
                        elif college.category == "GA":
                            print("College is of type GA, recalculating score.")
                            ga_score = self.score(search, True, **{'college': college.id})
                            if ga_score == "L":
                                schl = cq.schl_l
                            elif ga_score == "M":
                                schl = cq.schl_m
                            elif ga_score == "H":
                                schl = cq.schl_h
                            print("schl calculated is ", schl)

                        # Determine the fee #
                        f = 0
                        f_unit = 0
                        for _cc in models.CollegeCourse.objects.filter(college=college, qualification=q_obj__):
                            if not bool(f):
                                print("First fee found is ", _cc.fee)
                                f = _cc.fee
                                f_unit = _cc.time_unit
                            else:
                                if _cc.fee < f:
                                    print("Smaller fee found ", _cc.fee)
                                    f = _cc.fee
                                    f_unit = _cc.time_unit
                        fee = f
                        # Determine total seats #
                        if not cq.seats:
                            seats = -1
                        elif cq.seats == 0:
                            seats = -1
                        else:
                            seats = cq.seats
                            decrement_from = "cq"

                        # Make images array #
                        images = []
                        for image in college.images.all():
                            images.append({'url': image.image.url, 'height': '100%', 'width': '100%'})

                        if bool(schl):
                            s_fee = float(fee) - ((float(schl) / 100.0) * float(fee))
                            if cq is not None and seats != -1 and schl != 0:
                                json.append({'id': college.id, 'name': college.name, 'street1': college.street_1,
                                             'campus': college.campus,
                                             'street2': college.street_2,
                                             'city': college.city, 'state': college.state, 'pin': college.pin,
                                             'country': 'India', 'course_name': course_name, 'logo': college.logo.url,
                                             'images': images,
                                             'website': college.website, 'session_start': cq.session_start, 'cost': fee, 'fee_unit': f_unit,
                                             'scholarship': schl,
                                             'final_fee': int(s_fee), 'college_qualification': cq.id, 'seats': seats, 'lat': college.lat, 'long': college.long,
                                             'city_lat': college.city.lat, 'city_long': college.city.long, 'city_id': college.city.id, 'decrement_from': decrement_from,'college_quality_index':cq.college_quality_index})
                        print("bool schl", bool(schl), schl)

        return json

    def get_length(self):
        return len(self.get_results())

    def get_selected_city(self):
        search = models.Search.objects.get(id=int(self.kwargs['id']))
        city = models.City.objects.get(id=search.city)
        return {'name': city.name, 'lat': city.lat, 'long': city.long, 'id':city.id}

    def get_course_type(self):
        search = models.Search.objects.get(id=int(self.kwargs['id']))
        return search.course_type


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_vouchers(self):
        from django.core import serializers
        serialized_obj = serializers.serialize('json', list(models.Order.objects.filter(profile=self.request.user.profile, status=2)))
        print(serialized_obj)
        # return serialized_obj


# class UpdateProfile(LoginRequiredMixin, UpdateView):
#     model = models.Profile
#     template_name = "profile.html"
#     fields = ['name', 'id_type', 'id_no', 'dob', 'gender', 'otp', 'mobile', 'house'
#               'state', 'city', 'street', 'district', 'state', 'country']
#     success_url = "/"

#     def get_context_data(self, **kwargs):
#         context = super(UpdateProfile, self).get_context_data(**kwargs)
#         form = forms.UpdateProfile(self.request.POST or None)
#         context["form"] = form
#         return context

#     def get_vouchers(self):
#         return models.Order.objects.filter(profile=self.request.user.profile, status="2")

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         # Do any custom stuff here
#         self.object.save()

#         add_message(self.request, 25, "Updated Profile")
#         return redirect("/")


# class CreateProfile(LoginRequiredMixin, CreateView):
#     model = models.Profile
#     template_name = "profile.html"
#     fields = ['name', 'id_type', 'id_no', 'dob', 'gender', 'otp', 'mobile', 'house'
#               'state', 'city', 'street', 'district', 'state', 'country']
#     success_url = "/"

#     def form_valid(self, form):
#         fi = form.save(commit=False)
#         fi.user = self.request.user
#         fi.save()
#         add_message(self.request, 25, "Updated Profile")
#         return super(CreateProfile, self).form_valid(form)


class Selection(FormView):
    template_name = "profile.html"
    form_class = forms.SelectedForm

    def form_valid(self, form):
        print("Form is valid")
        college = models.College.objects.get(id=self.request.POST.get("college"))
        scholarship =self.request.POST.get("scholarship")
        fee = self.request.POST.get("fee")
        final_fee = self.request.POST.get("final_fee")
        course_name = self.request.POST.get("course_name")
        college_qualification = models.CollegeQualification.objects.get(id=self.request.POST.get("college_qualification"))
        search = models.Search.objects.get(id=self.request.POST.get("search"))
        seats = self.request.POST.get("seats")
        cc_obj = False
        if self.request.POST.get("cc_obj"):
            cc_obj = models.CollegeCourse.objects.get(id=int(self.request.POST.get("cc_obj")))
        a = models.Selection.objects.create(
            coupon_code= "JR"+''.join(random.choice(string.digits) for _ in range(2)) + college.code + ''.join(random.choice(string.digits) for _ in range(1)),
            college=college,
            scholarship=scholarship,
            fee=fee,
            final_fee=final_fee,
            course_name=course_name,
            college_qualification=college_qualification,
            search=search,
            savings=int(fee) - int(final_fee),
            total_savings=(int(fee) - int(final_fee))*college_qualification.qualification.duration,
            seats=seats,
            decrement_from=self.request.POST.get("decrement_from")
        )
        if cc_obj:
            a.cc_obj = cc_obj
            a.save()
        b = models.Configuration.objects.first()
        b.last_c_code += 1
        b.save()
        return HttpResponseRedirect("/selected-college/" + str(a.id))

    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)
        return super(Selection, self).form_invalid(form)


class Screen3(TemplateView):
    template_name = "screen3.html"

    def get_selection(self):
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return self.kwargs['pk']

    def get_data(self):
        data = []
        s = models.Selection.objects.get(id=self.kwargs['pk'])
        cq = s.college_qualification
        savings = int(s.fee) - int(s.final_fee)
        # Make images array #
        images = []
        for image in s.college.images.all():
            try:
                images.append({'src': image.image.url, 'height': '100%', 'width': '100%'})
            except:
                print("Error")
                pass

        def get_p_image():
            imageUrl=""
            for image in s.college.images.all():
                if image.primary:
                    imageUrl=image.image.url
                    break
            else:
                imageUrl=s.college.images.all()[0].image.url
            return imageUrl

        data.append(
            {'college': s.college.name, 'course_name': s.course_name, 'address_s1':
                s.college.street_1, 'address_s2': s.college.street_2,
             'address_city': s.college.city,
             'address_state': s.college.state, 'address_pin': s.college.pin,
             'fee': s.fee, 'final_fee': s.final_fee, 'scholarship': s.scholarship, 'images': images, 'pimage': get_p_image(),
             'lat': s.college.lat, 'long': s.college.long, 'logo': s.college.logo.url, 'campus': s.college.campus,
             'session_start_date': s.college_qualification.session_start, 'seats': s.seats,
             'af_cr': cq.af_cr, 'savings': savings, 'rec_app': cq.rec_app,'college_quality_index':cq.college_quality_index}
        )
        return data

    def get_eb1(self):
        try:
            if len(models.Event1.objects.all()) == 1:
                if models.Event1.objects.all().first().activate and models.Event1.objects.all().first().date_from.month <= datetime.date.today().month <= models.Event1.objects.all().first().date_to.month:
                    print("E1 is true")
                    s = models.Selection.objects.get(id=self.kwargs['pk'])
                    if s.search.level == "G":
                        print("Level is G")
                        q_exm = s.search.q_exm
                        if not q_exm:
                            q_exm = -1
                        print("q_exm", q_exm)
                        e1 = models.Event1.objects.all().first()
                        if q_exm is None:
                            print("E1 is fired")
                            return [{'preview': e1.preview, 'description': e1.description,
                                     'icon_lib': e1.icon_lib, 'icon_name': e1.icon_name, 'icon_size': e1.icon_size, 'icon_color': e1.icon_color,
                                     'preview2': e1.preview2, 'description2': e1.description2}]
                        _p = []
                        for p in e1.parameter1.all():
                            _p.append(int(p.id))
                        print(_p, q_exm)
                        if q_exm:
                            if int(q_exm) not in _p:
                                print("E1 is fired")
                                return [{'preview': e1.preview, 'description': e1.description,
                                         'icon_lib': e1.icon_lib, 'icon_name': e1.icon_name, 'icon_size': e1.icon_size, 'icon_color': e1.icon_color,
                                         'preview2': e1.preview2, 'description2': e1.description2}]
                    elif s.search.level == "PG":
                        q_exm = s.search.q_exm
                        e1 = models.Event1.objects.all().first()
                        if not q_exm:
                            print("E1 is fired")
                            return [{'preview': e1.preview, 'description': e1.description,
                                     'icon_lib': e1.icon_lib, 'icon_name': e1.icon_name, 'icon_size': e1.icon_size, 'icon_color': e1.icon_color,
                                     'preview2': e1.preview2, 'description2': e1.description2}]
                        _p = []
                        for p in e1.parameter2.all():
                            _p.append(int(p.id))
                        if q_exm:
                            if int(q_exm) not in _p:
                                print("E1 is fired")
                                return [{'preview': e1.preview, 'description': e1.description,
                                         'icon_lib': e1.icon_lib, 'icon_name': e1.icon_name, 'icon_size': e1.icon_size, 'icon_color': e1.icon_color,
                                         'preview2': e1.preview2, 'description2': e1.description2}]
        except(Exception, e):
            print('Exception Occured {}'.format(sys.exc_info()[-1].tb_lineno))
        return False

    def get_eb2(self):
        try:
            s = models.Selection.objects.get(id=self.kwargs['pk'])
            if len(models.Event2.objects.all()) == 1:
                if models.Event2.objects.all().first().activate:
                    if s.college_qualification.guarantee:
                        e2 = models.Event2.objects.all().first()
                        return [{'preview': e2.preview, 'description': e2.description,
                                 'icon_lib': e2.icon_lib, 'icon_name': e2.icon_name, 'icon_size': e2.icon_size, 'icon_color': e2.icon_color,
                                 'preview2': e2.preview2, 'description2': e2.description2, 'true': True}]
                    else:
                        e2 = models.Event2.objects.all().first()
                        return [{'preview3': e2.preview3, 'description3': e2.description3, 'true': False}]
        except:
            print("Exception occured")
        return False

    def get_boxes(self):
        b = models.Selection.objects.get(id=self.kwargs['pk']).college_qualification
        return [b.b1, b.b2, b.b3, b.b4, b.b5]

    def get_important_info(self):
        y = []
        if models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.important_info:
            for x in models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.important_info.statements.all():
                y.append({'description': x.description, 'preview': x.preview })
            return y
        return False

    def get_other_benefits(self):
        y = []
        if models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.other_benefits:
            for x in models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.other_benefits.statements.all():
                y.append({'description': x.description, 'preview': x.preview })
            return y
        return False

    def get_info_scholarship(self):
        y = []
        if models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.info_scholarship:
            for x in models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.info_scholarship.statements.all():
                y.append({'description': x.description, 'preview': x.preview })
            return y
        return None

    def get_admission_process(self):
        y = []
        if models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.info_admission_process:
            for x in models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.info_admission_process.statements.all():
                y.append({'description': x.description, 'preview': x.preview })
            return y
        return False

    def get_col(self):
        eb = 0
        if self.get_eb1():
            eb += 1
            print("EB1")
        if self.get_eb2():
            eb += 1
            print("EB2")
        b = 0
        for item in self.get_boxes():
            if item:
                b += 1
        b = b + eb
        print("total ", b)
        if b == 4:
            return 3
        elif b == 3:
            return 4
        elif b == 2:
            return 6
        elif b == 1:
            return 12
        return 3


class Screen4(TemplateView):
    template_name = "screen4-new.html"

    def get_context_data(self, **kwargs):
        context = super(Screen4, self).get_context_data(**kwargs)
        form = forms.Screen4Form(self.request.POST or None)
        context["form"] = form
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context

    def get_college(self):
        s = models.Selection.objects.get(id=self.kwargs['pk'])
        return [{'logo': s.college.logo.url, 'course_title': s.course_name, 'college': s.college, 'duration': s.college_qualification.qualification.duration, 'college_qualification': s.college_qualification, 'coupon_code': s.coupon_code,'street_1':s.street_1,'city':s.city }]

    def get_agreements(self):
        y = []
        if models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.agreements:
            for x in models.Selection.objects.get(id=self.kwargs['pk']).college_qualification.agreements.statements.all():
                y.append(x.preview)
            return y
        return False

    def ask_college(self):
        s = models.Selection.objects.get(id=self.kwargs['pk'])
        if s.search.level == 'PG':
            return True
        return False

    def ask_school(self):
        s = models.Selection.objects.get(id=self.kwargs['pk'])
        if s.search.level == "G":
            return True
        return False

    def get_scholarship_details(self):
        s = models.Selection.objects.get(id=self.kwargs['pk'])
        return [s]

    def get_c_exams(self):
        s = models.Selection.objects.get(id=self.kwargs['pk'])
        results = []
        if s.search.compt_exm_type_1:
            e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_1)
            results.append(e)
        if s.search.compt_exm_type_2:
            e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_2)
            results.append(e)
        if s.search.compt_exm_type_3:
            e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_3)
            results.append(e)
        if s.search.compt_exm_type_4:
            e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_4)
            results.append(e)
        if s.search.compt_exm_type_5:
            e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_5)
            results.append(e)
        return results


class VerifyEmail(View):

    def get(self, request, *args, **kwargs):
        email = self.kwargs['email']
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        models.OTP.objects.create(
            key=key,
            type="email"
        )
        message = models.EmailTemplate.objects.get(type="OTP").html
        message = message.replace("*|NAME|*", email)
        message = message.replace("*|OTP|*", key)
        postmark = PostmarkClient(token=models.Configuration.objects.first().post_mark_key)
        postmark.emails.send(
            From="no-reply@justrokket.com",
            To=email,
            Subject=models.EmailTemplate.objects.get(type="OTP").subject,
            HtmlBody=message
        )
        return HttpResponse("Successfully sent code to: " + email)


class VerifyMobile(View):

    def get(self, request, *args, **kwargs):
        mobile = self.kwargs['mobile']
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        models.OTP.objects.create(
            key=key,
            type="mobile"
        )
        c = models.Configuration.objects.first()
        client = TwilioRestClient(c.twillio_account_sid, c.twillio_key)

        message = client.messages.create(
            body="The OTP to verify your Just Rokket account is: " + str(key),
            to="+91"+str(mobile),
            from_=str(c.twillio_from_number),
        )
        return HttpResponse("Successfully Sent code to: " + mobile)


class CreateProfile(FormView):
    form_class = forms.Screen4Form
    model = models.Profile

    def get_context_data(self, *args, **kwargs):
        context = super(CreateProfile, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        context['form'] = forms.Screen4Form
        return context

    def form_valid(self, form):

        # def get(request, parameter):
        #     return self.request.POST.get(parameter)

        p = models.Profile.objects.create(
            name=pget(self.request, "name"),
            # id_type=pget(self.request,  "id_type"),
            # id_no=pget(self.request, "id_no"),
            dob=pget(self.request, "dob"),
            gender=pget(self.request, "gender"),
            email=pget(self.request, "email"),
            address=pget(self.request, "address"),
            # otp=pget(self.request, "otp"),
            # phone=pget(self.request,  "phone"),
            # house=pget(self.request, "house"),
            # street=pget(self.request, "street"),
            # city=pget(self.request, "city"),
            # country=pget(self.request, "country"),
            college=pget(self.request, "college")
        )

        p.user = models.User.objects.create_user(
            username=pget(self.request, "email"),
            password=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        )
        p.save()

    def form_invalid(self, form):
        print("Form is invalid")
        return super(CreateProfile, self).form_invalid(form)


class VerifyOTP(View):

    def get(self, request, *args, **kwargs):
        if self.kwargs['type'] == "e":
            otp_type = "email"
        elif self.kwargs['type'] == "m":
            otp_type = "mobile"
        otp = models.OTP.objects.filter(key=self.kwargs['otp'], type=otp_type).first()
        if otp is not None:
            otp.used = True
            otp.save()
            p = models.Profile.objects.filter(user=self.request.user).first()
            if self.request.user.is_authenticated and p is not None:
                if otp_type == "email":
                    p.email_verified = True
                    p.save()
                else:
                    p.mobile_verified = True
                    p.save()
            return HttpResponse("Valid")
        else:
            return HttpResponse("Invalid")



class LoginUser(FormView):
    form_class = forms.LoginForm
    template_name = ""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginUser, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        form = form_class(self.request.POST or None)
        context["form"] = form
        return context

    def form_valid(self, form):
        u = models.User.objects.filter(email=self.request.POST.get("email"),
                                       ).first()

        if u is None:
            if self.request.is_ajax():
               data_dict = {'success': True, 'msg': "User with this email does not exist", 'email': '', 'password': ''}
               return HttpResponse(json.dumps(data_dict), content_type="application/json")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        else:
            user_authenticated = authenticate(username=self.request.POST.get("email"), password=self.request.POST.get("password"))
            if user_authenticated:
                login(self.request, u)
                if self.request.is_ajax():
                    data_dict = {'success': True, 'msg': "Login Successfull", 'email': '', 'password': ''}
                    return HttpResponse(json.dumps(data_dict), content_type="application/json")
                p = models.Profile.objects.filter(user=u).first()
                if p is None:
                    return HttpResponseRedirect("/update-profile/")
                return HttpResponseRedirect("/")            #self.request.META.get('HTTP_REFERER')
            else:
                if self.request.is_ajax():
                    data_dict = {'success': False, 'msg': "Invalid Credentials", 'email': '', 'password': ''}
                    return HttpResponse(json.dumps(data_dict), content_type="application/json")
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        if self.request.is_ajax():
            data_dict = {'form': form.errors}
            print(data_dict)
            return HttpResponse(json.dumps(data_dict), content_type="application/json")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class UpdateProfile(LoginRequiredMixin, UpdateView):
    success_url = "/update-profile/"
    template_name = "profile.html"
    # form_class = forms.Screen4Form
    # fields = ['name', 'dob', 'gender', 'phone', 'address',
    #           'profile_image', 'graduation_year', 'mobile','college']

    form_class = forms.ProfileForm

    def get_context_data(self, **kwargs):
        context = super(UpdateProfile, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        profile = models.Profile.objects.get(user=user)
        # questions asked by me
        context['my_questions'] = Question.objects.filter(user=profile)


        context['answered_by_me'] = models.QuestionExpert.objects.filter(assigned_to=profile).filter(answered=True)

        #questions that were assigned to this profile but haven't been answered by him yet
        context['questions_pending'] = models.QuestionExpert.objects.filter(assigned_to=profile).filter(answered=False)


        print(context['answered_by_me'])
        # context['questions_pending'] = 

        #question 
        # context['questio']
        print(context['my_questions'])

        if self.request.POST:
            context['eduqualform'] = forms.EduQualFormSet(self.request.POST, instance=self.object)
        else:
            context['eduqualform'] = forms.EduQualFormSet(instance=self.object)
        return context



    def get_success_url(self):
        view_name = 'update-profile'
        return reverse(view_name, kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        user = User.objects.get(id=self.kwargs['pk'])
        return models.Profile.objects.get(id=user.profile.id)

    def get_vouchers(self):
        a = []
        for v in models.Order.objects.filter(profile=self.request.user.profile, status=2):
            c1, c2, q1 = False, False, False
            print(v.selection.search.compt_exm_type_1)
            if bool(v.selection.search.compt_exm_type_1):
                c1 = models.CompetitiveExam.objects.filter(id=v.selection.search.compt_exm_type_1).first()
            if bool(v.selection.search.compt_exm_type_2):
                c2 = models.CompetitiveExam.objects.filter(id=v.selection.search.compt_exm_type_2).first()
            if bool(v.selection.search.q_exm):
                q1 = models.QualifyingExam.objects.filter(id=int(v.selection.search.q_exm)).first()
            a.append(
                {'order_number': v.order_number,
                 'id': v.id,
                 'scholarship_awarded': v.selection.scholarship,
                 'college_name': v.selection.college.name,
                 'campus': v.selection.college.campus,
                 'qualification': v.selection.college_qualification.qualification,
                 'session_start': v.selection.college_qualification.session_start,
                 'email': v.profile.user.email,
                 'mobile': v.profile.mobile,
                 'c_exm_type_1': c1,
                 'c_exm_type_2': c2,
                 'c_exm_score_1': v.selection.search.compt_exm_score_1,
                 'c_exm_score_2': v.selection.search.compt_exm_score_2,
                 'q_exm': q1,
                 'q_exm_score': v.selection.search.q_exm_score,
                 'transaction_date': v.transaction_date,
                 'refund_requested': v.refund_requested,
                 'refund_processed': v.refund_processed
                 }
            )
        print(a)
        return a

    def form_valid(self, form):

        context = self.get_context_data()
        eduqual = context['eduqualform']

        with transaction.atomic():
            self.object = form.save()
        if eduqual.is_valid():
            eduqual.instance = self.object
            eduqual.save()



        return super(UpdateProfile, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(UpdateProfile, self).form_invalid(form)


class SignupView(FormView):
    model = models.User
    template_name = "signup.html"
    form_class = forms.SignupForm
    success_url = "/"

    def form_invalid(self, form):
        if self.request.is_ajax():
            data_dict = {'form': form.errors}
            return HttpResponse(json.dumps(data_dict), content_type="application/json")
        return super(SignupView, self).form_invalid(form)

    def form_valid(self, form):
        e = models.User.objects.filter(email=self.request.POST.get("signup_email")).first()
        if e is None:
            user_obj, created = \
                models.User.objects.get_or_create(email=self.request.POST.get("signup_email"),
                                                  username=self.request.POST.get("signup_email"),
                                                  )
            user_obj.set_password(self.request.POST.get("signup_password"))
            user_obj.save()
            login(self.request, user_obj)
            profile_obj = models.Profile.objects.create(user=user_obj)
            email_template = models.EmailTemplate.objects.filter(type="NEWUSER").first()
            if email_template is not None:
                subject = email_template.subject
                message = email_template.html
                # message = message.replace("*|STUDENT_NAME|*", profile_obj.name)
                message = message.replace("*|NAME|*", profile_obj.user.email)
                # message = message.replace("*|COURSE_NAME|*", selection.course_name)
                # message = message.replace("*|SCHOLARSHIP|*", selection.scholarship)
                # message = message.replace("*|FINAL_FEE|*", selection.final_Fee)
                send_mail(
                    subject=subject,
                    message=message,
                    recipient_list=[str(self.request.user.email)],
                )
            if self.request.is_ajax():
                data_dict = {'success': True, 'msg': "Signup Successfull", 'email': '', 'password': ''}

                return HttpResponse(json.dumps(data_dict), content_type="application/json")

            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        else:
            if self.request.is_ajax():
                data_dict = {'success': False, 'msg': "A user with this email already exists.", 'email': '', 'password': ''}
                return HttpResponse(json.dumps(data_dict), content_type="application/json")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


def get_name(obj):
    try:
        name = obj["name"]
    except:
        name = obj["course_category"]
    return name


def populate_course_categories(request):
    final_data = []
    course_category = []
    final_data_list = []
    data = []
    if request.is_ajax():
        web_input = request.GET.get('q')
        web_input_for_level = request.GET.get('page')
        if web_input and web_input_for_level:
            # two kinds of search criteria
            # 1) keywords search based on course-returns course obj and course category
            # fetch course objects, prepare data list and return course name
            course_obj = models.Course.objects.filter(keywords__word__icontains=web_input,
                                                      qualification__level=web_input_for_level).values('id', 'name').distinct()

            # convert it into python data type
            course_object_data_list = list(course_obj)
            # fetch course category, prepare data list and return course category
            for item in course_object_data_list:
                course_category.extend(list(models.Qualification.objects.filter(courses=item.get('id'),
                                                                                level=web_input_for_level).values('course_category').distinct()))
            # at this point of time we have data with two list
            # now merge these two list and return the json
            final_data.extend([item.get('course_category') for item in course_category])
            final_data.extend([item.get('name') for item in course_object_data_list])
            # 2) keywords search based on qualifications-returns course category and courses
            # fetch course category from qualification keywords
            course_category_from_qualification_queryset = \
                models.Qualification.objects.filter(keywords__word__icontains=web_input,
                                                    level=web_input_for_level).values('course_category', 'courses__name').distinct()
            # getting the python data type
            course_category_from_qualification_list = \
                list(course_category_from_qualification_queryset)
            # finally prepare the data to render
            final_data.extend([item.get('course_category') for item in course_category_from_qualification_list])
            final_data.extend([item.get('courses__name') for item in course_category_from_qualification_list])
            final_data = list(set(final_data))
            # data.extend(models.Course.objects.filter(name__in=final_data, qualification__level=web_input_for_level).distinct('name', 'id'))
            # data.extend(models.Qualification.objects.filter(course_category__in=final_data, level=web_input_for_level).distinct('course_category'))

            data.extend(models.Course.objects.filter(name__in=final_data, qualification__level=web_input_for_level).values().distinct())
            data.extend(models.Qualification.objects.filter(course_category__in=final_data, level=web_input_for_level).values().distinct())

            # for idx, iterable in enumerate(data):
            #     final_data_list.append({'id': iterable.search_code, 'name': get_name(iterable)})

            for idx, iterable in enumerate(data):
                 final_data_list.append({'id': iterable["search_code"], 'name': get_name(iterable)})

    return HttpResponse(json.dumps(final_data_list), content_type="application/json")


def populate_qualification_exam(request):
    data_list = []
    if request.is_ajax():
        web_input_for_course = request.GET.get('course')
        web_input_for_keyword = request.GET.get('q')
        web_input_for_keyword = web_input_for_keyword
        if web_input_for_course in ["null" '', None]:
            web_input_for_course = None
        web_input_for_level = request.GET.get('level')
        qualification_exam_obj = []
        # if web_input_for_level and web_input_for_level is not None:
        #     qualification_exam_obj = \
        #         models.Qualification.objects.filter(level=web_input_for_level, courses__name=web_input_for_course).values('id', 'qualifying_exams__name', 'competitive_exam__name').distinct('qualifying_exams__name')
        print(web_input_for_keyword, web_input_for_level)
        if web_input_for_level and web_input_for_keyword:
            qualification_exam_obj = \
                models.Qualification.objects.filter(level=web_input_for_level).filter(
                Q(qualifying_exams__qualifying_exams_keywords__word__istartswith=web_input_for_keyword) | Q(qualifying_exams__name__istartswith=web_input_for_keyword)).values('qualifying_exams__id', 'qualifying_exams__name', 'competitive_exam__name').distinct('qualifying_exams__name')

        elif web_input_for_level:
            qualification_exam_obj = \
                models.Qualification.objects.filter(level=web_input_for_level).values('qualifying_exams_id', 'qualifying_exams__name', 'competitive_exam__name').distinct('qualifying_exams__name')

        qualification_exam_data_list = list(qualification_exam_obj)
        for item in qualification_exam_data_list:
            data_list.append({'id': item.get('qualifying_exams__id'), 'name': item.get('qualifying_exams__name'),
                              'c_name': item.get('competitive_exam__name'), 'c_id': item.get('competitive_exam__id')})
    return HttpResponse(json.dumps(data_list), content_type="application/json")


def populate_competitve_exam(request):
    data_list = []
    if request.is_ajax():
        web_input_for_course = request.GET.get('course')
        if web_input_for_course in ["null" '', None]:
            web_input_for_course = None
        web_input_for_level = request.GET.get('level')
        web_input_for_q_exm = request.GET.get('q_exm')
        web_input_for_keyword = request.GET.get('keyword')
        # all three are available
        if web_input_for_level and web_input_for_course is not None and web_input_for_q_exm is not None:
            competitve_exam_obj = \
                Qualification.objects.filter(level=web_input_for_level,
                                             courses__name=web_input_for_course,
                                             qualifying_exams__name=web_input_for_q_exm).values('id', 'competitive_exam__name', 'competitive_exam__score_type').distinct('competitive_exam__name')
            if web_input_for_keyword:
                competitve_exam_obj = \
                    competitve_exam_obj.filter(competitive_exam__competitive_exam_keywords__word__istartswith=web_input_for_keyword).values('competitive_exam__id', 'competitive_exam__name', 'competitive_exam__score_type').distinct('competitive_exam__name')

        # level and course are available
        if web_input_for_level and web_input_for_course:
            competitve_exam_obj = \
                models.Qualification.objects.filter(level=web_input_for_level, courses__name=web_input_for_course).values('competitive_exam__id', 'competitive_exam__name').distinct('competitive_exam__name')
            if web_input_for_keyword:
                competitve_exam_obj = \
                competitve_exam_obj.filter(Q(competitive_exam__competitive_exam_keywords__word__istartswith=web_input_for_keyword) | Q(competitive_exam__name__istartswith=web_input_for_keyword)).values('competitive_exam__id', 'competitive_exam__name', 'competitive_exam__score_type').distinct('competitive_exam__name')

        if web_input_for_level and web_input_for_keyword:
            competitve_exam_obj = \
                models.Qualification.objects.filter(level=web_input_for_level
                    ).filter(Q(competitive_exam__competitive_exam_keywords__word__istartswith=web_input_for_keyword) | Q(competitive_exam__name__istartswith=web_input_for_keyword)).values('competitive_exam__id', 'competitive_exam__name', 'competitive_exam__score_type').distinct('competitive_exam__name')


        # if web_input_for_level:
        #     competitve_exam_obj = \
        #         models.Qualification.objects.filter(level=web_input_for_level).values('id', 'competitive_exam__name').distinct('competitive_exam__name')
        competitve_exam_data_list = list(competitve_exam_obj)
        for item in competitve_exam_data_list:
            print(item)
            data_list.append({'id': item.get('competitive_exam__id'), 'name': item.get('competitive_exam__name'),  'exam_type': item.get('competitive_exam__score_type')})
    return HttpResponse(json.dumps(data_list), content_type="application/json")


class AboutView(TemplateView):
    template_name = "aboutus.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class ContactView(TemplateView):
    template_name = "contactus.html"

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class PartnersView(TemplateView):
    template_name = "partners.html"

    def get_p_colleges(self):
        results = []
        for college in models.PartnerCollege.objects.all():
            qualifications = []
            for q in models.CollegeQualification.objects.filter(college=college.college):
                courses = []
                for course in q.qualification.courses.all():
                    courses.append(course.name)
                qualifications.append(
                    {'name': q.qualification.qualification,
                     'courses': courses}
                )
            results.append(
                {
                    'college': college,
                    'qualifications': qualifications
                }
            )
        return results

    def get_context_data(self, **kwargs):
        context = super(PartnersView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class FaqView(TemplateView):
    template_name = "faqs.html"

    def get_context_data(self, **kwargs):
        context = super(FaqView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class PrivacyView(TemplateView):
    template_name = "privacy.html"

    def get_context_data(self, **kwargs):
        context = super(PrivacyView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class TermsView(TemplateView):
    template_name = "tnc.html"

    def get_context_data(self, **kwargs):
        context = super(TermsView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class RefundAssuranceView(TemplateView):
    template_name = "refund-assurance.html"

    def get_context_data(self, **kwargs):
        context = super(RefundAssuranceView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class WhyDependView(TemplateView):
    template_name = "why-you-can-depend-on-us.html"

    def get_context_data(self, **kwargs):
        context = super(WhyDependView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class WorkView(TemplateView):
    template_name = "how-just-rokket-helps-you.html"

    def get_context_data(self, **kwargs):
        context = super(WorkView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class HowView(TemplateView):
    template_name = "how-this-works.html"

    def get_context_data(self, **kwargs):
        context = super(HowView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


class PricingView(TemplateView):
    template_name = "pricing.html"

    def get_context_data(self, **kwargs):
        context = super(PricingView, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context


def get_college(pk):
    s = models.Selection.objects.get(id=pk)
    print("Screen 4 requesting college details")
    return [{'logo': s.college.logo.url, 'course_title': s.course_name, 'college': s.college, 'duration': s.college_qualification.qualification.duration, 'college_qualification': s.college_qualification, 'coupon_code': s.coupon_code}]


def get_agreements(pk):
    y = []
    if models.Selection.objects.get(id=pk).college_qualification.agreements:
        for x in models.Selection.objects.get(id=pk).college_qualification.agreements.statements.all():
            y.append(x.preview)
        print("Agreements ", y)
        return y
    return False


def ask_college(pk):
    s = models.Selection.objects.get(id=pk)
    if s.search.level == 'PG':
        return True
    return False


def ask_school(pk):
    s = models.Selection.objects.get(id=pk)
    if s.search.level == "G":
        return True
    return False


def get_scholarship_details(pk):
    s = models.Selection.objects.get(id=pk)
    return [s]


def get_c_exams(pk):
    s = models.Selection.objects.get(id=pk)
    results = []
    if s.search.compt_exm_type_1:
        e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_1)
        results.append(e)
    if s.search.compt_exm_type_2:
        e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_2)
        results.append(e)
    if s.search.compt_exm_type_3:
        e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_3)
        results.append(e)
    if s.search.compt_exm_type_4:
        e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_4)
        results.append(e)
    if s.search.compt_exm_type_5:
        e = models.CompetitiveExam.objects.get(id=s.search.compt_exm_type_5)
        results.append(e)
    return results


def get_amount_for_order(request, profile_obj, getcollege):
    # check first transaction
    amount = 0
    order_obj = models.Order.objects.filter(profile=profile_obj, status=2)
    if not order_obj:
        # means first transaction
        amount = models.Configuration.objects.first().jr_fee_1
    elif len(order_obj) == 1:
        # charge him for second transaction
        amount = models.Configuration.objects.first().jr_fee_2
    elif len(order_obj) >= 2:
        amount = models.Configuration.objects.first().jr_fee_3
    else:
        amount = 0
    return str(amount)


def formatrequestparameterstoccavnue(request, profile_obj, getcollege):
    p_merchant_id = str(settings.MERCHANT_ID)
    p_order_id = getcollege[0].get('coupon_code')
    p_currency = "INR"
    p_amount = get_amount_for_order(request, profile_obj, getcollege)
    # p_amount = str(getcollege[0].get('college_qualification').pr_fee_l)
    p_redirect_url = settings.BASE_URL + "/payment/redirect/"
    p_cancel_url = settings.BASE_URL + "/payment/cancel/"
    p_language = "EN"
    p_billing_name = profile_obj.name
    p_billing_address = profile_obj.street
    p_billing_city = profile_obj.city
    p_billing_state = profile_obj.state
    p_billing_zip = profile_obj.pin
    p_billing_country = profile_obj.country if profile_obj.country else "INDIA"
    p_billing_tel = profile_obj.mobile
    p_billing_email = request.user.email
    p_delivery_name = profile_obj.name
    p_delivery_address = profile_obj.street
    p_delivery_city = profile_obj.city
    p_delivery_state = profile_obj.state
    p_delivery_zip = profile_obj.pin
    p_delivery_country = profile_obj.country if profile_obj.country else "INDIA"
    p_delivery_tel = profile_obj.mobile
    p_merchant_param1 = "AdditonInfor1"
    p_merchant_param2 = "AdditonInfor2"
    p_merchant_param3 = "AdditonInfor3"
    p_merchant_param4 = "AdditonInfor4"
    p_merchant_param5 = "AdditonInfor5"
    p_promo_code = ""
    p_customer_identifier = str(request.user.id)
    merchant_data ='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email='+p_billing_email+'&'+'delivery_name='+p_delivery_name+'&'+'delivery_address='+p_delivery_address+'&'+'delivery_city='+p_delivery_city+'&'+'delivery_state='+p_delivery_state+'&'+'delivery_zip='+p_delivery_zip+'&'+'delivery_country='+p_delivery_country+'&'+'delivery_tel='+p_delivery_tel+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier+'&'

    encryption = encrypt(merchant_data, settings.TEST_WORKING_KEY)
    return encryption


def profile_view(request, pk):
    '''
    This is screen 4 view.
    :param request:
    :param pk:
    :return:
    '''
    if request.session.get('next'):
        del request.session['next']
    request.session['next'] = request.get_full_path()
    getcexams = get_c_exams(pk)
    askcollege = ask_college(pk)
    askschool = ask_school(pk)
    getcollege = get_college(pk)
    getagreements = get_agreements(pk)
    getscholarshipdetails = get_scholarship_details(pk)
    encryption = None
    profile = None
    if request.method == "POST":
        request.POST._mutable =True
        try:
            request.POST['search_id'] = request.get_full_path().split("/")[-1]
        except:
            pass
        form_data = forms.Screen4Form(request.POST)
        # temporary for new flow #
        request.user.email = request.POST.get("email")
        request.user.save()
        if form_data.is_valid():
            cd = form_data.cleaned_data
            try:
                if not request.user:
                    user_obj, created = \
                        models.User.objects.get_or_create(username=cd.get("email"))
                else:
                    user_obj = request.user
                user_obj.save()
                profile_obj, created = models.Profile.objects.get_or_create(user=user_obj)
                profile_obj.name = cd.get('name')
                profile_obj.dob = cd.get('dob')
                profile_obj.parent_email = cd.get('parent_email', None)
                profile_obj.gender = cd.get('gender')
                profile_obj.email = cd.get('email')
                profile_obj.mobile = cd.get('phone')
                profile_obj.address = cd.get('address')
                profile_obj.college = cd.get('college_name')
                profile_obj.college_location = cd.get('college_location')
                profile_obj.school = cd.get('school_name')
                profile_obj.school_location = cd.get('school_location')
                profile_obj.graduation_year = cd.get('graduation_year')
                profile_obj.tab_flag = "Profile"
                profile_obj.school = cd.get('class_12_year')
                profile_obj.school_location = cd.get('class_12_year')
                profile_obj.class_12_year = cd.get('class_12_year')
                profile_obj.email_verified = True
                profile_obj.mobile_verified = True
                try:
                    profile_obj.save()
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
                try:
                    # encryption = formatrequestparameterstoccavnue(request, profile_obj, getcollege)
                    # This is to be brought back after temporary control flow
                    None
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
                selection_obj = models.Selection.objects.filter(coupon_code=getcollege[0].get('coupon_code')).latest('id')
                # create order object
                order, created = \
                    models.Order.objects.get_or_create(order_number=selection_obj.coupon_code,
                                                       selection=selection_obj,
                                                       profile=profile_obj,
                                                       status=2, #FIXME: change to 1 when reverting control flow.
                                                       )
                try:
                    order.amount = get_amount_for_order(request, profile_obj, getcollege)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
                order.tnc = cd.get('tnc')
                from django.forms.models import model_to_dict  # lazy load                
                order.save()
                # FIXME: An silent fail occurs if the admin has failed to add amounts to the configuration table. \
                # This error needs to be caught and handled.

                if not request.user.is_authenticated():
                    login(request, user_obj)
                    #return HttpResponseRedirect(request.META.get('HTTP_REFERER')+"#payment")
                    return HttpResponseRedirect("/thank-you/"+pk+"?email=None")
                #return HttpResponseRedirect(request.META.get('HTTP_REFERER')+"#payment")
                return HttpResponseRedirect("/thank-you/"+pk+"?email=None")
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
        else:
            print(form_data.errors)
    else:
        try:
            user = request.user
            profile = request.user.profile
            data_dict = {'email': request.user.email,
                         'name': profile.name,
                         'dob': profile.dob,
                         'gender': profile.gender,
                         'phone':profile.mobile,
                         'school': profile.school,
                         'class_12_year': profile.class_12_year,
                         'address': profile.address,
                         'parent_email': profile.parent_email,
                         }
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
        try:
            form_data = forms.Screen4Form(initial=data_dict)
            selection_obj = models.Selection.objects.filter(coupon_code=getcollege[0].get('coupon_code')).latest('id')
            order = \
                    models.Order.objects.filter(order_number=selection_obj.coupon_code,
                                                selection=selection_obj,
                                                profile=profile,
                                                status=2, #FIXME: Change to 1 when reverting control flow.
                                                amount=get_amount_for_order(request, profile, getcollege),
                                                ).latest('id')
            data_dict['tnc'] = order.tnc
            # encryption = formatrequestparameterstoccavnue(request, profile, getcollege)
            encryption = None
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
            encryption = None
            try:
                form_data = forms.Screen4Form(initial=data_dict)
            except Exception as e:
                form_data = forms.Screen4Form()
    context = {'form': form_data, 'get_c_exams': getcexams,
               'ask_college': askcollege, 'ask_school': askschool, 'get_college': getcollege,
               'get_agreements': getagreements,
               'get_scholarship_details': getscholarshipdetails,
               'encryption': encryption,
               'access_code': settings.TEST_ACCESS_CODE,
               'profile_obj': profile, 'pk': pk,
               'email': request.POST.get("email"),
               'scholarship':getscholarshipdetails[0].scholarship,
               'cert_detail':models.Selection.objects.get(id=pk),
               'amount': get_amount_for_order(request, profile, getcollege) if get_amount_for_order(request, profile, getcollege) else 0}
    template = "screen4-new.html"
    return render(request, template, context)


def get_order_status(string):
    b = string.split('&')
    results = []
    for c in b:
        d = c.split('=')
        if len(d) == 2:
            e = {'attr': d[0], 'val': d[1]}
        results.append(e)
    for item in results:
        if item['attr'] == "order_status":
            return item['val']


@csrf_exempt
def redirectview(request):
    workingKey = settings.TEST_WORKING_KEY
    # <QueryDict: {u'encResp': [u'47c128b6ceca5d6a2cbea49e2df9ddf065c833798a8758b804a528c6269abf273fc513e9139c4c670667ef55f4141c6f5c00c3c34b21872ba624000240a098b6bdc07b4b1660954863a3fe5fcfeff8afa6bab074f41bcaed984aee22fe39a34bed70a26dd89940e2f6fe22e99a73142fc8ad020cf6eac505774bb29efd23013b28a8c14a375ad5f02c54cd5944aacf1999394e9afeba2bfa9359fbab5c056e9119685a53c01ba38b6bb0ec99aaa7ac257755c42a4a6f9cc34b39616f1a2a55995f05c51608c6f1fa7a7aa4b667bb4697bf1a44ba2f2ddf60b41a62803265d7fcf3666a9ec6702e8ca51d116cd9675f7955e6f21d10f317ece68a4fcce4f0dfa7bf62ab8c2efb3ff85d83ba447c038d3fb3ec11e079089953aedb50626d38b3552a69e87d50fa1c3ebf122434791bd842f11681a7d56075990edf95af0398b773d7c49edbbac7605b294e540f1991be296d7bf9910fdc9bd5a2fccbccb681dca17d801b63a6b5f4ee5f8ab2006f80176acef5cfa0e17bcfb7e470595b8d3f216b532bdce0b59f51c9ca661ccecf0af494cb37bc6aa59afecbecab9e7c3b2ddad437fcb5a0742dbc3ae03b6b6c10545001feead2e81a0775ad5156068f18c56521496192e09d20d7172cab829026da522196c8b2f8cac3da5e07d70e403144d51905fc479e9c2700cb5456cde780d0c6635389bbb756e264c562ad75f6ec7a6f10051d4539a8b85f6447bf058e06baa1c42865509f289325e9c5c45a37d88a0a4ef3f8794f832bc4c6874af574400bba4ba1556fe42336e9e85a6a6d7ba8a7f30a62c61cf4a1bf38e3b816c79f678b6400ccc8067540ed89e99d6bed068c390876fb7ed23b856ed87f9f981e63f5cbe85fc794495dabdc2970683e4b47794ccd9e7893054038889c520115342d7bb826fa415e019cff5b7df2342dfa422fa792836485284cca7e9ad85a4334ff570d7aae2911eedab573e479358a28f1674bc75ee6efc847b0ec2e49b9579c05efc4e548cf44633d55577e00a19b270a412810e0eaf0cf2e6ee4710231f1c87192a1b9850e6788793d90d33dce5309023afb17e0e1894266123ad2c499fff7c5d41cc691505ca070dd17a151410b8c86edce3551ccc6c945e1c9d0fd7a5db4338624d8b55a26dbd076f1740fae57a849f09bc7864ce51aa7999013db8f834945b26df8756d6b920d828dfdfa2a6318ac6aa8c14b2c9d0117b5e01c71eb5468631c73e99b427c7c2ad85382d510e47c66c7755de0be508f5a0420309260c06358f08c98539ffae3a5e2a6c9a4cae74613393f60e8'], u'orderNo': [u'JR59AS25']}>
    pk = request.user.profile.id
    encryption = None
    var = None
    decResp = decrypt(request.POST.get('encResp'), workingKey)
    if get_order_status(decResp) == "Failure":
        return HttpResponseRedirect("/payment/cancel")
    order_no = request.POST.getlist('orderNo')
    user_obj = request.user
    profile_obj, created = models.Profile.objects.get_or_create(user=user_obj)
    order_obj = models.Order.objects.filter(order_number__in=order_no).latest('id')
    order_obj.status = 2
    order_obj.save()

    if order_obj.selection.decrement_from == "cc":
        a = order_obj.selection.cc_obj
        a.seats = int(order_obj.selection.cc_obj.seats) - 1
        a.save()
    elif order_obj.selection.decrement_from == "cq":
        a = order_obj.selection.college_qualification
        a.seats = int(order_obj.selection.college_qualification.seats) - 1
        a.save()

    getcexams = get_c_exams(order_obj.selection.id)
    askcollege = ask_college(order_obj.selection.id)
    askschool = ask_school(order_obj.selection.id)
    getcollege = get_college(order_obj.selection.id)
    getagreements = get_agreements(order_obj.selection.id)
    getscholarshipdetails = get_scholarship_details(order_obj.selection.id)
    selection = order_obj.selection
    context = {'profile_obj': profile_obj, 'redirect': True, 'order_obj': order_obj, 'get_selection': selection}
    template = "screen6.html"

    # Email to college
    email_template = models.EmailTemplate.objects.filter(type="COLLEGE_EMAIL").first()
    subject = email_template.subject
    message = email_template.html
    message = message.replace("*|NAME|*", request.user.email)
    message = message.replace("*|GOVT_ID_TYPE|*", profile_obj.id_type)
    message = message.replace("*|GOVT_ID|*", profile_obj.id_no)
    message = message.replace("*|GENDER|*", profile_obj.gender)
    if profile_obj.dob:
        message = message.replace("*|DOB|*", profile_obj.dob.strftime('%m/%d/%Y'))
    message = message.replace("*|ADDRESS|*", profile_obj.get_address())
    message = message.replace("*|VERIFIED_EMAIL|*", profile_obj.user.email)
    message = message.replace("*|VERIFIED_MOBILE|*", profile_obj.user.profile.mobile)
    message = message.replace("*|AMOUNT|*", str(order_obj.amount))
    message = message.replace("*|NEXT_SELECTION_STEPS|*", selection.college_qualification.next_selection_steps)
    message = message.replace("*|SELECTION_WITHIN_DAYS|*", str(selection.college_qualification.nst_closure_within))
    message = message.replace("*|COURSE_SELECTED|*", selection.course_name)
    message = message.replace("*|INSTITUTION_ADDRESS|*", selection.college.institution_address())
    message = message.replace("*|SESSION|*", selection.college_qualification.session.get_session())
    message = message.replace("*|SCHOLARSHIP|*", selection.scholarship)
    message = message.replace("*|STUDENT_NAME|*", request.user.profile.name)
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[str(selection.college.email)],
    )

    email_template = models.EmailTemplate.objects.filter(type="PURCHASEDSCHL").first()
    subject = email_template.subject
    message = email_template.html
    message = message.replace("*|NAME|*", request.user.email)
    message = message.replace("*|INSTITUTION_NAME|*", selection.college.name)
    message = message.replace("*|INSTITUTION_ADDRESS|*", selection.college.institution_address())
    message = message.replace("*|COURSE_SELECTED|*", selection.course_name)
    message = message.replace("*|SESSION|*", selection.college_qualification.session.get_session())
    message = message.replace("*|STUDENT_NAME|*", profile_obj.name)
    message = message.replace("*|COURSE_NAME|*", selection.course_name)
    message = message.replace("*|SCHOLARSHIP|*", selection.scholarship)
    message = message.replace("*|FINAL_FEE|*", selection.final_fee)
    message = message.replace("*|SELECTION_WITHIN_DAYS|*", str(selection.college_qualification.nst_closure_within))
    message = message.replace("*|NEXT_SELECTION_STEPS|*", str(selection.college_qualification.next_selection_steps))
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[str(request.user.email)],
    )
    # email_template = models.EmailTemplate.objects.filter(type="INVOICE").first()
    # subject = email_template.subject
    # message = email_template.html
    # message = message.replace("*|NAME|*", request.user.email)
    # message = message.replace("*|INSTITUTION_NAME|*", selection.college.name)
    # message = message.replace("*|INSTITUTION_ADDRESS|*", selection.college.institution_address())
    # message = message.replace("*|COURSE_SELECTED|*", selection.course_name)
    # message = message.replace("*|SESSION|*", selection.college_qualification.session.get_session())
    # message = message.replace("*|STUDENT_NAME|*", profile_obj.name)
    # message = message.replace("*|STUDENT_ID|*", str(profile_obj.user.id))
    # message = message.replace("*|COURSE_NAME|*", selection.course_name)
    # message = message.replace("*|SCHOLARSHIP|*", selection.scholarship)
    # message = message.replace("*|FINAL_FEE|*", selection.final_fee)
    # message = message.replace("*|AMOUNT|*", str(order_obj.amount))
    # message = message.replace("*|SELECTION_WITHIN_DAYS|*", str(selection.college_qualification.nst_closure_within))
    # message = message.replace("*|NEXT_SELECTION_STEPS|*", str(selection.college_qualification.next_selection_steps))
    # send_mail(
    #     subject=subject,
    #     message=message,
    #     recipient_list=[str(request.user.email)],
    # )
    if profile_obj.parent_email and profile_obj.parent_email != "":
        email_template = models.EmailTemplate.objects.filter(type="PARENTEMAIL").first()
        subject = email_template.subject
        message = email_template.html
        message = message.replace("*|NAME|*", request.user.email)
        message = message.replace("*|INSTITUTION_NAME|*", selection.college.name)
        message = message.replace("*|INSTITUTION_ADDRESS|*", selection.college.institution_address())
        message = message.replace("*|COURSE_SELECTED|*", selection.course_name)
        message = message.replace("*|SESSION|*", selection.college_qualification.session.get_session())
        message = message.replace("*|STUDENT_NAME|*", profile_obj.name)
        message = message.replace("*|COURSE_NAME|*", selection.course_name)
        message = message.replace("*|SCHOLARSHIP|*", selection.scholarship)
        message = message.replace("*|FINAL_FEE|*", str(selection.final_fee))
        message = message.replace("*|SELECTION_WITHIN_DAYS|*", str(selection.college_qualification.nst_closure_within))
        message = message.replace("*|NEXT_SELECTION_STEPS|*", str(selection.college_qualification.next_selection_steps))
        send_mail(
            subject=subject,
            message=message,
            recipient_list=[str(request.user.profile.parent_email)],
        )
    # return render(request, template, context)
    return redirect("/thank-you/%s" % selection.id)


@csrf_exempt
def cancelview(request):
    user_obj = request.user
    profile_obj = models.Profile.objects.get_or_create(user=user_obj)
    context = {'profile_obj': profile_obj, 'redirect': True}
    template = "cancel.html"
    return render(request, template, context)


class ForgotPassword(FormView):
    template_name = "registration/forgot-password.html"
    form_class = forms.ForgotPassword

    def form_valid(self, form):
        email = self.request.POST.get("email")
        users = models.User.objects.filter(email=email)
        if len(users) > 1:
            # add_message(self.request, 40, "We have messed up. Please contact customer care.")
            response_data = {}
            response_data['msg'] = "We have messed up. Please contact customer care."
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif len(users) == 1 and users is not None:
            # add_message(self.request, 40, "An email with a link to reset your password has been sent. Please click on it to continue.")
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            models.OTP.objects.create(
                key=key,
                type="email",
                email=email
            )
            _message = models.EmailTemplate.objects.filter(type="FORGOTPASSWORD").first()
            message = _message.html
            x = "https://www.justrokket.com/forgot-password/verify-otp/"+str(key)
            message = message.replace("*|LINK|*", x)
            subject = _message.subject
            send_mail(
                subject="You requested to reset your password on JustRokket",
                message=message,
                recipient_list=[email],
            )
            response_data = {}
            response_data['msg'] = "Recovery Email has been sent."
        else:
            response_data = {}
            response_data['msg'] = "Please input the correct email."
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def get_success_url(self):
        users = models.User.objects.filter(email=self.request.POST.get("email"))
        if len(users) == 1 and users is not None:
            return "/forgot-password/verify-otp"
        else:
            return "/forgot-password/"


class ForgotPasswordVerifyOTP(View):
    template_name = "registration/forgot-password-otp.html"
    # form_class = forms.ForgotPasswordVerifyOTP

    def get(self, request, *args, **kwargs):
        otp = models.OTP.objects.filter(key=self.kwargs['otp']).first()
        if otp is not None and not otp.used:
            otp.used = True
            otp.save()
            return HttpResponseRedirect("/forgot-password/new-password/"+str(otp.key))
        else:
            return HttpResponseRedirect("/")


class ForgotPasswordNewPassword(FormView):
    template_name = "registration/forgot-password-new-password.html"
    form_class = forms.ForgotPasswordNewPassword

    def form_valid(self, form):
        if self.request.POST.get("password") != self.request.POST.get("repeat_password"):
            return HttpResponseRedirect(self.request.META.get("HTTP_REFERER"))
        email = models.OTP.objects.filter(key=self.kwargs['otp']).first().email
        user = models.User.objects.get(email=email)
        user.set_password(self.request.POST.get("password"))
        user.save()
        print(self.request.POST.get("password"))
        return HttpResponseRedirect("/")


class ResetPasswordProfilePage(LoginRequiredMixin, FormView):
    template_name = "registration/forgot-password.html"
    form_class = forms.ForgotPasswordNewPassword

    def form_valid(self, form):
        if self.request.POST.get("password") != self.request.POST.get("repeat_password"):
            return HttpResponseRedirect(self.request.META.get("HTTP_REFERER"))
        user = self.request.user
        user.set_password(self.request.POST.get("password"))
        user.save()
        _auth = authenticate(username=user.username, password=self.request.POST.get("password"))
        if _auth is not None:
            login(self.request, _auth)
        return HttpResponseRedirect("/profile/"+str(self.request.user.profile.id))


class ContactForm(CreateView):
    model = models.ContactUsMessages
    fields = "__all__"
    template_name = "contactus.html"
    success_url = "/contact-us/"

    def get_context_data(self, **kwargs):
        context = super(ContactForm, self).get_context_data(**kwargs)
        if self.request.session.get('next'):
            del self.request.session['next']
        self.request.session['next'] = self.request.get_full_path()
        return context

    def form_valid(self, form):
        send_mail(
                subject="You have received a new message via the contact page on your website",
                message="Name: " + self.request.POST.get("first_name") + " " + self.request.POST.get("last_name") + "<br>" + \
                "message: " + self.request.POST.get("message") + " <br> Access all details via the admin panel.",
                recipient_list=[models.Configuration.objects.first().admin_contact_email],
            )
        return super(ContactForm, self).form_valid(form)


class FaviconView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/static/favicon.ico")


class Newsletter(FormView):
    form_class = forms.NewsletterForm
    template_name = "base.html"

    def form_invalid(self, form):
        add_message(self.request, 25, "Please enter a valid email and try again.")
        return super(Newsletter, self).form_invalid(form)

    def form_valid(self, form):
        e = models.Newsletter.objects.filter(email=self.request.POST.get("email")).first()
        if e is not None:
            add_message(self.request, 25, "Hey! You're already subscribed to the list. ")
            return super(Newsletter, self).form_valid(form)
        models.Newsletter.objects.create(
            email=self.request.POST.get("email")
        )
        add_message(self.request, 25, "Congratulations! You are subscribed to Just Rokket's Newsletter")
        return super(Newsletter, self).form_valid(form)


    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class RequestRefund(TemplateView):

    def get(self, request, *args, **kwargs):
        o = models.Order.objects.get(id=self.kwargs['pk'])
        o.refund_requested = True
        o.refund_requested_on = datetime.datetime.now()
        from datetime import timedelta #lazy import
        o.refund_due_date = datetime.datetime.now() + timedelta(days=15)
        o.refund_reason = self.request.GET.get("why")
        o.save()
        print(self.request.META.get("HTTP_REFERRER"))
        return HttpResponseRedirect(self.request.META.get("HTTP_REFERER")+"#tab2")


def error404(request):

    template = loader.get_template('404-error.html')
    context = Context({
        'message': 'All: %s' % request,
        })
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)