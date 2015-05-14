#coding:utf8
from django import forms


class PlaceholderForm(object):
    def __init__(self, *args, **kw):
        super(PlaceholderForm, self).__init__(*args, **kw)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'placeholder': self.fields[field].label})


class ErrorsForm(object):
    def is_valid(self):
        result = super(ErrorsForm, self).is_valid()

        for field in self:
            if field.errors:
                self.fields[field.name].widget.attrs.update({'class': 'error'})

        return result


class PlaceholderErrorsForm(PlaceholderForm, ErrorsForm):
    pass


class BackCallForm(PlaceholderErrorsForm, forms.Form):
    name = forms.CharField(max_length=100, label=u'Имя', widget=forms.TextInput(attrs={'placeholder': u'Имя'}), required=False)
    phone = forms.CharField(max_length=100, label=u'Телефон', widget=forms.TextInput(attrs={'placeholder': u'Телефон'}))