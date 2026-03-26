from django.db import models
from core.models import SuperUser
from django.db.models.manager import EmptyManager
from mptt.models import MPTTModel, TreeForeignKey

class RequestSource(MPTTModel):
	id = models.BigAutoField(primary_key=True)
	created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
	updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
	created_by = models.ForeignKey(SuperUser, null=True, blank=True,verbose_name="Created By", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
	updated_by = models.ForeignKey(SuperUser, null=True, blank=True,verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
	ip = models.GenericIPAddressField(verbose_name="Ip Address", null=True, blank=True)
	name = models.CharField(max_length=50, unique=True)
	code = models.CharField(max_length=50, unique=True)
	description = models.TextField(null=True,blank=True)

	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=EmptyManager)
	lft = models.IntegerField(default=0, blank=True, null=True, editable=False)
	rght = models.IntegerField(default=0, blank=True, null=True, editable=False)
	tree_id = models.IntegerField(default=0, blank=True, null=True, editable=False)
	mptt_level = models.IntegerField(default=0, blank=True, null=True, editable=False)

	I_STATUS = (
		("active", "Active"),
		("inactive", "Inactive"),
	)
	status = models.CharField(max_length=20, choices=I_STATUS, blank=False, null=False)

	class MPTTMeta:
		order_insertion_by = ['mptt_level']
		level_attr = 'mptt_level'

	class Meta:
		ordering = ['mptt_level']
		unique_together = ('parent','name', 'code')
		verbose_name = 'Request Source'
		verbose_name_plural = 'Request Sources'
		db_table = 'hs_request_sources'

	def get_slug_list(self):
		try:
			ancestors = self.get_ancestors(include_self=True)
		except:
			ancestors = []
		else:
			ancestors = [ i.slug for i in ancestors]
		slugs = []
		for i in range(len(ancestors)):
			slugs.append('/'.join(ancestors[:i+1]))
		return slugs

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
		return str(self.code)+"-"+str(self.name)