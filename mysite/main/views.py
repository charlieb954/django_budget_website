from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Budget, Item
from .forms import CreateNewList

import plotly.graph_objs as go
from plotly.offline import plot

# Create your views here.

def chunker(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i:i+n]

@login_required(login_url='/login/')
def index(request, id):
    ls = Budget.objects.get(id=id)
    
    if ls in request.user.budget.all():
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
                obj = [ob for ob in obj if str(ob.budget) == str(ls.name)]
                
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

@login_required(login_url='/login/')
def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    if request.method == "POST":
        form = CreateNewList(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            if Budget.objects.filter(name=n).exists():
                b = Budget.objects.get(name=n)
                return HttpResponseRedirect(f"/{b.id}")
            else:
                b = Budget(name=n)
                b.save()
                request.user.budget.add(b)
                return HttpResponseRedirect(f"/{b.id}")
    
    else:
        form = CreateNewList()
    return render(request, "main/create.html", {"form":form})

@login_required(login_url='/login/')
def view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    
    if "taskDelete" in request.POST: #checking if there is a request to delete a bud
        checked_list = request.POST["checkedbox"] #checked bud to be deleted
        bud = Budget.objects.get(id=checked_list) #getting bud id
        bud.delete() #deleting bud
        return render(request, "main/view.html")
    
    return render(request, "main/view.html", {})

@login_required(login_url='/login/')
def budget_summary(request):
    income = []
    outgoings = []
    
    for i in Item.objects.all():
        if str(i.budget) == "Income":
            income.append(float(i.cost))
        elif str(i.budget) == "Outgoings":
            outgoings.append(float(i.cost))
            
    total_income = format(sum(income), '.2f')
    total_outgoings = format(sum(outgoings), '.2f')

    x = ['Income', 'Outgoings']
    y = [sum(income), sum(outgoings)]

    # Use the hovertext kw argument for hover text
    fig = go.Figure(data=[go.Bar(x=x, y=y,
                hovertext=[f"£{total_income}", f"£{total_outgoings}"])])

    fig.update_layout(title_text='Budget Bar Chart',
                          xaxis_title="Budget type",
                          yaxis_title="Amount (in £s)",)
    
    div = plot(fig, output_type='div')
    
    return render(request, "main/summary.html", {"total_income": total_income,
                                                 "total_outgoings": total_outgoings,
                                                 "div": div})