from datetime import datetime

from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.pos.choices import genders


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.__str__()
        item['category'] = self.category.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = f'{self.pvp:.2f}'
        return item

    def get_image(self):
        if self.image:
            return f'{settings.local.MEDIA_URL}{self.image}'
        return f'{settings.local.STATIC_URL}img/empty.png'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Número de cedula')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=genders, default='male', verbose_name='Genero')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names} ({self.dni})'

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Company(models.Model):
    name = models.CharField(max_length=150, verbose_name='Razón social')
    nit = models.CharField(max_length=12, verbose_name='NIT')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    phone = models.CharField(max_length=7, verbose_name='Teléfono')
    mobile = models.CharField(max_length=12, null=True, blank=True, verbose_name='Celular')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='Correo electrónico')
    website = models.CharField(max_length=100, null=True, blank=True, verbose_name='Sitio web')
    cover = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Portada')
    logo = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Logotipo')

    def __str__(self):
        return self.name

    def get_image_cover(self):
        if self.cover:
            return f'{settings.local.MEDIA_URL}{self.cover}'
        return f'{settings.local.STATIC_URL}img/empty.png'

    def get_image_logo(self):
        if self.logo:
            return f'{settings.local.MEDIA_URL}{self.logo}'
        return f'{settings.local.STATIC_URL}img/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['cover'] = self.get_image_cover()
        item['logo'] = self.get_image_logo()
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        default_permissions = ()  # Con esto le estamos diciendo que no se creen los permisos por defecto
        permissions = (
            ('change_company', 'Can edit company'),
        )  # Habilitamos solamente este permiso
        ordering = ['id']


class Sale(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Compañía')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Subtotal')
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='IVA')
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Total IVA')
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Total')

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

    def get_number(self):
        return f'{self.id:06d}'
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Sale, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['client'] = self.client.toJSON()
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['saleproduct'] = [i.toJSON() for i in self.saleproduct_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.saleproduct_set.all():
            detail.product.stock += detail.cant
            detail.product.save()
        super(Sale, self).delete()

    def calculate_invoice(self):
        subtotal = self.saleproduct_set.all().aggregate(result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    def __str__(self):
        return self.client.names


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['id']
        
    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item
    
    def __str__(self):
        return self.product.name