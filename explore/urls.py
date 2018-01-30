from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from main.views import TemplateView
from django.views.generic.base import RedirectView
admin.site.site_header = "JustRokket Admin"
from main import views
from . import settings


urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomeViewNew.as_view(), name='home'),
    url(r'^admissions/$', views.HomeView.as_view(), name='home'),
    url(r'^community-page/$', views.admissions1.as_view(), name='home'),
    url(r'^explore-post/$', views.ExplorePost.as_view(), name='explore-post'),
    url(r'^profile/(?P<pk>\d+)', views.UpdateProfile.as_view(), name='profile'),
    url(r'^selected-college/(?P<pk>\d+)/$', views.Screen3.as_view(), name='selected-college'),
    url(r'^selection/$', views.Selection.as_view(), name='selected'),
    url(r'^finalize/(?P<pk>\d+)$', views.profile_view, name='finalized'),
    url(r'^explore/(?P<id>\d+)$', views.Explore.as_view(), name='explore'),
    url(r'^v/(?P<email>.*)', views.VerifyEmail.as_view(), name='v'),
    url(r'^vm/(?P<mobile>.*)', views.VerifyMobile.as_view(), name='vm'),
    url(r'^otp/(?P<otp>.*)/(?P<type>.*)', views.VerifyOTP.as_view(), name='otp'),
    url(r'^thank-you/(?P<pk>.*)', views.Screen6.as_view(), name='thank-you'),
    url(r'^refund/(?P<pk>.*)', views.RequestRefund.as_view(), name='refund-you'),
    # url(r'^blog/$', views.BlogView.as_view(), name='blog'),
    # url(r'^blog-details', views.BlogdetailsView.as_view(), name='blog-details'),
    url(r'^user-login', views.LoginUser.as_view(), name='login-user'),
    # url(r'^userlogin', views.UserLogin.as_view(), name='user-login'),
    url(r'^update-profile/(?P<pk>\d+)/', views.UpdateProfile.as_view(), name='update-profile'),
    url(r'^create-profile/', views.CreateProfile.as_view(), name='create-profile'),
    url(r'^populate/course/categories/', views.populate_course_categories, name='populate-course-categories'),
    url(r'^populate/qualification/exam/', views.populate_qualification_exam,
        name='populate-qualification-exam'),
    url(r'^populate/competitve/exam/', views.populate_competitve_exam,
        name='populate-competitve-exam'),
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    url(r'^about-us/', views.AboutView.as_view(), name='about-us'),
    url(r'^contact-us/', views.ContactView.as_view(), name='contact-us'),
    url(r'^partner-institutions/', views.PartnersView.as_view(), name='partners'),
    url(r'^faq/', views.FaqView.as_view(), name='faq'),
    url(r'^privacy-policy/', views.PrivacyView.as_view(), name='privacy'),
    url(r'^tnc/', views.TermsView.as_view(), name='terms-of-use'),
    url(r'^refund-policy/', views.RefundAssuranceView.as_view(), name='refund-assurance'),
    url(r'^why-students-can-depend-on-us/', views.WhyDependView.as_view(), name='why-you-can-depend-on-us'),
    url(r'^how-just-rokket-helps-partner-institutions/', views.WorkView.as_view(), name='how-just-rokket-helps-you'),
    url(r'^how-this-works/', views.HowView.as_view(), name='how-this-works'),
    url(r'^pricing/', views.PricingView.as_view(), name='pricing'),
    url(r'^forgot-password/$', views.ForgotPassword.as_view(), name='forgot-password'),
    url(r'^forgot-password/verify-otp/(?P<otp>.*)$', views.ForgotPasswordVerifyOTP.as_view(), name='forgot-password'),
    url(r'^forgot-password/new-password/(?P<otp>.*)', views.ForgotPasswordNewPassword.as_view(), name='forgot-password'),
    url(r'^reset-password-profile-page', views.ResetPasswordProfilePage.as_view(), name='forgot-password'),
    url(r'^contact-form', views.ContactForm.as_view(), name='contact-form'),
    # payment
    url(r'^how-just-rokket-helps-you/', views.WorkView.as_view(), name='how-just-rokket-helps-you'),
    # url(r'^payment/(?P<pk>\d+)/', views.payment_processor, name='payment-processor'),
    url(r'^payment/redirect/', views.redirectview, name='how-this-works'),
    url(r'^payment/cancel/', views.cancelview, name='cancel'),
    url(r'^accounts/facebook/login/callback/(?P<token>.*)', views.LoginUser.as_view(), name='login-user'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^newsletter/$', views.Newsletter.as_view(), name='newsletter'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    url(r'^apple-touch-icon\.png$', RedirectView.as_view(url="/static/images/apple-touch-icon.png", permanent=False)),
    url(r'^favicon-32x32\.png$', RedirectView.as_view(url="/static/images/favicon-32x32.png", permanent=False)),
    url(r'^favicon-16x16\.png$', RedirectView.as_view(url="/static/favicon-16x16.png", permanent=False)),
    url(r'^favicon\.ico$', RedirectView.as_view(url="/static/favicon.ico", permanent=False)),
    url(r'^manifest\.json$', RedirectView.as_view(url="/static/manifest.json", permanent=False)),
    url(r'^safari-pinned-tab\.svg$', RedirectView.as_view(url="/static/safari-pinned-tab.svg", permanent=False)),
    url(r'^featured-image\.jpg$', RedirectView.as_view(url="/static/images/featured.jpg")),
    # url(r'^community/', include('qa.urls')),
    url(r'^question-listing/', include('qa.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
