# Similarly to models.py, forms.py stores all the form declarations.

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import datetime

class RenewBookForm(forms.Form):

    # Set up the date field. There are MANY field types. https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        # Below: Clean data using default validators to make sure there is no unsafe input, and return
        # the correct data type (in this case, a datetime object).
        data = self.cleaned_data['renewal_date']
        
        # Validation Errors: Add own bounds to data, and the string message to be printed in the form if you get an invalid
        # submission. Note that the _ function is part of one of Django's translator for easy translation if that is 
        # required later.

        # Check if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

