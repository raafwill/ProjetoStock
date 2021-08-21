from django.db import models



bebida_choice = (
		('Brahma', 'Brahma'),
		('Skol', 'Skol'),
		('Glacial', 'Glacial'),)

# Create your models here.

class Bebida(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
	bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE, blank=True)
	quantidade = models.IntegerField(default='0', blank=False, null=True)
	preco_compra = models.IntegerField(default='0', blank=False, null=True)
	data_recebimento = models.DateTimeField(auto_now_add=False, auto_now=True)
	reportar_erro = models.IntegerField(default='0', blank=False, null=True)
	erro_por = models.CharField( max_length=50, blank=True, null=True )
	recebido = models.IntegerField(default='0', blank=False, null=True)
	recebido_por = models.CharField( max_length=50, blank=True, null=True )
	reorder_level = models.IntegerField(default='0', blank=False, null=True)

	def __str__(self):
		return self.bebida

