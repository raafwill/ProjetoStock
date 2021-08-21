from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import csv
from .models import Stock
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm, ReorderLevelForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
        title = 'Bem vindo: Esse é o nosso estoque'
        context =  {"title":title,}
        return render(request, "home.html", context)

@login_required
def list_items(request):
    form = StockSearchForm( request.POST or None )
    header = 'Lista de Bebidas'
    queryset = Stock.objects.all()
    context = {
        "form": form,
        "header": header,
        "queryset": queryset,
         }


    if request.method == 'POST':
        queryset = Stock.objects.filter(#bebida__icontains=form['bebida'].value(),
                                        )

        if form['export_to_CSV'].value() == True:
            response = HttpResponse( content_type='text/csv' )
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer( response )
            writer.writerow( ['Bebida', 'Quantidade', 'Preço'] )
            instance = queryset
            for stock in instance:
                writer.writerow( [stock.bebida, stock.quantidade, stock.preco_compra] )
            return response


        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
            }

    return render(request, "list_items.html", context)


@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success( request, 'Item adicionado' )
        return redirect('/list_items')
    context = {"form":form,
               "title": "Adicionar Items",
               }
    return render(request, "add_items.html", context)


def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Atualizado')
			return redirect('/list_items')


	context = {'form':form}
	return render(request, 'add_items.html', context)


def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Deletado com sucesso')
		return redirect('/list_items')

	return render(request, 'delete_items.html')


def stock_details(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {"title": queryset.bebida,
			   "queryset": queryset,
			   }
	return render(request, 'stock_details.html', context)


def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantidade -= instance.reportar_erro
		instance.erro_por = str(request.user)
		messages.success(request, "RReportado com sucesso. " + str(instance.quantidade) + " " + str(instance.bebida) + "s now left in Store")
		instance.save()

		return redirect('/stock_details/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Reportada ' + str(queryset.bebida),
		"queryset": queryset,
		"form": form,
		"username": 'Reportado por: ' + str(request.user),
	}
	return render(request, "add_items.html", context)



def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantidade += instance.recebido
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantidade) + " " + str(instance.bebida)+"s now in Store")

		return redirect('/stock_details/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Recebido ' + str(queryset.bebida),
			"instance": queryset,
			"form": form,
			"username": 'Recebido por: ' + str(request.user),
		}
	return render(request, "add_items.html", context)


def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.bebida) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_items")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)

