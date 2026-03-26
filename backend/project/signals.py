from django.db.models.signals import post_save
from django.dispatch import receiver
from project.models import TaskAction

@receiver(post_save,sender=TaskAction)
def generate_beep_on_red_flag(sender,instance,created,**kwargs):
    if created:
        print('\a')
        print("RED FLAG")
        pass

