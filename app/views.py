from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Brand
from .serializers import ProductSerializer, BrandSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def index(request):
    return render(request, 'index.html')

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_products(request):
    if request.method == 'GET':
        products = Product.objects.filter(brand__owner=request.user)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    
    
    elif request.method == 'POST':
        name = request.data.get('name')
        price = request.data.get('price')
        stock = request.data.get('stock')
        description = request.data.get('description')
        category = request.data.get('category')
        brand_id = request.data.get('brand')
        picture1 = request.FILES.get('picture1')
        picture2 = request.FILES.get('picture2')
        picture3 = request.FILES.get('picture3')
        
        brand = Brand.objects.get(id=brand_id)
        
        product = Product(name=name, price=price, stock=stock,description=description,category=category, brand=brand, picture1=picture1, picture2=picture2,picture3=picture3)
        product.save()
        return JsonResponse({"message": "Product created successfully"}, status=201)
    
    
    
        

@api_view(['GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        if product.brand.owner != request.user:
            raise PermissionDenied("You cannot update this product.")
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        category = request.POST.get('category')
        brand_id = request.POST.get('brand')
        picture1 = request.FILES.get('picture1')
        picture2 = request.FILES.get('picture2')
        picture3 = request.FILES.get('picture3')
        brand = Brand.objects.get(id=brand_id)
        
        if name:
            product.name = name
        if price:
            product.price = price
        if stock:
            product.stock = stock
        if description:
            product.description = description
        if category:
            product.category = category
        if brand:
            product.brand = brand
        if picture1:
            product.picture1 = picture1
        if picture2:
            product.picture2 = picture2
        if picture3:
            product.name = picture3
        
        product.save()
        
        return JsonResponse({"message":"success"}, status=200)
    
    elif request.method == 'DELETE':
        if product.brand.owner != request.user:
            raise PermissionDenied("You cannot delete this product.")
        product.delete()
        return JsonResponse({"message":"success"},status=204)

@csrf_exempt
def product_detail(request, id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, context={'request': request})
        return JsonResponse(serializer.data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_brands(request):
    if request.method == 'GET':
        brands = Brand.objects.filter(owner=request.user)
        serializer = BrandSerializer(brands, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        name = request.data.get('name')
        logo = request.FILES.get('logo')
        brand = Brand(name=name,owner=request.user,logo=logo)
        brand.save()
        return JsonResponse({"message": "Product created successfully"}, status=201)

@api_view(['GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_brand(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    
    if request.method == 'GET':
        if brand.owner != request.user:
            raise PermissionDenied("You cannot access this brand.")
        serializer = BrandSerializer(brand, context={'request': request})
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        if brand.owner != request.user:
            raise PermissionDenied("You cannot update this brand.")
        
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        
        if name:
            brand.name = name
        if logo:
            brand.logo = logo
        
        brand.save()
        
        return JsonResponse({"message":"success"}, status=200)
    
        
    
    
    elif request.method == 'DELETE':
        if brand.owner != request.user:
            raise PermissionDenied("You cannot delete this brand.")
        brand.delete()
        return JsonResponse(status=204)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        email = body.get('email')
        password = body.get('password')
        confirmPassword = body.get('confirmPassword')
        if password == confirmPassword:
            

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already in use.'}, status=400)

            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            token, created = Token.objects.get_or_create(user=user)

            return JsonResponse({'success': 'User created successfully.'}, status=201)
        else:
            return JsonResponse({'error': 'Password mismatch.'}, status=400)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_auth_status(request):
    return JsonResponse({'success': 'Auth successful.'}, status=200)
    
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        email = body.get('email')
        password = body.get('password')

        

        user = authenticate(request=request, username=email, password=password)

        if user is not None:
            auth.login(request, user)

            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'success': 'Login successful.', 'token': token.key}, status=200)
        else:
            
            return JsonResponse({'error': 'Invalid credentials.'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        token = Token.objects.get(user=request.user)
        token.delete()
        return JsonResponse({'success': 'Logged out successfully.'}, status=200)
