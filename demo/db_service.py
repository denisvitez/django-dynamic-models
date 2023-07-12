from django.contrib import admin
from django.db import connection, models

from demo.models import DynamicTable, DynamicTableColumn


def create_test_model():
    with connection.schema_editor() as schema_editor:
        fields = {
            'first_name': models.CharField(max_length=255),
            'last_name': models.CharField(max_length=255),
            '__str__': lambda self: '%s %s' % (self.first_name, self.last_name),
        }
        dynamic_model = create_dynamic_model('DynamicModel', fields, 'dynamic')
        schema_editor.create_model(dynamic_model)


def create_model(model_data):
    new_model = DynamicTable(name=model_data.get('name'))
    new_model.save()
    columns = model_data.get('columns')
    fields = {}
    for c in columns:
        new_column = DynamicTableColumn(name=c.get('name'), type=c.get('type'), table=new_model)
        new_column.save()
        model_type = models.CharField(max_length=255)
        if c.get('type') == 'INTEGER':
            model_type = models.IntegerField()
        elif c.get('type') == 'BOOLEAN':
            model_type = models.BooleanField()
        fields[c.get('name')] = model_type
    print(new_model.dynamictablecolumn_set.all())
    # create dynamic model
    dynamic_model = create_dynamic_model(model_data.get('name'), fields, 'dynamic')
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(dynamic_model)


def delete_test_model():
    with connection.schema_editor() as schema_editor:
        fields = {}
        dynamic_model = create_dynamic_model('DynamicModel', fields, 'dynamic')
        schema_editor.delete_model(dynamic_model)


def delete_model(pk):
    # Delete table record
    existing_model = DynamicTable.objects.get(pk=pk)
    existing_model.delete()


# Code copied from: https://code.djangoproject.com/wiki/DynamicModels
def create_dynamic_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
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
