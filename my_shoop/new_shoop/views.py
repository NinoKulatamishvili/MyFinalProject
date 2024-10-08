from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Products, Categories, User, Gender, Comment
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, ProductsForm, UserForm
from . seeder import seeder_func
from django.contrib import messages

#Create your views here.
# def home(request):
#     q=request.GET.get('q') if request.GET.get('q') !=None else ''
#     seeder_func()
#     products = Products.objects.filter(Q(category_name__icontains=q) | Q(stock_quantity__icontains=q) | Q(category__icontains=q)) #
#     products = list(dict.fromkeys(products))
#     #products=Products.objects.all()
#     gender=Gender.objects.all()
#     context = {"products": products, 'gender': gender}  #პითონიდან გადავცეთ ინფორმაცია გვერდს
#     return render(request, "new_shoop/home.html", context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    # seeder_func()
    products = Products.objects.filter(

        Q(description__icontains=q)
    ).distinct()    #Q(category_name__icontains=q) |Q(stock_quantity__icontains=q)
    gender = Gender.objects.all()
    context = {"products": products, 'gender': gender}
    return render(request, "new_shoop/home.html", context)



def about(request):
    return render(request, "new_shoop/about.html")

@login_required(login_url='login')
def profile(request, ms):
    user=User.objects.get(id=ms)
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    products = user.products_user.filter(Q(category_name__icontains=q) | Q(stock_quantity__icontains=q))
    products = list(set(products))
    gender = Gender.objects.all()
    #products=user.products.all()
    context = {"products": products, 'gender': gender}
    return render(request, "new_shoop/profile.html", context)

def adding(request, id):
    user=request.user
    products=Products.objects.get(id=id)
    user. products_user.add(products)
    return redirect('profile', user.id)

def delete(request, id):
    obj = Products.objects.get(id=id)
    if request.method =="POST":
        request.user.products_user.remove(obj)
        return redirect('profile', request.user.id)
    return render(request, 'new_shoop/delete.html', {'obj': obj})





        #return redirect('profile', request.user.id)
    #return render(request, "new_shoop/delete.html", {'obj': obj})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.id)
    if request.method =="POST":
        username=request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'User dose not exist')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', request.user.id)
        else:
            messages.error(request, 'User or Password is not correct')

    return render(request, "new_shoop/login.html")

def logout_user(request):
    logout(request)
    return redirect('home')
def register_user(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile', user.id)
        else:
            messages.error(request, 'Follow the instruction and  create user and password')



    context={'form': form}
    return render(request, "new_shoop/register.html", context)

# def add_product(request):
#     categories=Categories.objects.all()
#     gender=Gender.objects.all()
#     form=ProductsForm()
#
#     #new_product= Products(picture=request.FILES['picture'], categories=form.data['categories'],description=form.data['description']) #creator=request.user
#     #new_product.save() #
#     #new_product.category.add(categories) #
#     #return redirect('home') #
#
#     context={'form': form, 'categories':categories, 'gender': gender}
#     #return render(request, "new_shoop/add_product.html", context) ##
@login_required(login_url='login')
def add_product(request):
    categories = Categories.objects.all()
    genders = Gender.objects.all()
    form = ProductsForm()

    if request.method == 'POST':
        try:
            form = ProductsForm(request.POST)
            product_category = Categories.objects.get(id=form.data['category'])
            product = Products(creator=request.user, picture=request.FILES['picture'], category_name=form.data['category_name'],
                               category=product_category, price=form.data['price'], description=form.data['description'],
                               stock_quantity=form.data['stock_quantity'])

            product.save()
            gender_ids = request.POST.getlist('gender')
            product.gender.set(gender_ids)
            messages.success(request, 'Product added successfully')
        except:
            messages.error(request, 'Please correct the errors below.')
            return redirect('home')

    context = {'form': form, 'categories': categories, 'genders': genders}
    return render(request, 'new_shoop/add_product.html', context)

def reading(request, id):
    product = Products.objects.get(id=id)
    product_comments = product.comment_set.all()  # .order_by('-created')
    if request.method == "POST":
        Comment.objects.create(
            user=request.user,
            product=product,
            body=request.POST.get('body')
        )
    return render(request, "new_shoop/reading.html", {'product': product, 'comments': product_comments})

# def reading(request, id):
#     product=Products.objects.get(id=id)
#     product_comments = product.comment_set.all()  # .order_by('-created')
#     if request.method == "POST":
#         Comment.objects.create(
#             user=request.user,
#             product=product,
#             body=request.POST.get('body')
#         )
#     return render(request, "new_shoop/reading.html", {'product': product,  'comments':product_comments})

def delete_product(request, id):
    obj=Products.objects.get(id=id)

    if request.method == "POST":
        obj.picture.delete()
        #obj.file.delete()
        obj.delete()
        return redirect('home')
    return render(request, 'new_shoop/delete.html', {'obj': obj})

# def update_user(request):
#     form=UserForm()
#     context={'form': form}
#     return render(request, 'new_shoop/update_user.html')

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.id)

    context = {'form': form}
    return render(request, 'new_shoop/update_user.html', context)

def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    product = comment.product
    if request.method == 'POST':
        comment.delete()
        return redirect('reading', product.id)

    return render(request, 'new_shoop/delete.html', {'obj': comment})