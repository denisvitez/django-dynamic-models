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


def update_model(pk, model_data):
    with connection.schema_editor() as schema_editor:
        existing_model = DynamicTable.objects.get(pk=pk)
        old_columns = existing_model.dynamictablecolumn_set.all()
        old_fields = get_fields_for_columns(old_columns)
        old_dynamic_model = create_dynamic_model(existing_model.name, old_fields, 'dynamic')
        has_name_changed = existing_model.name != model_data.get('name')
        if has_name_changed:
            # rename the table
            old_name = existing_model.name
            existing_model.name = model_data.get('name')
            dynamic_model = create_dynamic_model(old_name, {}, 'dynamic')
            schema_editor.alter_db_table(dynamic_model, f"dynamic_{old_name}", f"dynamic_{existing_model.name}")
            existing_model.save()
        # delete all column rows and insert new ones
        DynamicTableColumn.objects.filter(table=existing_model).delete()
        columns = model_data.get('columns')
        for c in columns:
            new_column = DynamicTableColumn(name=c.get('name'), type=c.get('type'), table=existing_model)
            new_column.save()
        # update dynamic table structure
        new_columns = existing_model.dynamictablecolumn_set.all()
        new_fields = get_fields_for_columns(new_columns)
        new_dynamic_model = create_dynamic_model(existing_model.name, new_fields, 'dynamic')
        print(old_dynamic_model._meta.get_fields())
        print(new_dynamic_model._meta.get_fields())
        # if field is in old model, but not in new model, it must be deleted
        for old_field in old_dynamic_model._meta.get_fields():
            still_exists = False
            for new_field in new_dynamic_model._meta.get_fields():
                if old_field.attname == new_field.attname:
                    still_exists = True
                    break
            if not still_exists:
                schema_editor.remove_field(old_dynamic_model, old_field)
        # if field is in the new model but not in the new model, it must be added
        for new_field in new_dynamic_model._meta.get_fields():
            existed_before = False
            for old_field in old_dynamic_model._meta.get_fields():
                if old_field.attname == new_field.attname:
                    existed_before = True
            if not existed_before:
                new_field.null = True
                schema_editor.add_field(new_dynamic_model, new_field)


def delete_test_model():
    with connection.schema_editor() as schema_editor:
        fields = {}
        dynamic_model = create_dynamic_model('DynamicModel', fields, 'dynamic')
        schema_editor.delete_model(dynamic_model)


def delete_model(pk):
    # Delete table record
    existing_model = DynamicTable.objects.get(pk=pk)
    dynamic_model = create_dynamic_model(existing_model.name, {}, 'dynamic')
    existing_model.delete()
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(dynamic_model)


def get_rows(pk):
    existing_model = DynamicTable.objects.get(pk=pk)
    model_columns = existing_model.dynamictablecolumn_set.all()
    fields = get_fields_for_columns(model_columns)
    dynamic_model = create_dynamic_model(existing_model.name, fields, 'dynamic')
    result = []
    for dm in dynamic_model.objects.all():
        model_resp = {}
        for mc in model_columns:
            model_resp[mc.name] = getattr(dm, mc.name)
        result.append(model_resp)
    return result


def get_tables():
    existing_models = DynamicTable.objects.all()
    return existing_models


def add_row(pk, row_data):
    existing_model = DynamicTable.objects.get(pk=pk)
    model_columns = existing_model.dynamictablecolumn_set.all()
    fields = get_fields_for_columns(model_columns)
    dynamic_model = create_dynamic_model(existing_model.name, fields, 'dynamic')
    new_row = dynamic_model.objects.create(**row_data)
    # create response model
    response_model = {
        'pk': new_row.pk
    }
    for mc in model_columns:
        response_model[mc.name] = getattr(new_row, mc.name)
    return response_model


def get_fields_for_columns(columns):
    fields = {}
    for mc in columns:
        model_type = models.CharField(max_length=255)
        if mc.type == 'INTEGER':
            model_type = models.IntegerField()
        elif mc.type == 'BOOLEAN':
            model_type = models.BooleanField()
        fields[mc.name] = model_type
    return fields


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
