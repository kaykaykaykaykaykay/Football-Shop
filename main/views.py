from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.models import Product
from main.forms import ProductForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import time

# Simple in-memory cache to track recent requests
recent_requests = {}

@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.all()
    context = {
        "app_name": "FootBaller",
        "name": "Khayru Rafa Kartajaya",
        "class": "PBP KKI",
        "products": products,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("main:show_main")
    return render(request, "create_product.html", {"form": form})

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})

def show_xml(request):
    data = Product.objects.all()
    xml_data = serializers.serialize("xml", data)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'content': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'price': product.price,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'is_featured': product.is_featured,
            'user_id': product.id,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    xml_data = serializers.serialize("xml", data)
    if not data.exists():
        return HttpResponse(status=404)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json_by_id(request, id):
    try:
        product = Product.objects.get(pk=id)
        json_data = serializers.serialize("json", [product])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
@require_http_methods(["POST"])
def ajax_logout(request):
    try:
        logout(request)
        response = JsonResponse({
            'success': True, 
            'message': 'Logged out successfully!',
            'redirect_url': reverse('main:login')
        })
        response.delete_cookie('last_login')
        return response
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred during logout'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def ajax_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return JsonResponse({
                'success': False, 
                'error': 'Username and password are required'
            }, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            response = JsonResponse({
                'success': True, 
                'redirect_url': reverse('main:show_main')
            })
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({
                'success': False, 
                'error': 'Invalid username or password'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred during login'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def ajax_register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password1 = data.get('password1', '')
        password2 = data.get('password2', '')
        
        # Validation
        if not username or not password1 or not password2:
            return JsonResponse({
                'success': False, 
                'error': 'All fields are required'
            }, status=400)
        
        if len(username) < 3:
            return JsonResponse({
                'success': False, 
                'error': 'Username must be at least 3 characters long'
            }, status=400)
        
        if password1 != password2:
            return JsonResponse({
                'success': False, 
                'error': 'Passwords do not match'
            }, status=400)
        
        if len(password1) < 8:
            return JsonResponse({
                'success': False, 
                'error': 'Password must be at least 8 characters long'
            }, status=400)
        
        # Check if username already exists
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False, 
                'error': 'Username already exists'
            }, status=400)
        
        # Create user
        user = User.objects.create_user(username=username, password=password1)
        
        return JsonResponse({
            'success': True, 
            'message': 'Account created successfully!',
            'redirect_url': reverse('main:login')
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred during registration'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def ajax_create_product(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        price = data.get('price')
        category = data.get('category', '').strip()
        thumbnail = data.get('thumbnail', '').strip()
        is_featured = data.get('is_featured', False)
        request_id = data.get('request_id')
        
        # Log the request for debugging
        print(f"Creating product: {name} (Request ID: {request_id})")
        
        # Check for duplicate requests within 5 seconds
        current_time = time.time()
        request_key = f"{name}_{description}_{request_id}"
        
        if request_key in recent_requests:
            time_diff = current_time - recent_requests[request_key]
            if time_diff < 5:  # 5 seconds
                print(f"Duplicate request blocked: {request_key}")
                return JsonResponse({
                    'success': False, 
                    'error': 'Duplicate request detected. Please wait a moment and try again.'
                }, status=400)
        
        # Store this request
        recent_requests[request_key] = current_time
        
        # Clean old requests (older than 10 seconds)
        for key in list(recent_requests.keys()):
            if current_time - recent_requests[key] > 10:
                del recent_requests[key]
        
        # Validation
        if not name or not description or not price or not category:
            return JsonResponse({
                'success': False, 
                'error': 'Name, description, price, and category are required'
            }, status=400)
        
        if not isinstance(price, (int, float)) or price < 0:
            return JsonResponse({
                'success': False, 
                'error': 'Price must be a positive number'
            }, status=400)
        
        # Check for potential duplicates (same name and description)
        existing_product = Product.objects.filter(
            name__iexact=name, 
            description__iexact=description
        ).first()
        
        if existing_product:
            return JsonResponse({
                'success': False, 
                'error': 'A product with this name and description already exists'
            }, status=400)
        
        # Create product
        product = Product.objects.create(
            name=name,
            description=description,
            price=int(price),
            category=category,
            thumbnail=thumbnail if thumbnail else '',
            is_featured=is_featured
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Product created successfully!',
            'product_id': str(product.id)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred during product creation'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def ajax_edit_product(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        price = data.get('price')
        category = data.get('category', '').strip()
        thumbnail = data.get('thumbnail', '').strip()
        is_featured = data.get('is_featured', False)
        
        # Validation
        if not name or not description or not price or not category:
            return JsonResponse({
                'success': False, 
                'error': 'Name, description, price, and category are required'
            }, status=400)
        
        if not isinstance(price, (int, float)) or price < 0:
            return JsonResponse({
                'success': False, 
                'error': 'Price must be a positive number'
            }, status=400)
        
        # Update product
        product.name = name
        product.description = description
        product.price = int(price)
        product.category = category
        product.thumbnail = thumbnail if thumbnail else ''
        product.is_featured = is_featured
        product.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Product updated successfully!',
            'product_id': str(product.id)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred during product update'
        }, status=500)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_product', id=id)

    context = {'form': form}

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_http_methods(["POST"])
def ajax_delete_product(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        product_name = product.name
        product.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Product "{product_name}" deleted successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred during product deletion'
        }, status=500)
