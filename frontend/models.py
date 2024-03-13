from django.db import models
from user.models import BaseModel, _



""" Frontend User Home Page Banner Model. """
class Banner(BaseModel):
    image = models.ImageField(
        _("Banner Image"),
        upload_to='frontend/banner-images/',
        help_text="Image Type: jpg,png,gif,jpeg"
    )
    alt = models.CharField(
        max_length=256, 
        verbose_name=_('Alt')
    )

    class Meta:
        verbose_name = _("Fronted Banner")
        verbose_name_plural = _("Fronted Banners")
        
    def __str__(self):
        return str(self.id)
