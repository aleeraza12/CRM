
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm, CreateUserForm, TagForm,CustomerForm, ProductForm
from django.forms import inlineformset_factory
from .filter import OrderFilter,CustomerFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_user,admin_only
from django.contrib.auth.models import Group




@unauthenticated_user
def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('customer_order')
    # else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request , user)
                return redirect('customer_order')
            else:
                messages.info(request,'User name or password is incorrect')

        return render(request, 'salesforce/login.html')


@unauthenticated_user
def register(request):
    # if request.user.is_authenticated:
    #     return redirect('customer_order')
    # else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email,
                )

                messages.success(request,'Account created successfully of ' + username)
                return redirect('login')
        context = {'form': form}
        return render(request, 'salesforce/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def Tags(request):
    tags = Tags.objects.all()
    return render(request, 'salesforce/home.html', {'tags': tags})

@login_required(login_url='login')
@admin_only
def products(request):
    #product = Product.objects.filter(tags__name="Food")
    #product1 = Product.objects.filter(tags__name="Kitchen")
    #product2 = Product.objects.filter(tags__name="Sports")
    #product3 = Product.objects.filter(tags__name="Summer")
    #product4 = Product.objects.filter(tags__name="Medication")
    product_list = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 5)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    return render(request, 'salesforce/home.html', {'product': product})

@login_required(login_url='login')
@admin_only
def customerorder(request):
    customer = Customer.objects.all()
    order = Order.objects.all()
    total_customer = customer.count()
    total_order = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()
    ofd = order.filter(status='Out for Delivery').count()

    context =  {'customer': customer,
                'order': order,
                'total_order': total_order,
                'total_customer': total_customer,
                'delivered': delivered,
                'pending': pending,
                'ofd': ofd}
    return render(request, 'salesforce/customerorder.html',context)

@login_required(login_url='login')
@admin_only
def customer(request,pk_test):
        customer = Customer.objects.get(id=pk_test)
        order_list = customer.order_set.all()
        myFilter = OrderFilter(request.GET, queryset=order_list)
        order_list = myFilter.qs
        page = request.GET.get('page', 1)
        paginator = Paginator(order_list, 6)
        try:
            order = paginator.page(page)
        except PageNotAnInteger:
            order = paginator.page(1)
        except EmptyPage:
            order = paginator.page(paginator.num_pages)
        total_order = order_list.count()
        delivered = order_list.filter(status='Delivered').count()
        pending = order_list.filter(status='Pending').count()
        ofd = order_list.filter(status='Out for Delivery').count()
        #order_ = customer.order_set.all()

        #print(order)
        context = {'customer':customer,
                   'order':order,

                   'total_order': total_order,
                   'delivered': delivered,
                   'pending': pending,
                   'ofd': ofd,
                   'myFilter': myFilter
                   }
        return render(request, 'salesforce/singlecustomer.html', context)

@login_required(login_url='login')
def createOrder(request, pk):
    orderFormset = inlineformset_factory(Customer, Order, fields=('product', 'status','note'), extra=5)
    formset = orderFormset(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = orderFormset(request.POST, instance=customer)
    #if form.is_valid():
        if formset.is_valid():
            formset.save()
            return redirect('customer_order')

    context = {'formset': formset,'Cus_Filter':Cus_Filter}
    return render(request, 'salesforce/order_form.html',context)

@login_required(login_url='login')
@admin_only
def UpdateOrder(request,pk):
    #form = OrderForm()
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('customer_order')
    context = {'form': form}
    return render(request, 'salesforce/order_form.html',context)


@login_required(login_url='login')
@admin_only
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('customer_order')

    context = {'item': order}
    return render(request, 'salesforce/deleteorder.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ofd = orders.filter(status='Out for Delivery').count()

    context = {
               'orders': orders,
               'total_order': total_order,
               'delivered': delivered,
               'pending': pending,
               'ofd': ofd}
    return render(request, 'salesforce/userorder.html',context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def showtotaluser(request):
    customer = Customer.objects.all()
    context = {'customer':customer}
    return render(request, 'salesforce/showusertoadmin.html',context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userprofile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'salesforce/cust_profile.html', context)


@login_required(login_url='login')
@admin_only
def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'salesforce/add_product.html', context)


@login_required(login_url='login')
@admin_only
def addTag(request):
    form = TagForm()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'salesforce/add_tag.html', context)


