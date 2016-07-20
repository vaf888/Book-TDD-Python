from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    #print(">>>>>>>>>>> TESTS ONLY: in views.home_page")
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def new_list(request):
    #print(">>>>>>>>>>> TESTS ONLY: in views.new_list")
    new_item_text = request.POST['item_text']
    list_ = List.objects.create()
    Item.objects.create(text=new_item_text, list=list_)
    return redirect('/lists/the-only-list-in-the-world/')

def list_view(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
