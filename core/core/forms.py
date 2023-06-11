from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *


class EnhancedModelForm(forms.ModelForm):
    '''additional features:
        - filter based on model choices keys and groups
    '''

    MAX_WIDTH_FIELD = None
    FORM_TEMPLATE = None
    FORM_TAG = False


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Template
        self.helper = FormHelper()
        self.helper.form_tag = self.FORM_TAG
        self.helper.template = self.FORM_TEMPLATE



    def filter_choices(self, field_name: str, category_filter: list, item_filter: list = None):
        choices = []
        for group in self.fields[field_name].choices:
            if group[0] in category_filter:
                if item_filter:
                    items = tuple(
                        filter(lambda x: x[0] in item_filter, list(group[1])))
                else:
                    items = group[1]
                choices.append((group[0], items))
        self.fields[field_name].choices = choices

    def find_key(self, d, value):
        return next(filter(lambda k: value in d[k], d.keys()), None)
