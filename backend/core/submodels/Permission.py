from django.db import models

class Permission(models.Model):
    id = models.BigAutoField(primary_key=True)
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)
    class Meta:
       managed = False
       db_table = 'auth_permission'

    def __str__(self):
        return str(self.id)+" - "+str(self.name)