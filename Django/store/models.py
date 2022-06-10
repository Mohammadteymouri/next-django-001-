from email.mime import image
from unicodedata import name
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel , TreeForeignKey


class Category(MPTTModel):

    name = models.CharField(
        verbose_name= _("Category Name"), 
        help_text= _("request and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name= ("Category safe URl "), max_length=225 , unique= True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE , null = True, blank= True, related_name="children" )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by =["name"]

    class Meta : 
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name

class ProductType(models.Model):

    name = models.CharField(verbose_name=_("Product Name"), help_text=_("Required"), max_length= 250)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product types")

    def __str__(self):
        return self.name

class ProductSpecification(models.Model):
    produt_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length= 250)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name

class Product(models.Model):

    produt_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name = _("titel"),
        help_text=_("Required"),
        max_length = 255,
    )
    description = models.TextField(verbose_name =_("description"), help_text=_("Not Required"), blank= True)
    slug = models.SlugField(max_length =225)
    regular_price = models.DecimalField(
        verbose_name = _("Regular price"),
        help_text= _("Maximum 999.99"),
        error_messages = {
            "name": {
                "max_length": _("the price must be 0 and 999.99"),
            },
        },
        max_digits =5,
        decimal_places=2, 
    )

    discount_price = models.DecimalField(
        verbose_name = _("Discount price"),
        help_text= _("Maximum 999.99"),
        error_messages = {
            "name": {
                "max_length": _("the price must be 0 and 999.99"),
            },
        },
        max_digits =5,
        decimal_places=2, 
    )
    
    is_active = models.BooleanField(
        verbose_name = _("Product visibility"),
        help_text = _("Change product visibility"),
        default= True,
    )
    created_at = models.DateTimeField(_("created_at"), auto_now_add = True , editable= False)
    updated_at = models.DateTimeField(_("updatedd_at"), auto_now = True )

    class Meta:
        ordering = _("created_at")
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specifiction = models.ForeignKey(ProductSpecification , on_delete=models.RESTRICT)
    value = models.CharField(verbose= _("value"), help_text = _("product specifiction value (maximum of 225 words") , max_length=255)

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Value")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name ="product_image")
    image = models.ImageField(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name = _("image"),
        help_text=_("upload a product image"),
        upload_to = "image/",
        default="image/defulat.png", 
    )
    alt_text = models.CharField(
        verbose_name = _("Alturnative text "),
        help_text= _("Please add alturnative text"),
        max_length= 255, 
        null = True,
        blank= True,

    ) 
    is_feature = models.BooleanField (default= False)
    
    created_at = models.DateTimeFielda(_("created_at"), auto_now_add = True , editable= False)
    updated_at = models.DateTimeFielda(_("updatedd_at"), auto_now = True )

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Image")

