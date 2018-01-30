
from django.db.models.signals import post_save,m2m_changed
from .models import Question
from main.models import Profile

# from django.dispatch import receiver

def update_assigned_to(sender,instance,**kwargs):
    

    print("hellooooooooooooosssssss")


    college_contenttype = ContentType.objects.get(model='college')
    qualification_contenttype = ContentType.objects.get(model='qualification')
    course_contenttype = ContentType.objects.get(model='course')
    

    for c in ContentType.objects.all(): 
        print(c.model)


    qe_contenttype = ContentType.objects.get(model='qualifyingexam')
    ce_contenttype = ContentType.objects.get(model='competitiveexam')

    # country_contenttype = ContentType.objects.get(model='course')








    if instance.tag.content_type==course_contenttype:

        # user
        # instance.assigned_to=
        list = ['SE','CE','EE']
        print(Profile.objects.filter(user_type__in=list))
        expert_profile_list = Profile.objects.filter(user_type__in=list)
        
        print(created)
        if created:        
            transaction.on_commit(
                instance.assigned_to.set(expert_profile_list)
            )    



post_save.connect(update_assigned_to, sender=Question)
