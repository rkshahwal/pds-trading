from django.db import models
from user.models import BaseModel, _
from django.utils import timezone
from datetime import timedelta



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



""" Market Game Model. """
class Market(BaseModel):
    sybmol = models.ImageField(
        _("Market Symbol Image"),
        upload_to='frontend/market-symbol/',
        default="btc.png",
        help_text="Image Type: jpg,png,gif,jpeg"
    )
    name = models.CharField(
        max_length=256, 
        verbose_name=_('Name')
    )
    latest_price = models.FloatField(_("Latest Price"), default=0.0)
    fun_range = models.FloatField(_("Fluctuation Range"), default=0.0, help_text="In percentage.")
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Market Game")
        verbose_name_plural = _("Market Games")
        
    def __str__(self):
        return str(self.name)



class MarketBid(BaseModel):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="bid_results")
    bid = models.CharField(
        choices = (
            ("Call","Call"),
            ("Put","Put"),
        ),
        max_length = 5
    )
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(
        default=timezone.now() + timedelta(minutes=3)
    )
    
    class Meta:
        ordering = ('-start_time',)
        verbose_name = _("Market Bid Result")
        verbose_name_plural = _("Market Bid Results")
    
    def __str__(self) -> str:
        return f"{self.id} - {self.market}"
