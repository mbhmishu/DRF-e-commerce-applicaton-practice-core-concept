from django.db import models
from django.utils.text import slugify
from Accounts.models import User


#Category model
class Category(models.Model):
    title = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


#Tag model
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


#Product model
class Product(models.Model):
    name = models.CharField(max_length=264,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category',null=True,blank=True)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text',null=True,blank=True)
    detail_text = models.TextField(max_length=1000, verbose_name='Description',null=True,blank=True)
    slug = models.SlugField(unique=True, blank=True,null=True)
    tags = models.ManyToManyField(Tag, through='TagConnector', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created',]


#ProductImg model
class ProductImg(models.Model):
    mainimage = models.ImageField(upload_to='Imgs')

    def __str__(self):
        return self.mainimage.name


#ImgConnector model
class ImgConnector(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images',null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    mainimage = models.ForeignKey(ProductImg, on_delete=models.CASCADE)


#TagConnector model
class TagConnector(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.tag.name} '

#For product Variantion


class Color(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'color'
        verbose_name_plural = 'colors'

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'size'
        verbose_name_plural = 'sizes'

    def __str__(self):
        return self.name



class Material(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'material'
        verbose_name_plural = 'materials'

    def __str__(self):
        return self.name



class Attribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='attributes',null=True,blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='attributes',null=True,blank=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='attributes',null=True,blank=True)
    price = models.FloatField(default=0.00) # 100
    discount_percentage = models.FloatField(blank=True,null=True) # 10
    discount_amount = models.FloatField(blank=True,null=True,default=0.00) # this field is no need in model.

    @property
    def discounted_price(self):
        if self.discount_percentage:
            return self.price - self.discount_amount

    def save(self, *args, **kwargs):
        if self.discount_percentage:
            self.discount_amount = (self.price * self.discount_percentage) / 100
        super(Attribute, self).save(*args, **kwargs) 

    class Meta:
        verbose_name = 'attribute'
        verbose_name_plural = 'attributes'
        unique_together = ('product', 'color', 'size', 'material')

    def __str__(self):
        return f'{self.product} - {self.color} - {self.size} - {self.material}'

