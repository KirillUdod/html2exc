from django import forms
from products.models import Bouquet


class DependenciesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DependenciesForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        dependencies = getattr(self.Meta.model, 'dependencies', {})

        if isinstance(dependencies, dict):
            for (depend_field, depend_field_value), fields in dependencies.iteritems():
                if not isinstance(self.fields[depend_field], forms.BooleanField)\
                        and not getattr(self.fields[depend_field], 'choices', None):
                    raise ValueError()

                if not isinstance(fields, (list, tuple)):
                    fields = [fields]

                required = False

                if self.data:
                    post_value = self.data.get(self.add_prefix(depend_field))
                    if post_value == 'on' and isinstance(depend_field_value, bool):
                        post_value = 'True'

                    if post_value == unicode(depend_field_value):
                        required = True
                elif instance and getattr(instance, depend_field, None) == depend_field_value:
                    required = True

                for field in fields:
                    self.fields[field].required = required


class BouquetAdminForm(DependenciesForm):
    class Meta:
        model = Bouquet