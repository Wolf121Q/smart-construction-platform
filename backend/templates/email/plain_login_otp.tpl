{% extends "mail_templated/base.tpl" %}

{% block subject %}
DHAI-R Member Portal Login OTP
{% endblock %}
{% block body %}
Dear {{user.full_name}},
You have  received instructions to enter a one-time pin (OTP) code in order to log into your DHAI-R member portal account. Your OTP is: {{otp}}
For security reasons, this code will expire in 2 minutes.
If you did not request this code, you should change or reset your password or call at DHAI-R member portal helpline immediately.
{% endblock %}


