{% extends "mail_templated/base.tpl" %}

{% block subject %}
Your Email OTP for DHAi-R
{% endblock %}
{% block body %}
Dear {{user.full_name}},
Your verification code is {{otp}} for DHAI-R member portal
{% endblock %}