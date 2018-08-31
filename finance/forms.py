from directory_components import forms, fields


class ExampleForm(forms.Form):
    email = fields.EmailField()
    firstname = fields.CharField(label='First name')
    lastname = fields.CharField(label='Last name')
