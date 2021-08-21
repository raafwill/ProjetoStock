from django import forms
from .models import Stock

class StockCreateForm(forms.ModelForm):
   class Meta:
     model = Stock
     fields = ['bebida', 'quantidade', 'preco_compra']

   def clean_bebida(self):
       bebida = self.cleaned_data.get( 'bebida' )
       if not bebida:
           raise forms.ValidationError( 'Esse campo é obrigatório' )

       for instance in Stock.objects.all():
           if instance.bebida == bebida:
               raise forms.ValidationError( str( bebida ) + ' já está cadastrada' )
       return bebida


   def clean_quantidade(self):
       quantidade = self.cleaned_data.get( 'quantidade' )
       if not quantidade:
           raise forms.ValidationError( 'Esse campo é obrigatório' )
       return quantidade


class StockSearchForm(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required=False)
   class Meta:
     model = Stock
     fields = ['bebida']


class StockUpdateForm(forms.ModelForm):
   class Meta:
     model = Stock
     fields = ['bebida', 'quantidade', 'preco_compra']


class IssueForm( forms.ModelForm ):
	class Meta:
		model = Stock
		fields = ['reportar_erro', 'erro_por']


class ReceiveForm( forms.ModelForm ):
	class Meta:
		model = Stock
		fields = ['recebido', 'recebido_por']


class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']




