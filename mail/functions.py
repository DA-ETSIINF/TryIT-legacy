from django.core.mail import EmailMessage


def mail(title, body, attachment):
    # this is not finished
    email = EmailMessage(body)

    email.attach(attachment)
    email.send()
