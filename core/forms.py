from django.forms import ModelForm

from core.models import ShortURL


class ShortURLForm(ModelForm):
    """
    The form is useful in that case because it uses an URLValidator on the field url
    """
    class Meta:
        model = ShortURL
        fields = ["url"]
