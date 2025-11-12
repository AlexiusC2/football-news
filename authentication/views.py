from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({"status": False, "message": "Method not allowed."}, status=405)
    # Try JSON first, fallback to form
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body or "{}")
            username = data.get('username', '')
            password = data.get('password', '')
        else:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
    except json.JSONDecodeError:
        return JsonResponse({"status": False, "message": "Invalid JSON."}, status=400)

    user = authenticate(username=username, password=password)
    if user and user.is_active:
        auth_login(request, user)
        return JsonResponse({"username": user.username, "status": True, "message": "Login successful."}, status=200)
    return JsonResponse({"status": False, "message": "Invalid credentials."}, status=401)

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({"status": False, "message": "Method not allowed."}, status=405)
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": False, "message": "Invalid JSON."}, status=400)

    username = data.get('username', '').strip()
    password1 = data.get('password1', '')
    password2 = data.get('password2', '')

    if not username or not password1 or not password2:
        return JsonResponse({"status": False, "message": "Missing required fields."}, status=400)
    if password1 != password2:
        return JsonResponse({"status": False, "message": "Passwords do not match."}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": False, "message": "Username already exists."}, status=400)

    user = User.objects.create_user(username=username, password=password1)
    return JsonResponse({"username": user.username, "status": True, "message": "User created successfully."}, status=200)

@csrf_exempt
def logout(request):
    if request.method != 'POST':
        return JsonResponse({"status": False, "message": "Method not allowed."}, status=405)
    username = getattr(request.user, 'username', '')
    if request.user.is_authenticated:
        auth_logout(request)
        return JsonResponse({"username": username, "status": True, "message": "Logged out successfully."}, status=200)
    return JsonResponse({"status": False, "message": "Not authenticated."}, status=401)