import project.models
allmodels = dict([(name.lower(), cls) for name, cls in project.models.__dict__.items() if isinstance(cls, type)])
...
class MyDBRouter(object):

    def db_for_read(self, model, **hints):
        if not hasattr(model, 'params'):
            return None
        """ reading model based on params """
        return getattr(model.params, 'db')

    def db_for_write(self, model, **hints):
        if not hasattr(model, 'params'):
            return None
        """ writing model based on params """
        return getattr(model.params, 'db')

    def allow_migrate(self, db, app_label, model_name = None, **hints):
        """ migrate to appropriate database per model """
        model = allmodels.get(model_name)
        if not hasattr(model, 'params'):
            return None
        return(model.params.db == db)