from django.db import models
from django.db.models.manager import EmptyManager
from mptt.models import MPTTModel, TreeForeignKey


class ContentType(models.Model):
	app_label = models.CharField(max_length=100)
	model = models.CharField(max_length=100)

	class Meta:
		managed = False
		db_table = 'django_content_type'
		unique_together = (('app_label', 'model'),)

	def __str__(self):
			return str(self.model)

class AppMenu(MPTTModel):
	id = models.BigAutoField(primary_key=True)
	created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
	updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
	content_type = models.OneToOneField(ContentType, null=True, blank=True,verbose_name="Content Type", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
	name = models.CharField(max_length=100)
	icon = models.CharField(max_length=100,null=True,default="far fa-file-alt opacity-4 d-block text-150 my-15")
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=EmptyManager)
	lft = models.IntegerField(default=0, blank=True, null=True, editable=False)
	rght = models.IntegerField(default=0, blank=True, null=True, editable=False)
	tree_id = models.IntegerField(default=0, blank=True, null=True, editable=False)
	mptt_level = models.IntegerField(default=0, blank=True, null=True, editable=False)

	I_type = (
		("app_label", "App_Label"),
		("model", "Model"),
	)
	type = models.CharField(max_length=20, choices=I_type, blank=False, null=False)

	@property
	def menu_order(self):
		if self.parent is not None:
			return int(self.parent_id)+self.mptt_level+self.lft+self.tree_id
		else:
			return self.mptt_level+self.lft+self.tree_id


	class MPTTMeta:
		order_insertion_by = ['mptt_level']
		level_attr = 'mptt_level'

	class Meta:
		ordering = ['mptt_level']
		unique_together = ('name','parent','content_type')
		verbose_name = 'App Menu'
		verbose_name_plural = 'App Menu'
		db_table = 'core_app_menu'


	def __str__(self):
		return str(self.type).title() +" "+str(self.name).title()