
from django import forms
from datetime import timedelta
class SplitDurationWidget(forms.MultiWidget):
    """
    A Widget that splits duration input into four number input boxes.
    """
    def __init__(self, attrs=None):
        widgets = (forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs))
        super(SplitDurationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = value
            if d:
                hours = d.seconds // 3600
                minutes = (d.seconds % 3600) // 60
                seconds = d.seconds % 60
                return [int(d.days), int(hours), int(minutes), int(seconds)]
        return [0, 1, 0, 0]

class MultiValueDurationField(forms.MultiValueField):
     widget = SplitDurationWidget

     def __init__(self, *args, **kwargs):
         fields = (
             forms.IntegerField(label="Days"),
             forms.IntegerField(),
             forms.IntegerField(),
             forms.IntegerField(),
         )
         super(MultiValueDurationField, self).__init__(
             fields=fields,
             require_all_fields=True, *args, **kwargs)

     def compress(self, data_list):
         if len(data_list) == 4:
             return timedelta(
                 days=int(data_list[0]),
                 hours=int(data_list[1]),
                 minutes=int(data_list[2]),
                 seconds=int(data_list[3]))
         else:
             return timedelta(0)
