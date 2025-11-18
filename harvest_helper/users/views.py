# users/views.py
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('email') # Using email as username
        password = data.get('password')
        full_name = data.get('name')

        if not username or not password:
            return JsonResponse({'error': 'Email and password are required.'}, status=400)
        
        try:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'An account with this email already exists.'}, status=400)
            
            user = User.objects.create_user(username=username, email=username, password=password)
            user.first_name = full_name
            user.save()
            
            # Log the user in immediately
            login(request, user)
            return JsonResponse({'message': 'Registration successful!', 'user': user.email})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Use for testing
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('email') # Using email as username
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful!', 'user': user.email})
        else:
            return JsonResponse({'error': 'Invalid credentials. Please try again.'}, status=401)
 # Use for testing
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful!'})