from django import template
from qa.models import BlogContent
register = template.Library()

@register.filter
def get_blog_content(blogcontent,index):
    i=(index-1)//2
    s=""
    TagList=""
    try:
        b=BlogContent.objects.get(id=blogcontent[i]["id"])
        for t in b.tag.all():
            TagList+="# "+str(t)+" | "
    except:
        print("Some Issue");
    try:
        if(blogcontent and len(blogcontent)>0):
            s+="<div class='qa__q-card nqa'><h4>"+blogcontent[i]["title"]+"</h4><p>"+blogcontent[i]["body_content"]+"</p><a href='"+str(blogcontent[i]["url"])+"'>"+str(blogcontent[i]["url"])+"</a><div class='tag'>"+TagList[:-2]+"</div></div>"
    except:
        s="";
    return s

@register.filter
def get_blog_content_remaining(blogcontent,index):
    i=(index-2)//2
    s=""
    try:
        for x in range(i,len(blogcontent),1):
            TagList=""
            try:
                b=BlogContent.objects.get(id=blogcontent[i]["id"])
                for t in b.tag.all():
                    TagList+="# "+str(t)+" | "
            except:
                print("Some Issue");
                
            s+="<div class='qa__q-card nqa'><h4>"+blogcontent[i]["title"]+"</h4><p>"+blogcontent[i]["body_content"]+"</p><a href='"+str(blogcontent[i]["url"])+"'>"+str(blogcontent[i]["url"])+"</a><div class='tag'>"+TagList[:-2]+"</div></div>"
    except:
        s+=""
    return s