from django import template
from django.conf import settings
from postmarker.core import PostmarkClient


SCREEN_6_TEXT = "The institution will grant provisional admission till the minimum eligibility proof of the qualifying exam is not submitted. The qualifying exam results need to be submitted within 7 days of their declaration as otherwise the admitting institution may cancel the admission offer"


def send_mail(subject, message, recipient_list, from_email=None, attachments=[]):
    #c = main.models.Configuration.objects.first()  # lazy-load
    # postmark = PostmarkClient(server_token=c.post_mark_key)
    postmark = PostmarkClient(token='400be863-1b90-4a8d-84e5-9be9a2d9b455')

    if not from_email:
        # from_email = c.from_email
        from_email='7cc645e5518c4130a4cbe3ae77ae588e@inbound.postmarkapp.com'
    print("Sending Email to ", recipient_list)
    sent_email = postmark.emails.send_batch(
        *[{
            'To': recipient,
            'From': from_email,
            'Subject': subject,
            'HtmlBody': message,
            'Attachments': attachments
        } for recipient in recipient_list]
    )
    print(sent_email)
    return sent_email