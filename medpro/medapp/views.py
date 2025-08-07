from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.models import User
from.models import *
from django.http import HttpResponse
from .forms import PharmacySignupForm,FeedbackForm,PaymentForm,MedicineForm,BookingForm
from django.contrib import messages
from medapp.models import PharmacyUser,Medicine

# def product(request):
#     products=Demo.objects.all()
#     return render(request,'home.html',{'products':products})
def homepage(request):
    return render(request,'index.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to authenticate a regular Django user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in as regular user.")
            return redirect('userhome')  # Change to your desired redirect

        # If not a regular user, try pharmacy user
        try:
            pharmacy_user = PharmacyUser.objects.get(username=username)
            if pharmacy_user.check_password(password):  # Only works if you've implemented check_password
                request.session['pharmacy_user_id'] = pharmacy_user.id
                messages.success(request, "Logged in as pharmacy user.")
                return redirect('pharmacyhome')  # Change to your desired redirect
            else:
                messages.error(request, "Invalid credentials.")
        except PharmacyUser.DoesNotExist:
            messages.error(request, "Invalid credentials.")

    return render(request,'login.html')



def signup_view(request):
    if request.method == "POST":
        # Use parentheses for the get method
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Create a new user
        User.objects.create_user(username=username, password=password,email=email)

        return redirect('login')  # Redirect to home or any other page after login
    
    return render(request, 'signup.html')

def homepage_user(request):
    medicine = Medicine.objects.all()  # fetch all cars
    return render(request, 'user_homepage.html',{'medicine':medicine})

def profile_view(request):
    return render(request,'profile.html')

def pharmacy_signup(request):
    if request.method == "POST":
        form = PharmacySignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to a dashboard after signup
    else:
        form = PharmacySignupForm()
    
    return render(request, 'pharmacy_signup.html', {'form': form})

def homepage_pharmacy(request):
    medicines = Medicine.objects.all()  # Fetch all medicines
    return render(request, 'pharmacy_homepage.html', {'medicines': medicines})

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'feedback.html', {'form': FeedbackForm(), 'success': True})
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Medicine, Payment, Booking
from .forms import PaymentForm, BookingForm

def payment_view(request, medicine_id):
    # Fetch the Medicine object based on the medicine_id
    medicine = get_object_or_404(Medicine, id=medicine_id)

    # Retrieve the quantity from the session (set earlier in cart or selection)
    quantity = request.session.get('medicine_quantity', 1)  # Default to 1 if no quantity is set
    total_cost = medicine.price * quantity  # Total cost = price * quantity

    # Handle the payment process (POST request)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Save the payment instance and associate the amount with the total cost
            payment = form.save(commit=False)
            payment.amount = total_cost  # Assign the calculated total cost
            payment.save()

            # Optionally clear session data after successful payment
            if 'medicine_quantity' in request.session:
                del request.session['medicine_quantity']

            return render(request, 'payment.html', {
                'form': PaymentForm(initial={'amount': total_cost}),
                'medicine': medicine,
                'total_cost': total_cost,
                'success': True
            })
    else:
        form = PaymentForm(initial={'amount': total_cost})

    return render(request, 'payment.html', {
        'form': form,
        'medicine': medicine,
        'total_cost': total_cost
    })


def booking(request, id):
    # Fetch the Medicine object based on the id
    medicine = get_object_or_404(Medicine, pk=id)

    # Handle the booking process (POST request)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save the booking instance
            booking = form.save(commit=False)
            booking.user = request.user  # Associate the current user with the booking
            booking.medicine = medicine  # Link the booking with the medicine
            booking.total_cost = booking.quantity * medicine.price  # Calculate the total cost
            booking.save()

            # Store the quantity in the session and redirect to the payment view
            request.session['medicine_quantity'] = booking.quantity
            return redirect('payment', medicine_id=medicine.id)  # Redirect to the payment page
    else:
        form = BookingForm()

    return render(request, 'book_medicine.html', {'form': form, 'medicine': medicine})


def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pharmacyhome')
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})


def payment_list(request):
    payments = Payment.objects.all().order_by('-paid_at')
    return render(request, 'payment_list.html', {'payments': payments})


def delete_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    medicine.delete()
    return redirect('pharmacyhome')  # Replace with your dashboard URL name



def about(request):
    return render(request,'about.html')

def logout_view(request):
    logout(request)
    return redirect('home') 


