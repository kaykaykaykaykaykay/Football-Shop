from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.models import Product
from main.forms import ProductForm

def show_main(request):
    products = Product.objects.all()
    context = {
        "app_name": "FootBaller",
        "name": "Khayru Rafa Kartajaya",
        "class": "PBP KKI",
        "products": products,
    }
    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("main:show_main")
    return render(request, "create_product.html", {"form": form})

def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})

def show_xml(request):
    data = Product.objects.all()
    xml_data = serializers.serialize("xml", data)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    json_data = serializers.serialize("json", data)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    xml_data = serializers.serialize("xml", data)
    if not data.exists():
        return HttpResponse(status=404)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json_by_id(request, id):
    try:
        obj = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    json_data = serializers.serialize("json", [obj])
    return HttpResponse(json_data, content_type="application/json")