from uuid import uuid4
def Upload(instance, filename, **kwargs):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    file_path = 'org/{instance_name}/uploads/{uid}/{filename}'.format(
            instance_name=str(instance._meta.model_name),uid= str(instance.id),filename=filename
        )
    return file_path