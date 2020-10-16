from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.

def chunker(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i:i+n]

def index(request, id):
    ls = ToDoList.objects.get(id=id)
    
    if ls in request.user.todolist.all():
        if request.method == "POST":                    
            if request.POST.get("newItem"):
                txt = request.POST.get("outgoing")
                cost = request.POST.get("cost")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, cost=cost)
                else:
                    print("invalid input")
            
            elif request.POST.get("update"):
                a = request.POST.getlist('items')
                b = list(chunker(a, 2))
                
                obj = Item.objects.all()
                print(obj)
                
                i = 0
                for ob in obj:
                    ob.text = a[i]
                    ob.cost = a[i+1].lstrip("£").strip()
                    ob.save()
                    i+=2
                    
        return render(request, "main/list.html", {"ls":ls})
    return render(request, "main/view.html", {})

def home(request):
    return render(request, "main/home.html", {})

def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    if request.method == "POST":
        form = CreateNewList(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            request.user.todolist.add(t)
            
            return HttpResponseRedirect(f"/{t.id}")
    
    else:
        form = CreateNewList()
    return render(request, "main/create.html", {"form":form})

def view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    
    if "taskDelete" in request.POST: #checking if there is a request to delete a todo
        checked_list = request.POST["checkedbox"] #checked todos to be deleted
        todo = ToDoList.objects.get(id=checked_list) #getting todo id
        todo.delete() #deleting todo
        return render(request, "main/view.html")
    
    return render(request, "main/view.html", {})