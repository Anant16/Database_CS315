from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _


class StockForm(forms.Form):
    Handle = forms.RegexField(label=_("Handle"), max_length=20,
        regex=r'^[A-Za-z0-9|\.|\-|]+$',
        help_text=_("Required. 5 characters or fewer. Latin letters or digits"),
        error_messages={
            'invalid': _("This value may contain only latin letters or digits"),
        })

class QueryForm(forms.Form):
    Handle = forms.RegexField(label=_("Handle"), max_length=20,
        regex=r'^[A-Za-z0-9|.|-|]+$',
        help_text=_("Required. 20 characters or fewer. Latin letters or digits"),
        error_messages={
            'invalid': _("This value may contain only latin letters or digits,. or -"),
        })
    BeginDate = forms.CharField(label=_("Begin Date"), max_length=10)
    EndDate = forms.CharField(label=_("End Date"), max_length=10)

# class SymbolInfoForm(forms.Form):
#     Handle = forms.RegexField(label=_("Handle"), max_length=20,
#         regex=r'^[A-Za-z0-9|.|-|]+$',
#         help_text=_("Required. 20 characters or fewer. Latin letters or digits"),
#         error_messages={
#             'invalid': _("This value may contain only latin letters or digits,. or -"),
#         })
# class lastUpdatedForm(forms.Form):
#     Handle = forms.RegexField(label=_("Handle"), max_length=20,
#         regex=r'^[A-Za-z0-9|.|-|]+$',
#         help_text=_("Required. 20 characters or fewer. Latin letters or digits"),
#         error_messages={
#             'invalid': _("This value may contain only latin letters or digits,. or -"),
#         })
class DayInfoForm(forms.Form):
    Date = forms.CharField(label=_("Date"), max_length=10)
