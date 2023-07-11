from django.contrib import admin
from django.db import connection, models


def create_test_model():
    with connection.schema_editor() as schema_editor:
        fields = {
            'first_name': models.CharField(max_length=255),
            'last_name': models.CharField(max_length=255),
            '__str__': lambda self: '%s %s'(self.first_name, self.last_name),
        }
        dynamic_model = create_model('DynamicModel', fields, 'dynamic')
        schema_editor.create_model(dynamic_model)


def delete_test_model():
    with connection.schema_editor() as schema_editor:
        fields = {
            'first_name': models.CharField(max_length=255),
            'last_name': models.CharField(max_length=255),
            '__str__': lambda self: '%s %s'(self.first_name, self.last_name),
        }
        dynamic_model = create_model('DynamicModel', fields, 'dynamic')
        schema_editor.delete_model(dynamic_model)


# Code copied from: https://code.djangoproject.com/wiki/DynamicModels
def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in iter(options.items()):
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)
    return model
