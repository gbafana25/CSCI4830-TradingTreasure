from django.shortcuts import render, redirect
from .forms import ItemForm
from .models import Item
from django.shortcuts import get_object_or_404, redirect

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form})


def item_list(request):
    items = Item.objects.all()
    return render(request, 'items/item_list.html', {'items': items})


def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/item_form.html', {'form': form})

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'items/item_confirm_delete.html', {'item': item})

