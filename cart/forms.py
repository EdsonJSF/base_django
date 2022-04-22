from django import forms

class CartAddItemForm(forms.Form):
    quantity = forms.IntegerField(label='Cantidad', initial=1)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(CartAddItemForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'