# from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from string import ascii_letters, whitespace, punctuation, digits
import string
# Create your models here.


from django.db.models.signals import post_save,pre_save,m2m_changed
from django.contrib.contenttypes.models import ContentType
from qa.models import tag,Question,Answer


import datetime

from .utils import send_mail

LEVEL_CHOICES = (
    ('G', 'G'),
    ('PG', 'PG')
)


class City(models.Model):
    name = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    long = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class College(models.Model):

    CAT_CHOICES = (
        ('GA', 'GA'),
        ('QA', 'QA'),
        ('C', 'C')
    )
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=64, choices=CAT_CHOICES)
    hold = models.BooleanField(default=False)
    pop_score = models.IntegerField()
    weight = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(-5)])
    street_1 = models.TextField()
    street_2 = models.TextField()
    city = models.ForeignKey("City", on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey("District", on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey("State", on_delete=models.SET_NULL, null=True)
    pin = models.IntegerField()
    campus = models.TextField()
    email = models.EmailField()
    website = models.URLField()
    logo = models.ImageField()
    lat = models.CharField(max_length=100)
    long = models.CharField(max_length=100)
    qualifications = models.ManyToManyField("Qualification")
    seats = models.IntegerField(verbose_name="System Field. Leave this blank.", null=True, blank=True)

    images = models.ManyToManyField("Image")

    def __str__(self):
        return self.name

    def institution_address(self):
        address = self.street_1 + " " + self.street_2 + " " + self.city.name + " " + self.district.name + " " + self.state.name
        return address


class AFCR(models.Model):
    text = models.TextField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.text


class Qualification(models.Model):

    qualification = models.TextField()
    course_category = models.TextField()
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    courses = models.ManyToManyField("Course", blank=True)
    competitive_exam = models.ManyToManyField("CompetitiveExam", blank=True)
    qualifying_exams = models.ManyToManyField("QualifyingExam")
    keywords = models.ManyToManyField("GeneralKeyword")
    search_code = models.CharField(max_length=10, null=True, blank=True)
    duration = models.IntegerField()

    def save(self, *args, **kwargs):
        # if not self.search_code and not self.pk:
        #     val = Qualification.objects.latest('id').id
        #     self.search_code = "QL" + str(val+1)
        # if not self.search_code:
        #     self.search_code = "QL"+ str(self.pk)
        super(Qualification, self).save(*args, **kwargs)

    def __str__(self):
        return self.qualification


class Course(models.Model):
    name = models.TextField()
    keywords = models.ManyToManyField("SpecializedKeyword")
    search_code = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        # if not self.search_code and not self.pk:
        #     val = Course.objects.latest('id').id
        #     self.search_code = "CO" + str(val+1)
        # if not self.search_code:
        #     self.search_code = "CO"+ str(self.pk)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CollegeCourse(models.Model):

    TIME_PERIOD = (
        ('Year', 'Year'),
        ('Month', 'Month'),
        ('Semester', 'Semester')
    )
    college = models.ForeignKey("College", on_delete=models.SET_NULL, null=True)
    qualification = models.ForeignKey("Qualification", on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey("Course", on_delete=models.SET_NULL, null=True)
    session = models.ForeignKey("Session", on_delete=models.SET_NULL, null=True)
    fee = models.IntegerField()
    time_unit = models.CharField(max_length=64, choices=TIME_PERIOD)
    seats = models.IntegerField(null=True, blank=True)
    approval_period = models.ForeignKey('ApprovalPeriod', null=True, on_delete=models.SET_NULL)
    schl_l = models.IntegerField()
    schl_m = models.IntegerField()
    schl_h = models.IntegerField()

    def __str__(self):
        return str(self.college.id) + ": " + self.college.name + " - " + self.course.name + " - " + self.qualification.qualification + " - " +  str(self.approval_period.date_from) + " : " + str(self.approval_period.date_to)


class CollegeQualification(models.Model):

    TIME_PERIOD = (
        ('Year', 'Year'),
        ('Month', 'Month'),
        ('Semester', 'Semester')
    )
    college = models.ForeignKey("College", on_delete=models.SET_NULL, null=True)
    qualification = models.ForeignKey("Qualification", on_delete=models.SET_NULL, null=True)
    pr_fee_l = models.BigIntegerField()
    pr_fee_m = models.BigIntegerField()
    pr_fee_h = models.BigIntegerField()
    schl_l = models.IntegerField()
    schl_m = models.IntegerField()
    schl_h = models.IntegerField()

    rec_app = models.ForeignKey("Rec_app", on_delete=models.SET_NULL, null=True, blank=True)
    next_selection_steps = models.TextField(null=True, blank=True)
    nst_closure_within = models.IntegerField(null=True, blank=True)
    conf_within = models.IntegerField()
    session = models.ForeignKey("Session", null=True, on_delete=models.SET)
    seats = models.IntegerField(null=True, blank=True)
    approval_period = models.ForeignKey("ApprovalPeriod", null=True, on_delete=models.SET_NULL)

    college_quality_index=models.DecimalField(null=True,blank=True,max_digits=5,decimal_places=2)

    af_cr = models.ManyToManyField("AFCR",blank=True)
    session_start = models.DateField()

    b1 = models.ForeignKey("StaticText", related_name="s1+", on_delete=models.SET_NULL, null=True, blank=True)
    b2 = models.ForeignKey("StaticText", related_name="s2+", on_delete=models.SET_NULL, null=True, blank=True)
    b3 = models.ForeignKey("StaticText", related_name="s3+", on_delete=models.SET_NULL, null=True, blank=True)
    b4 = models.ForeignKey("StaticText", related_name="s4+", on_delete=models.SET_NULL, null=True, blank=True)
    b5 = models.ForeignKey("StaticText", related_name="s4+", on_delete=models.SET_NULL, null=True, blank=True)

    guarantee = models.BooleanField(default=False)

    important_info = models.ForeignKey("StatementGroup", related_name="sg1", null=True, blank=True, on_delete=models.SET_NULL)
    other_benefits = models.ForeignKey("StatementGroup", related_name="sg2", null=True, blank=True, on_delete=models.SET_NULL)
    info_scholarship = models.ForeignKey("StatementGroup", related_name="sg3", null=True, blank=True, on_delete=models.SET_NULL)
    info_admission_process = models.ForeignKey("StatementGroup", related_name="sg4", null=True, blank=True, on_delete=models.SET_NULL)
    agreements = models.ForeignKey("StatementGroup", related_name="sg5", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.qualification:
            return str(self.college.id) + ": " + self.college.name + " - " + self.qualification.qualification + " - " + str(self.approval_period.date_from) + " : " + str(self.approval_period.date_to)
        else:
            return str("No qualification name" )


class Rec_app(models.Model):
    text = models.TextField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.text


class Session(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return str(self.date_to) + " " + str(self.date_from)

    def get_session(self):
        return str(self.date_from.year) + " - " + str(self.date_to.year)


class CompetitiveExam(models.Model):

    SCORE_TYPE = (
        ('Percentage', 'Percentage'),
        ('Percentile', 'Percentile'),
        ('Rank', 'Rank'),
        ('Score', 'Score')
    )
    name = models.TextField()
    competitive_exam_keywords = models.ManyToManyField("GeneralKeyword",
                                                       related_name="competitive_exam_keywords")
    score_type = models.CharField(choices=SCORE_TYPE, max_length=10)
    l_cutoff = models.IntegerField()
    m_cutoff = models.IntegerField()
    h_cutoff = models.IntegerField()

    def __str__(self):
        return self.name


class QualifyingExam(models.Model):

    SCORE_TYPE = (
        ('Percentage', 'Percentage'),
        ('Percentile', 'Percentile'),
        ('Rank', 'Rank')
    )
    qualifying_exams_keywords = models.ManyToManyField("GeneralKeyword",
                                                       related_name="qualifying_exams_keywords")
    name = models.TextField()
    score_type = models.CharField(choices=SCORE_TYPE, max_length=10)
    l_cutoff = models.IntegerField()
    m_cutoff = models.IntegerField()
    h_cutoff = models.IntegerField()

    def __str__(self):
        return self.name


class GeneralKeyword(models.Model):
    word = models.TextField()

    def __str__(self):
        return self.word


class SpecializedKeyword(models.Model):
    word = models.TextField()

    def __str__(self):
        return self.word


class Search(models.Model):
    level = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    course_type = models.CharField(max_length=64)
    course = models.CharField(max_length=64)
    q_exm = models.CharField(max_length=64, null=True)
    q_exm_score = models.CharField(max_length=64)
    compt_exm_type_1 = models.CharField(max_length=64, null=True, blank=True)
    compt_exm_score_1 = models.CharField(max_length=64, null=True, blank=True)
    compt_exm_type_2 = models.CharField(max_length=64, null=True, blank=True)
    compt_exm_score_2 = models.CharField(max_length=64, null=True, blank=True)
    compt_exm_type_3 = models.CharField(max_length=64, null=True, blank=True)
    compt_exm_score_3 = models.CharField(max_length=64, null=True, blank=True)
    compt_exm_type_4 = models.CharField(max_length=64, null=True, blank=True)
    compt_exm_score_4 = models.CharField(max_length=64, null=True, blank=True)
    compt_exm_type_5 = models.CharField(max_length=64, null=True, blank=True)
    compt_exm_score_5 = models.CharField(max_length=64, null=True, blank=True)
    screen_6_text = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return str(self.id) + ":" +self.level


class PartnerCollege(models.Model):
    college = models.ForeignKey("College", null=True, blank=False)
    logo = models.ImageField()
    description = models.TextField()
    title = models.CharField(max_length=100)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    homepage_display = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Rokketeer(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField()
    to_date = models.DateField()
    from_date = models.DateField()
    homepage_display = models.BooleanField(default=True)


class Selection(models.Model):
    coupon_code = models.CharField(max_length=100)
    college = models.ForeignKey("College", on_delete=models.SET_NULL, null=True)
    scholarship = models.CharField(max_length=200)
    fee = models.CharField(max_length=200)
    final_fee = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    college_qualification = models.ForeignKey("CollegeQualification", on_delete=models.SET_NULL, null=True)
    search = models.ForeignKey('Search', on_delete=models.SET_NULL, null=True)
    savings = models.IntegerField(null=True)
    total_savings = models.IntegerField(null=True)
    seats = models.IntegerField(null=True)
    decrement_from = models.TextField(null=True, blank=True)
    cc_obj = models.ForeignKey("CollegeCourse", null=True, blank=True)

    def __unicode__(self):
        return str(self.id)+":"+self.coupon_code


class Event1(models.Model):

    ICON_LIB = (
        ('fa', 'Font Awesome'),
    )

    ICON_SIZE = (
        ('fa-2x', 'fa-2x'),
        ('fa-3x', 'fa-3x'),
        ('fa-4x', 'fa-4x'),
        ('fa-5x', 'fa-5x'),
    )

    ICON_NAME = (
        ('fa-bell-o', 'fa-bell-o'),
        ('fa-handshake-o', 'fa-handshake-o'),
        ('fa-certificate', 'fa-certificate'),
        ('fa-calendar', 'fa-calendar'),
        ('fa-plus-circle', 'fa-plus-circle'),
        ('fa-university', 'fa-university'),
    )

    activate = models.BooleanField(default=True)
    parameter1 = models.ManyToManyField("QualifyingExam", related_name="parameter1+", verbose_name="When X is not selected for G", blank=True)
    parameter2 = models.ManyToManyField("QualifyingExam", related_name="parameter2+", verbose_name="When X is not selected for PG", blank=True)
    preview = models.TextField(verbose_name="Preview for BOX", null=True, blank=True)
    description = models.TextField(verbose_name="Description for BOX", null=True, blank=True)
    preview2 = models.TextField(verbose_name="Preview for Accordian", null=True, blank=True)
    description2 = models.TextField(verbose_name="Description for Accordian", null=True, blank=True)
    icon_lib = models.CharField(max_length=100, choices=ICON_LIB, null=True, blank=True)
    icon_name = models.CharField(max_length=100, choices=ICON_NAME, null=True, blank=True)
    icon_size = models.CharField(max_length=100, choices=ICON_SIZE, null=True, blank=True)
    icon_color = models.CharField(max_length=7, null=True, blank=True)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)


class Event2(models.Model):

    ICON_LIB = (
        ('fa', 'Font Awesome'),
    )

    ICON_SIZE = (
        ('fa-2x', 'fa-2x'),
        ('fa-3x', 'fa-3x'),
        ('fa-4x', 'fa-4x'),
        ('fa-5x', 'fa-5x'),
    )

    ICON_NAME = (
        ('fa-bell-o', 'fa-bell-o'),
        ('fa-handshake-o', 'fa-handshake-o'),
        ('fa-certificate', 'fa-certificate'),
        ('fa-calendar', 'fa-calendar'),
        ('fa-plus-circle', 'fa-plus-circle'),
        ('fa-university', 'fa-university'),
        ('fa-exclamation', 'fa-exclamation'),
        ('fa-gift', 'fa-gift'),
        ('fa-money', 'fa-money'),
    )

    activate = models.BooleanField(default=True)
    preview = models.TextField(verbose_name="Preview for BOX", null=True, blank=True)
    description = models.TextField(verbose_name="Description for BOX", null=True, blank=True)
    preview2 = models.TextField(verbose_name="Preview for Accordian", null=True, blank=True)
    description2 = models.TextField(verbose_name="Description for Accordian", null=True, blank=True)
    preview3 = models.TextField(verbose_name="If Not: Preview for Accordian", null=True, blank=True)
    description3 = models.TextField(verbose_name="If Not: Description for Accordian", null=True, blank=True)
    icon_lib = models.CharField(max_length=100, choices=ICON_LIB, null=True, blank=True)
    icon_name = models.CharField(max_length=100, choices=ICON_NAME, null=True, blank=True)
    icon_size = models.CharField(max_length=100, choices=ICON_SIZE, null=True, blank=True)
    icon_color = models.CharField(max_length=7, null=True, blank=True)


class StaticText(models.Model):

    ICON_LIB = (
        ('fa', 'Font Awesome'),
    )

    ICON_SIZE = (
        ('fa-2x', 'fa-2x'),
        ('fa-3x', 'fa-3x'),
        ('fa-4x', 'fa-4x'),
        ('fa-5x', 'fa-5x'),
    )

    ICON_NAME = (
        ('fa-bell-o', 'fa-bell-o'),
        ('fa-handshake-o', 'fa-handshake-o'),
        ('fa-certificate', 'fa-certificate'),
        ('fa-calendar', 'fa-calendar'),
        ('fa-plus-circle', 'fa-plus-circle'),
        ('fa-university', 'fa-university'),
        ('fa-exclamation', 'fa-exclamation'),
        ('fa-gift', 'fa-gift'),
        ('fa-money', 'fa-money'),
    )

    TYPE_CHOICES = (
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('A3', 'A3'),
        ('A4', 'A4'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('B3', 'B3'),
        ('B4', 'B4'),
        ('Agreement', 'Agreement'),
        ('Other', 'Other'),
    )

    preview = models.TextField()
    description = models.TextField(null=True, blank=True)
    icon_lib = models.CharField(max_length=100, choices=ICON_LIB, null=True, blank=True)
    icon_name = models.CharField(max_length=100, choices=ICON_NAME, null=True, blank=True)
    icon_size = models.CharField(max_length=100, choices=ICON_SIZE, null=True, blank=True)
    icon_color = models.CharField(max_length=7, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        a = (self.preview[:75] + '..') if len(self.preview) > 75 else self.preview
        return self.type + " : " + a
#return self.clean_text(self.type) + " : " + self.clean_text(a)

    def clean_text(self, text):
        replace_punctuation = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        try:
            text = text.decode('utf-8', 'ignore')
        except:
            text = text.encode('utf-8', 'ignore')
            text = text.decode('utf-8', 'ignore')
        text = text.encode('ascii', 'ignore').lower().translate(replace_punctuation)
        text = " ".join(text.split())
        return text


class ApprovalPeriod(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return str(self.date_from) + " : " + str(self.date_to)


class StatementGroup(models.Model):
    name = models.CharField(max_length=100)
    statements = models.ManyToManyField("StaticText")

    def __str__(self):
        return self.name


class OTP(models.Model):

    TYPE_CHOICES = (
        ('email', 'email'),
        ('mobile', 'mobile')
    )

    key = models.CharField(max_length=5)
    used = models.BooleanField(default=False)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, blank=False, null=True)
    email = models.EmailField(null=True, blank=True)


class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    TABS_CHOICES = (
        ('Profile', 'Profile'),
        ('Payment', 'Payment'),
    )

    ID_TYPE_CHOICES = (
        ('Aadhar', 'Aadhar'),
        ('Voter ID', 'Voter ID'),
        ('Driving Licence', 'Driving Licence')
    )


    USER_TYPES = (

        ('A','Applicant'),
        ('SA','Student Advisor'),
        ('EE','Education Expert'),
        ('CE','Career Expert'),
        ('FE','Foreign Expert'),

    )
    

    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))




    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, null=True)
    who_i_am = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, null=True)
    otp = models.ForeignKey("OTP", blank=True, null=True, on_delete=models.SET_NULL)
    mobile = models.CharField(max_length=20, null=True)
    house = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)  # validators=[MaxValueValidator(25)])
    district = models.CharField(max_length=100, null=True)  # validators=[MaxValueValidator(25)])
    state = models.CharField(max_length=100, null=True)  # validators=[MaxValueValidator(25)])
    country = models.CharField(max_length=100, null=True, default="India")
    pin = models.CharField(max_length=100, null=True)  # validators=[MaxValueValidator(6)])
    address = models.TextField(null=True)
    college = models.CharField(max_length=100, null=True)
    college_location = models.CharField(max_length=200, null=True, blank=True)
    school = models.CharField(max_length=100, null=True, blank=True)
    school_location = models.CharField(max_length=100, null=True, blank=True)
    school_qualification = models.CharField(max_length=100, null=True, blank=True)
    school_course = models.CharField(max_length=100, null=True, blank=True)
    class_12_year = models.CharField(max_length=100, null=True, blank=True)
    graduation_year = models.CharField(max_length=10, null=True, blank=True)
    terms_conditions = models.BooleanField(default=False)
    profile_image = models.ImageField(null=True, blank=True)
    tab_flag = models.CharField(max_length=80, choices=TABS_CHOICES, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=100)
    parent_email = models.EmailField(null=True, blank=False)

    
    
    user_type = models.CharField(max_length=15, choices=USER_TYPES,null=True,blank=True,default='A')

    #educational qualification fields

    # college1 = models.ForeignKey(College,blank=True,null=True,related_name="col1")
    # course1 = models.ForeignKey(Course,blank=True,null=True,related_name="course1")
    # qualification1 = models.ForeignKey(Qualification,blank=True,null=True,related_name="qual1")
    # year_of_passingout1 = models.CharField(max_length=4,choices=YEAR_CHOICES,null=True,blank=True)

    # college2 = models.ForeignKey(College,blank=True,null=True,related_name="col2")
    # course2 = models.ForeignKey(Course,blank=True,null=True,related_name="course2")
    # qualification2 = models.ForeignKey(Qualification,blank=True,null=True,related_name="qual2")
    # year_of_passingout2 = models.CharField(max_length=4,choices=YEAR_CHOICES,null=True,blank=True)

    # college3 = models.ForeignKey(College,blank=True,null=True,related_name="col3")
    # course3 = models.ForeignKey(Course,blank=True,null=True,related_name="course3")
    # qualification3 = models.ForeignKey(Qualification,blank=True,null=True,related_name="qual3")
    # year_of_passingout3 = models.CharField(max_length=4,choices=YEAR_CHOICES,null=True,blank=True)



    #hobbies

    my_interest = models.CharField(max_length=100,null=True,blank=True)
    what_i_do_well = models.CharField(max_length=100,null=True,blank=True)
    career_mission = models.CharField(max_length=100,null=True,blank=True)
    interesting_about_me = models.CharField(max_length=100,null=True,blank=True)
    my_extra_curri = models.CharField(max_length=100,null=True,blank=True)


    #users class 12th info, optional but necessary for expert profiles



    mobile_verified = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=True)

    def get_address(self):
        return self.address

    def __str__(self):
        return self.user.username







# college educational qualification of a Profile
class CollegeEduQual(models.Model):
    """docstring for CollegeEducationalQual"""

    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))



    college = models.ForeignKey(College,blank=True,null=True)
    course = models.ForeignKey(Course,blank=True,null=True)
    qualification = models.ForeignKey(Qualification,blank=True,null=True)
    year_of_passing_out = models.IntegerField(choices=YEAR_CHOICES,blank=True,null=True,max_length=4)
    profile = models.ForeignKey(Profile,null=False)


    def __str__(self):
        return profile.user.username









class Image(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    post = models.TextField()
    title = models.TextField()
    preview = models.TextField()
    author = models.CharField(max_length=100)
    date = models.DateField()
    publish = models.BooleanField(default=False)


class GAScore(models.Model):

    SCORE_TYPE = (
        ('Percentage', 'Percentage'),
        ('Percentile', 'Percentile'),
        ('Rank', 'Rank'),
        ('Score', 'Score')
    )

    college = models.ForeignKey("College", on_delete=models.SET_NULL, null=True)
    q_exam = models.ManyToManyField("QualifyingExam", null=True, blank=True)
    c_exam = models.ManyToManyField("CompetitiveExam", null=True, blank=True)
    l_cutoff = models.IntegerField()
    m_cutoff = models.IntegerField()
    h_cutoff = models.IntegerField()
    score_type = models.CharField(max_length=100, choices=SCORE_TYPE)

    def __str__(self):
        return self.college.name + ": " + str(self.college.id)


class EmailTemplate(models.Model):

    TYPE_CHOICES = (
        ('NEWUSER', 'NEWUSER'),
        ('FORGOTPASSWORD', 'FORGOTPASSWORD'),
        ('PURCHASEDSCHL', 'PURCHASEDSCHL'),
        ('COLLEGE_EMAIL', 'COLLEGE_EMAIL'),
        ('OTP', 'OTP'),
        ('INVOICE', 'INVOICE'),
        ('FORGOTPASSWORD', 'FORGOTPASSWORD'),
        ('PARENTEMAIL', 'PARENTEMAIL'),
    )
    html = models.TextField()
    subject = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    def __str__(self):
        return self.subject


class Configuration(models.Model):
    last_c_code = models.IntegerField(default=0)
    post_mark_key = models.CharField(default="400be863-1b90-4a8d-84e5-9be9a2d9b455", max_length=100)
    from_email = models.CharField(default="no-reply@justrokket.com", max_length=100)
    twillio_account_sid = models.CharField(null=True, max_length=100)
    twillio_key = models.CharField(max_length=100, null=True)
    twillio_from_number = models.CharField(max_length=100, null=True)
    admin_contact_email = models.EmailField(null=True, blank=True)
    jr_fee_1 = models.IntegerField(null=True, blank=True)
    jr_fee_2 = models.IntegerField(null=True, blank=True)
    jr_fee_3 = models.IntegerField(null=True, blank=True)

# class Month(models.Model):
#     month_count = models.IntegerField(verbose_name="Month Number", null=True, blank=False)
#     price_for_this_month = models.IntegerField(verbose_name="Price for this Month", null=True, blank=False)

#     def __unicode__(self):
#         return """ Month Count: %s Price for this month: %s """ % (str(self.month_count), str(self.price_for_this_month))


class Order(models.Model):

    ORDER_STATUS = (
        ('1', 'Unprocessed'),
        ('2', 'Processed'),
        ('3', 'Cancelled'),
    )
    order_number = models.CharField(max_length=80, null=True, blank=False)
    profile = models.ForeignKey(Profile, null=True, blank=False, on_delete=models.SET_NULL)
    selection = models.ForeignKey(Selection, null=True, blank=False, related_name="selection", on_delete=models.SET_NULL)
    status = models.IntegerField(null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True, auto_now=True)
    amount = models.IntegerField(null=True, blank=True)
    prn = models.IntegerField(null=True, blank=False)
    bid = models.IntegerField(null=True, blank=False)
    pid = models.IntegerField(null=True, blank=False)
    tnc = models.BooleanField(default=False)
    notInCollege = models.BooleanField(default=False)

    refund_requested = models.BooleanField(default=False)
    refund_requested_on = models.DateTimeField(null=True)
    refund_processed = models.BooleanField(default=False)
    refund_due_date = models.DateTimeField(null=True)
    refund_reason = models.TextField(null=True, blank=True)
    refund_approved_by = models.TextField(null=True, blank=True)
    refund_approved_on = models.DateTimeField(null=True, blank=True)
    student_accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.order_number


class ContactUsMessages(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    phone = models.TextField(verbose_name="Mobile Phone")
    email = models.EmailField()
    message = models.TextField()


class Newsletter(models.Model):
    email = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.email



class QuestionExpert(models.Model):
    question = models.ForeignKey(Question)
    assigned_to = models.ForeignKey(Profile)
    answered = models.BooleanField(default=False)
    def __str__(self):
        return self.question.title+'-'+self.assigned_to.user.username


class ForeignStudy(models.Model):
    name = models.CharField(max_length=40)
     
    def __str__(self):
        return self.name





def create_tag(sender, instance,created, **kwargs):
    
    if created:

        tag_name = instance.name
        tag_name = tag_name.replace(" ","").lower()
        tag.objects.create(name=tag_name,content_type=ContentType.objects.get_for_model(sender),object_id=instance.pk)

#foreign study tag
def create_tag_fs(sender, instance,created, **kwargs):
    
    if created:

        tag_name = instance.name
        tag_name = "studyin"+tag_name.replace(" ","").lower()
        tag.objects.create(name=tag_name,content_type=ContentType.objects.get_for_model(sender),object_id=instance.pk)


post_save.connect(create_tag, sender=College)
post_save.connect(create_tag, sender=Course)
post_save.connect(create_tag, sender=QualifyingExam)
post_save.connect(create_tag, sender=CompetitiveExam)

post_save.connect(create_tag_fs, sender = ForeignStudy)

# create tag for qualification model instance just after its created
def create_tag_qualification(sender, instance, created,**kwargs):

    print("hi")
    print(created)
    if created:

        tag_name = instance.qualification
        tag_name = tag_name.replace(" ","").lower()
        tag.objects.create(name=tag_name,content_type=ContentType.objects.get_for_model(sender),object_id=instance.pk)




post_save.connect(create_tag_qualification, sender=Qualification)




# from django.dispatch import receiver

def update_assigned_to(sender, instance, created, **kwargs):



    college_contenttype = ContentType.objects.get(model='college')
    qualification_contenttype = ContentType.objects.get(model='qualification')
    course_contenttype = ContentType.objects.get(model='course')



    qe_contenttype = ContentType.objects.get(model='qualifyingexam')
    ce_contenttype = ContentType.objects.get(model='competitiveexam')

    # country_contenttype = ContentType.objects.get(model='course')

    if instance.tag.content_type==college_contenttype:
        college = College.objects.get(id=instance.tag.object_id)
        #send this question only to students of this college
        sa_relevant_profiles = Profile.objects.filter(collegeeduqual__college=college).filter(user_type='SA')
        for expert in sa_relevant_profiles:
            QuestionExpert.objects.create(question=instance,assigned_to=expert)

    if instance.tag.content_type==qualification_contenttype:
        list = ['CE']
        qualification = Qualification.objects.get(id=instance.tag.object_id)
        sa_relevant_profiles = Profile.objects.filter(collegeeduqual__qualification=qualification).filter(user_type='SA')
        for expert in sa_relevant_profiles:
            QuestionExpert.objects.create(question=instance,assigned_to=expert)
        assign_and_mail_experts(list,instance)


    if instance.tag.content_type==course_contenttype:

        # user
        # instance.assigned_to=
        list = ['CE','EE']
        course = Course.objects.get(id=instance.tag.object_id)
        sa_relevant_profiles = Profile.objects.filter(collegeeduqual__course=course).filter(user_type='SA')
        for expert in sa_relevant_profiles:
            QuestionExpert.objects.create(question=instance,assigned_to=expert)
        assign_and_mail_experts(list,instance)

    if instance.tag.content_type==qe_contenttype:
        list = ['EE']
        assign_and_mail_experts(list,instance)

    if instance.tag.content_type==ce_contenttype:
        list = ['EE']
        assign_and_mail_experts(list,instance)




def assign_and_mail_experts(myList,instance):
    print("hi")
    print(Profile.objects.filter(user_type__in=myList))
    expert_profile_list = Profile.objects.filter(user_type__in=myList)




    for expert in expert_profile_list:
        QuestionExpert.objects.create(question=instance,assigned_to=expert)
        # send_mail(subject="hi",message="this is a message", recipient_list=[expert.parent_email])








post_save.connect(update_assigned_to, sender=Question)


#whenever answer is posted by an expert, update questionexpert for that question by setting answered to true 

def update_questionexpert(sender, instance, **kwargs):
    profile = instance.user
    question = instance.question
    relevant_qe_rows = QuestionExpert.objects.filter(assigned_to=profile).filter(question=question)
    
    


    
    for qe in relevant_qe_rows:
        qe.answered = True
        qe.save()

#test comment
    

post_save.connect(update_questionexpert, sender=Answer)



