from django.db import models
from core.models import SystemType

class UserTypeHierarchy(models.Model):
	id = models.BigAutoField(primary_key=True)
	created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
	updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
	created_by = models.ForeignKey('User', null=True, blank=True,verbose_name="Created By", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
	updated_by = models.ForeignKey('User', null=True, blank=True,verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
	ip = models.GenericIPAddressField(verbose_name="Ip Address", null=True, blank=True)
	user_type = models.ForeignKey(SystemType, null=False, blank=False,verbose_name="User Type", on_delete=models.CASCADE,related_name="ut_%(app_label)s_%(class)s_related",related_query_name="ut_%(app_label)s_%(class)ss")
	group_user_types = models.ManyToManyField(SystemType,blank=True,related_name="gut_%(app_label)s_%(class)s_related",related_query_name="gut_%(app_label)s_%(class)ss")
	
	I_STATUS = (
		("active", "Active"),
		("inactive", "Inactive"),
	)
	status = models.CharField(default='active', max_length=20, choices=I_STATUS, blank=False, null=False)

	class Meta:
		# unique_together = ('parent','system_code')
		verbose_name = 'Hierarchy'
		verbose_name_plural = 'Hierarchy'
		db_table = 'core_user_type_hierarchy'

	# def __str__(self):
	# 	if self.parent:
	# 		return "{name} - {parent}".format(name = self.name, parent = self.parent.name)
	# 	else:
	# 		return str(self.name)