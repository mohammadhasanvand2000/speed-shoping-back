from colorfield.fields import ColorField
from django.db import models
from django.db.models import Count, F, Value
from accounts.models import User

class Grouping(models.Model):
    title= models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return '{}'.format (self.title )


class Product (models.Model):
    grouping    = models.ForeignKey(Grouping,on_delete=models.CASCADE,related_name="grouping",verbose_name=("grouping"))
    title       = models.CharField(max_length=200,null=True,blank=True)
    price       = models.IntegerField(default='1000',null=True,blank=True)
    image       = models.ImageField(upload_to="assets\img\products",null=True,blank=True)
    slug        = models.SlugField(unique=True, max_length=255,null=True,blank=True) 
    


    def __str__(self):
        return '{},{},{},{},'.format (self.title ,self.price,self.image,self.slug )

class Detail(models.Model):
    #COLOR_CHOISES=[]

    producti            = models.OneToOneField(Product,on_delete=models.CASCADE,related_name="productdetail",verbose_name=("product"))
    discribtion         = models.CharField(max_length=1000,null=True,blank=True)
    introduction        = models.CharField(max_length=2000,null=True,blank=True)
    Alloy               = models.CharField(max_length=200,null=True,blank=True)
    
    warranty            = models.IntegerField(null=True,blank=True)
    made_in             = models.CharField(max_length=50,null=True,blank=True)
    dimensions          = models.FloatField(null=True,blank=True)
    in_dimensions       = models.FloatField(null=True,blank=True)
    Weight              = models.IntegerField(null=True,blank=True)

    used                = models.CharField(max_length=100,null=True,blank=True)
    size                = models.CharField(max_length=100,null=True,blank=True)
    size_body           = models.CharField(max_length=100,null=True,blank=True)
    Set_of_accessories  = models.CharField(max_length=100,null=True,blank=True) 
        
    
   

    def __str__(self):
        return '{},{},{},{},{}'.format (self.discribtion ,self.introduction,self.warranty,self.made_in,self.dimensions )


class Product_image(models.Model):
    producti            = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="productimage",verbose_name=("producti"),null=True)
    image               = models.ImageField(upload_to="assets\img\products",null=True,blank=True)


    def __str__(self):
        return '{},'.format (self.image , )

class Product_color(models.Model):
    producti            = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="productcolor",verbose_name=("producti"),null=True)
    color               = ColorField(default='#FF0000',null=True,blank=True)
    title               = models.CharField(max_length=200,null=True,blank=True)

 

class Client_Coments(models.Model):
    producti            = models.OneToOneField(Product,on_delete=models.SET_NULL,related_name="cproduct",verbose_name=("cproduct"),null=True)
    coment              = models.CharField(max_length=10000,null=True,blank=True)
    img                 = models.ImageField(help_text="plase enter images your product ",null=True,blank=True)


    def __str__(self):
        return '{},{}'.format (self.coment ,self.img,)



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="usercart", verbose_name=("user"))
    items = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f'Cart for User: {self.user.name}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_cart_items")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.quantity} of {self.product.title} in Cart for User: {self.cart.user.name}'



    






    