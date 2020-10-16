from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label='Select budget:', widget=forms.Select(choices=[('Income', 'Income'),
                                                                                ('Outgoings', 'Outgoings')]))