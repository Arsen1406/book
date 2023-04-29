from book import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


def generation_confirm_code(user):
    them = 'Ваш код подтверждения'
    confirmation_code = default_token_generator.make_token(user)
    text = f'Ваш код подтверждения: {confirmation_code}'
    email_from = settings.EMAIL_BACKEND
    send_mail(them, text, email_from, [user.email])
