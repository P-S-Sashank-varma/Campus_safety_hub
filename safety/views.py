from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import vonage
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login


def home(request):
    return render(request, 'home.html')

from django.contrib import messages

# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
def signup(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        gender = request.POST['gender']
        student_type = request.POST['student_type']
        room_no = request.POST.get('room_no', '')
        bus_no = request.POST.get('bus_no', '')
        college = request.POST['college']
        terms = request.POST.get('terms')

        # Check if the user agreed to the terms
        if not terms:
            messages.error(request, "You must accept the terms and conditions.")
            return render(request, 'signup.html')

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "User with this email already exists.")
        else:
            # Create the user
            user = User.objects.create_user(username=email, email=email, password='password')  # Set a default password
            user.first_name = full_name
            user.save()

        
            # Show success message and redirect
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')  # Redirect to the login page

    # Render the signup page with any messages
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('main')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    
    # Redirect back to the signup page (where login form is located) with error messages
    return redirect('signup')


def main(request):
    return render(request, 'main.html')
import requests
import json
import requests

@csrf_exempt

def sos_action(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Hardcoded values
            username = "P S Sashank Varma"
            email = "sashankvarma920@gmail.com"
            latitude = "12.9716"  # Example latitude
            longitude = "77.5946" # Example longitude
            college_name = "ACET" # Example college name
            gender = "male"  # Example gender

            # Debugging the received data
            print("Received Data:", data)

            # Ensure all required fields are correctly set
            if not username:
                return JsonResponse({'status': 'error', 'message': 'Username is required'})
            if not email:
                return JsonResponse({'status': 'error', 'message': 'Email is required'})
            if not latitude:
                return JsonResponse({'status': 'error', 'message': 'Latitude is required'})
            if not longitude:
                return JsonResponse({'status': 'error', 'message': 'Longitude is required'})
            if not college_name:
                return JsonResponse({'status': 'error', 'message': 'College name is required'})
            if gender not in ['male', 'female', 'other']:
                return JsonResponse({'status': 'error', 'message': 'Invalid gender value'})

            # Vonage API credentials
            api_key = '9ad697f3'  # Replace with your actual Vonage API Key
            api_secret = 'qRq8T4PYTZgwbdE7'  # Replace with your actual Vonage API Secret

            # Initialize the Vonage client
            client = vonage.Client(key=api_key, secret=api_secret)
            sms = vonage.Sms(client)

            # Prepare SMS data with better formatting
            message = (
                f"SOS Alert!\n"
                f"Username: {username}\n"
                f"Email: {email}\n"
                f"Latitude: {latitude}\n"
                f"Longitude: {longitude}\n"
                f"College: {college_name}\n"
                f"Gender: {gender}"
            )
            sms_data = {
                'from': 'VonageAPI',  # Replace with a valid sender ID if required
                'to': '+919493271558',   # Replace with the recipient's phone number
                'text': message,
            }

            # Send the SMS
            response = sms.send_message(sms_data)
            result = response['messages'][0]

            if result['status'] == '0':
                return JsonResponse({'status': 'success', 'message': 'SMS sent successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': result['error-text']})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
