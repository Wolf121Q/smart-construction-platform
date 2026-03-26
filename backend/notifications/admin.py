''' Django notifications admin file '''
# -*- coding: utf-8 -*-
from django.contrib import admin
from notifications.base.admin import AbstractNotificationAdmin
from swapper import load_model

Notification = load_model('notifications', 'Notification')


class NotificationAdmin(AbstractNotificationAdmin):
    raw_id_fields = ('recipient',)
    list_display = ('recipient', 'actor',
                    'level', 'target', 'unread', 'public')
    list_filter = ('level', 'unread', 'public', 'timestamp',)

    def get_queryset(self, request):
        qs = super(NotificationAdmin, self).get_queryset(request)
        return qs.prefetch_related('actor')
    
    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
        if request.user.is_superuser == 0:
            return False
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return True
        else:
            return False

admin.site.register(Notification, NotificationAdmin)
