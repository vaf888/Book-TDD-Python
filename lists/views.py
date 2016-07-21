from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def new_list(request):
    new_item_text = request.POST['item_text']
    list_ = List.objects.create()
    Item.objects.create(text=new_item_text, list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def view_list(request, list_id):
    list_id.strip()
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'list':list_, 'items': items})

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text, list=list_)
    return redirect('/lists/%d/' % (list_.id,))
