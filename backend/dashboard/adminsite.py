from django.contrib.admin import AdminSite
from django.shortcuts import redirect
from datetime import datetime, timedelta,date
from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from django.utils.text import capfirst
from django.apps import apps
from django.utils.safestring import mark_safe
from django.contrib import messages
from core.models import AppMenu
from django.contrib.contenttypes.models import ContentType


def getAppinstance(app_label):
    app_label =str(app_label).lower().strip().replace(" ","")
    app = AppMenu.objects.filter(name=app_label,type="app_label").first()
    if app is None:
        app = AppMenu()
        app.name = app_label
        app.type = "app_label"
        app.save()
    return app

class AppAdminSite(AdminSite):
    # site_title = _('Hello World')
    # index_template = 'dashboard/dashboard.html';

    def index(self, request, extra_context=None):
        #messages.info(request,mark_safe(request.user.type.system_code))
        if not request.user.is_superuser :
           return redirect("/dashboard/projectdirectorhousing/")
        
        if extra_context is None:
            extra_context = {}

        return super().index(request, extra_context)
    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label
            #messages.info(request, mark_safe(model._meta.get_field_value('id')))

            app_instance = getAppinstance(app_label)
            content_type = ContentType.objects.get_for_model(model,for_concrete_model=False)
            if content_type is None:
                content_type = ContentType.objects.get_for_model(model)

            model_info = AppMenu.objects.filter(content_type_id=content_type.id, type="model").first()
            #messages.info(request, mark_safe(model))
            if model_info is None:
                model_info = AppMenu()
                model_info.parent = app_instance
                model_info.content_type_id = content_type.id
                model_info.name = str(content_type.model).lower()
                model_info.type = "model"
                model_info.save()

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue
            #ixd = ixd-1
            info = (app_label, model._meta.model_name)
            # model_ct = CT.objects.get_for_model(model)
            # model_info = AppMenu.objects.filter(content_type_id=model_ct.id, type="model").first()
            #messages.info(request,mark_safe(model_ct))
            model_dict = {
                'model': model,
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'perms': perms,
                'admin_url': None,
                'icon': model_info.icon+" "+model_info.name,
                #'icon': '',
                'admin_model_order': model_info.menu_order,
                #'admin_model_order': 1,
                'add_url': None,
            }
            if perms.get('change') or perms.get('view'):
                model_dict['view_only'] = not perms.get('change')
                try:
                    model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                #messages.info(request, mark_safe("already"))
                app_dict[app_label]['models'].append(model_dict)
                app_dict[app_label]['admin_model_order']= app_instance.menu_order
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'admin_model_order': app_instance.menu_order,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                }

        if label:
            return app_dict.get(label)
        return app_dict


