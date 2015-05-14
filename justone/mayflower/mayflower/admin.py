from django.contrib.admin import ModelAdmin
from django import forms
from redactor.fields import RedactorField
from redactor.widgets import RedactorEditor


class RedactorAdminForm(forms.ModelForm):
    class Media:
        css = {'all': ('//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css',
                       'redactor/additional.css')}

    def __init__(self, *args, **kwargs):
        super(RedactorAdminForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            if isinstance(self._meta.model._meta.get_field(field_name), RedactorField):
                self.fields[field_name].widget = RedactorEditor()


class RedactorAdmin(ModelAdmin):
    form = RedactorAdminForm


class SingleObjectAdmin(ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return not self.model.objects.exists()


class RedactorSingleObjectAdmin(RedactorAdmin, SingleObjectAdmin):
    pass