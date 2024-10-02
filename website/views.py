from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record, Quarry, Material, Truck_no
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from datetime import datetime


def user_records(request):
    if request.user.is_superuser:
        return Record.objects.all()
    if request.user.is_authenticated:
        return Record.objects.filter(user=request.user)
    return None  

def home(request):
    if request.method == 'POST':
        # Handle login logic
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There was an error logging in. Please try again.")
            return redirect('home')

    else:
        records = user_records(request)  # Get records for logged-in user
        filter_query = request.GET.get('filter_query', '')
        start_date = request.GET.get('start_date')  # New date filter
        end_date = request.GET.get('end_date')      # New date filter
		
        if records:
            if filter_query:
                # Get the quarry, material, and truck names
                quarry_data = Quarry.objects.filter(name__exact=filter_query).first()  # Get the first matching object or None
                material_data = Material.objects.filter(name__exact=filter_query).first()
                truck_data = Truck_no.objects.filter(name__exact=filter_query).first()  # Note: Updated to 'Truck'

                # Construct the filter conditions
                filter_conditions = Q(challan_no__exact=filter_query)
                if material_data:
                    filter_conditions |= Q(material=material_data)
                if quarry_data:
                    filter_conditions |= Q(quarry=quarry_data)
                if truck_data:
                    filter_conditions |= Q(truck=truck_data)

                records = records.filter(filter_conditions)  # Use the constructed filter conditions
                
            if start_date and end_date:
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    records = records.filter(date__range=(start_date, end_date))
                except ValueError:
                    messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")

            return render(request, 'home.html', {'records': records, 'filter_query': filter_query, 'start_date': start_date, 'end_date': end_date})
        else:
            messages.error(request, "No records found or you are not logged in.")
            return render(request, 'home.html')


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})


@login_required(login_url='/')
def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')


@login_required(login_url='/')
def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


@login_required(login_url='/')
def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save(commit=False)
				add_record.user = request.user
				add_record.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

@login_required(login_url='/')
def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

@login_required(login_url='/')
def view_invoice(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    return render(request, 'invoice.html', {'record': record})