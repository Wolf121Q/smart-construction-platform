{% extends "mail_templated/base.tpl" %}

{% block subject %}
Email Debugger {{current_datetime}}, {{tag}}
{% endblock %}
{% block body %}
{{raw_data}}
{% endblock %}