from django.forms import ModelForm

from catalog.models import GoodItem


class GoodItemForm(ModelForm):
    class Meta:
        model = GoodItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GoodItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''