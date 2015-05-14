#coding:utf8
from django.forms.widgets import RadioInput, RadioSelect, RadioFieldRenderer
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import format_html


class ExtRadioInput(RadioInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = format_html(' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = force_text(self.choice_label)
        return format_html(u'{1}<label{0}>{2}</label>', label_for, self.tag(), choice_label)


@python_2_unicode_compatible
class ExtRadioFieldRenderer(RadioFieldRenderer):
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield ExtRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx]
        return ExtRadioInput(self.name, self.value, self.attrs.copy(), choice, idx)


class ExtRadioSelect(RadioSelect):
    renderer = ExtRadioFieldRenderer