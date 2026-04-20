from django.shortcuts import render, redirect
from .models import UserProfile, Car


# 💰 EMI FUNCTION
def calculate_emi(principal, annual_rate, months):
    r = annual_rate / (12 * 100)
    emi = (principal * r * (1 + r)**months) / ((1 + r)**months - 1)
    return round(emi, 2)


# 🏠 HOME VIEW
def home(request):
    if request.method == 'POST':
        user = request.user

        emi_required = True if request.POST.get('emi_required') else False

        # get form data
        name = request.POST.get('name')
        income = request.POST.get('income')
        family_size = request.POST.get('family_size')
        car_type = request.POST.get('car_type')
        location = request.POST.get('location')
        usage = request.POST.get('usage')

        # create/update profile
        profile, created = UserProfile.objects.get_or_create(user=user)

        profile.name = name
        profile.income = income
        profile.family_size = family_size
        profile.car_type = car_type
        profile.emi_required = emi_required
        profile.location = location
        profile.usage = usage
        profile.save()

        return redirect('suggestion')

    return render(request, 'carapp/home.html')


# 🚗 SUGGESTION VIEW
def suggestion(request):
    user = request.user

    try:
        profile = UserProfile.objects.get(user=user)

        # safe conversion
        income = int(profile.income) if profile.income else 0
        family_size = int(profile.family_size) if profile.family_size else 1

        # 🎯 GET ALL CARS
        cars = Car.objects.all()

        # =========================
        # 💰 PRICE FILTER
        # =========================
        if income < 500000:
            cars = cars.filter(price__lte=500000)
        elif income < 1000000:
            cars = cars.filter(price__lte=1000000)
        else:
            cars = cars.filter(price__lte=2000000)

        # =========================
        # 👨‍👩‍👧‍👦 FAMILY SIZE FILTER
        # =========================
        if family_size <= 4:
            cars = cars.filter(seating__gte=4)
        else:
            cars = cars.filter(seating__gte=family_size)

        # =========================
        # 🚗 CAR TYPE FILTER
        # =========================
        if profile.car_type and profile.car_type != "any":
            cars = cars.filter(car_type__iexact=profile.car_type)

        # =========================
        # 💬 MESSAGE + EMI
        # =========================
        emi_value = None

        if cars.exists():
            first_car = cars.first()

            # 💰 EMI only if user selected
            if profile.emi_required:
                loan_amount = first_car.price * 0.8   # 80% loan
                emi_value = calculate_emi(loan_amount, 10, 60)  # 10% interest, 5 years

            message = (
                f"Hello {profile.name}, {first_car.name} is perfect for you. "
                f"It fits your family size of {family_size}, "
                f"comes within your budget, and gives around {first_car.mileage} km/l mileage."
            )
        else:
            message = "❌ Sorry bro, no cars match your requirements. Try adjusting filters."

        # =========================
        # CONTEXT
        # =========================
        context = {
            'name': profile.name,
            'cars': cars,
            'message': message,
            'emi': emi_value
        }

        return render(request, 'carapp/suggestion.html', context)

    except UserProfile.DoesNotExist:
        return redirect('home')