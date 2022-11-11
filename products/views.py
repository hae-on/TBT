from django.shortcuts import render, redirect, get_object_or_404
from .form import ProductsFrom
from .models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "products/index.html", context)


def products_create(request):
    if request.method == "POST":
        create_form = ProductsFrom(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect("products:index")

    else:
        create_form = ProductsFrom()

    context = {
        "create_form": create_form,
    }

    return render(request, "products/products_create.html", context)


def products_detail(request, products_pk):
    products = get_object_or_404(Product, pk=products_pk)

    context = {
        "products": products,
    }

    return render(request, "products/products_detail.html", context)


def products_update(request, products_pk):
    products = get_object_or_404(Product, pk=products_pk)
    if request.method == "POST":
        form = ProductsFrom(request.POST, request.FILES, instance=products)
        if form.is_valid():
            form.save()
            return redirect("products:products_detail", products_pk)

    else:
        form = ProductsFrom(instance=products)

    context = {
        "form": form,
    }

    return render(request, "products/products_update.html", context)


def products_delete(request, products_pk):

    products = get_object_or_404(Product, pk=products_pk)
    products.delete()
    return redirect("products:index")


@login_required
def like(request, products_pk):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=products_pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
            is_liked = False
        else:
            product.like_users.add(request.user)
            is_liked = True
    else:
        return redirect("products:detail", products_pk)
    return JsonResponse(
        {
            "is_liked": is_liked,
            "like_count": product.like_users.count(),
        }
    )
