from django.db import models
from django.db.models.manager import EmptyManager
from mptt.models import MPTTModel, TreeForeignKey
from colorfield.fields import ColorField

class SystemType(MPTTModel):
	id = models.BigAutoField(primary_key=True)
	created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
	updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
	created_by = models.ForeignKey('User', null=True, blank=True,verbose_name="Created By", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
	updated_by = models.ForeignKey('User', null=True, blank=True,verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
	ip = models.GenericIPAddressField(verbose_name="Ip Address", null=True, blank=True)
	color = ColorField(default='#FF0000')
	name = models.CharField(max_length=100, unique=False)
	code = models.CharField(max_length=100, unique=False)
	system_code = models.CharField(max_length=100, unique=True)

	desg_level = TreeForeignKey('self', null=True, blank=True, related_name='des_level_children', db_index=True,on_delete=EmptyManager)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=models.SET_NULL)
	lft = models.IntegerField(default=0, blank=True, null=True, editable=False)
	rght = models.IntegerField(default=0, blank=True, null=True, editable=False)
	tree_id = models.IntegerField(default=0, blank=True, null=True, editable=False)
	mptt_level = models.IntegerField(default=0, blank=True, null=True, editable=False)

	I_STATUS = (
		("active", "Active"),
		("inactive", "Inactive"),
	)
	status = models.CharField(default='active',max_length=20, choices=I_STATUS, blank=False, null=False)

	class MPTTMeta:
		order_insertion_by = ['mptt_level']
		level_attr = 'mptt_level'

	class Meta:
		ordering = ['mptt_level']
		unique_together = ('parent','system_code')
		verbose_name = 'System Type'
		verbose_name_plural = 'System Types'
		db_table = 'core_types'

	def getNameTree(self):
		try:
			name = self.name
			k = self.parent
			while k is not None:
				name = k.name+" / "+name
				k = k.parent
			return name
		except:
			return ""

	def getCodeTree(self):
		try:
			code = self.code
			k = self.parent
			while k is not None:
				code = k.code+"-"+code
				k = k.parent
			return code
		except:
			return ""


	def __str__(self):
		return str(self.name)