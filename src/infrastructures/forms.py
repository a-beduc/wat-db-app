from django import forms


class WaterMeterCreateForm(forms.Form):
    rg_code = forms.CharField(max_length=10)
    internal_number = forms.IntegerField(min_value=0)
    serial_id = forms.CharField(max_length=15)
    subscriber_name = forms.CharField(max_length=200)
    raw_address = forms.CharField(max_length=200)

    def clean_rg_code(self):
        return self.cleaned_data['rg_code'].strip().upper()

    def clean_serial_id(self):
        return self.cleaned_data['serial_id'].strip().upper()
