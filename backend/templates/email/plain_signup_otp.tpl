{% extends "mail_templated/base.tpl" %}

{% block subject %}
DHAI-R Member Portal OTP
{% endblock %}
{% block body %}
Dear {{user.full_name}},
Welcome to DHAI-R member portal, 
Your OTP  is: {{otp}}
For security reasons, this code will expire in 2 minutes.Warning! Do not share your PIN with anyone, if you do not requested PIN, please contact at our helpline."
{% endblock %}


