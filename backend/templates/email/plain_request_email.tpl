{% extends "mail_templated/base.tpl" %}
{% block subject %}
Request {{method}}: {{ip}},{{full_path}}
{% endblock %}
{% block body %}

url : {{url}} method : {{method}}

{% if headers %}
headers : {{ headers }}
{% endif %}

{% if body %}
body : {{ body }}


{% endif %}

{{request_body}}

user name: {{user.full_name}},
username: {{user.username}},
Type: {{user.type}}
email: {{user.email}}

ip: {{ip}}
Time: {{current_datetime}}
path : {{full_path}}

error: {{trace_back}}

{% endblock %}
