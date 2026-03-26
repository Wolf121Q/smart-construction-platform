from django.db import models
from core.models import UserType

class CommentableUserType(models.Model):
	id = models.BigAutoField(primary_key=True)
	created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
	updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
	created_by = models.ForeignKey('User', null=True, blank=True,verbose_name="Created By", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
	updated_by = models.ForeignKey('User', null=True, blank=True,verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
	ip = models.GenericIPAddressField(verbose_name="Ip Address", null=True, blank=True)
	user_types = models.ManyToManyField('UserType',blank=False,verbose_name="User Types",related_name="ut_%(app_label)s_%(class)s_related",related_query_name="ut_%(app_label)s_%(class)ss")

	class Meta:
		verbose_name = 'Allowed To Comment User'
		verbose_name_plural = 'Allowed To Comment Users'
		db_table = 'core_commentable_user_type'

	def __str__(self):
		user_types = ", ".join([str(user_type) for user_type in self.user_types.all()])
		return f"Allowed Users: ({user_types})"