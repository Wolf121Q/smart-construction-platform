{% extends "mail_templated/base.tpl" %}

{% block subject %}
{{notification.verb}}
{% endblock %}
{% block body %}
Dear {{notification.recipient.full_name}},
{{notification.description}}
{% endblock %}