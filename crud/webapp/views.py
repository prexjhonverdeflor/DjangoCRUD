from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm, BICSetupForm, MCRegisterForm, PesoNetForm, EditUserProfileForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import  Record, BICSetup, MCRegister, PesoNet, UserProfile
from django.contrib.auth import update_session_auth_hash

from .forms import EditUserProfileForm, EditUserPasswordForm
 
from django.contrib import messages
from django.contrib.auth.models import User



#Homepage 
def home(request):
    return render(request, 'webapp/index.html')


# Register
@login_required(login_url='my-login')
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            user_type = form.cleaned_data.get('user_type')
            branch_type = form.cleaned_data.get('branch_type')
            
            if user_type == 'admin':
                user.is_staff = True
                branch_type = None 
            else:
                user.is_staff = False
            
            user.save()  
            
            # Create the related UserProfile
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                branch_type=branch_type
            )
            
            messages.success(request, "Account created successfully!")
            return redirect("dashboard")
    else:
        form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'webapp/register.html', context)



# Login
def my_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect("dashboard")
                else:
                    return redirect("mc_register")
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'webapp/my-login.html', context=context)






#Admin 
#user list
@login_required(login_url='my-login')
def user_list(request):
    # Make sure the logged-in user is an admin
    if not request.user.is_staff:
        # Redirect to some appropriate page or raise a 403 Forbidden error
        return redirect("dashboard")  # Redirect to dashboard for example

    # Exclude the superuser account
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'webapp/user_list.html', {'users': users})



#edit user
@login_required(login_url='my-login')
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = user.profile

    if request.method == "POST":
        profile_form = EditUserProfileForm(request.POST, instance=user_profile)
        password_form = EditUserPasswordForm(user, request.POST)  # Use custom form

        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()

            new_password = password_form.cleaned_data.get('new_password1')
            if new_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Update session to prevent logout

            messages.success(request, "User profile updated successfully!")
            return redirect("user-list")
    else:
        profile_form = EditUserProfileForm(instance=user_profile)
        password_form = EditUserPasswordForm(user)  # Use custom form

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'user': user,
    }
    return render(request, 'webapp/edit-user.html', context)





@login_required(login_url='my-login')
def admin_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    branch_type = user_profile.branch_type

    # Retrieve all records without filtering by branch_type
    all_records = Record.objects.all()

    context = {
        'branch_type': branch_type,
        'records': all_records,
    }

    return render(request, 'webapp/admin/branch/dashboard.html', context)


# Dashboard ADD RECORD
@login_required(login_url='my-login')
def add_record(request):

    user_profile = UserProfile.objects.get(user=request.user)
    form = CreateRecordForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        new_record = form.save(commit=False)
        new_record.branch = user_profile.branch_type 
        new_record.save()
        
        messages.success(request, "Your record was created!")
        return redirect("dashboard")
    
    context = {'form': form}
    return render(request, 'webapp/admin/branch/create-record.html', context)


#Admin EDIT
@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect("dashboard")
    context = {'form':form}
    return render(request, 'webapp/admin/branch/update-record.html', context=context)


#Admin Delete
@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Your record was deleted!")
    return redirect("dashboard")


# BIC SETUP
@login_required(login_url='my-login')
def bic_setup(request):
    user_profile = UserProfile.objects.get(user=request.user)
    branch_type = user_profile.branch_type

    # Retrieve all BICSetup records without filtering by branch_type
    all_bic_setups = BICSetup.objects.all()

    context = {
        'branch_type': branch_type,
        'bic_setups': all_bic_setups,
    }

    return render(request, 'webapp/admin/bic/bic_setup.html', context)


@login_required(login_url='my-login')
def bic_setup_create(request):
    
    user_profile = UserProfile.objects.get(user=request.user)
    form = BICSetupForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        new_record = form.save(commit=False)
        new_record.branch = user_profile.branch_type 
        new_record.save()
        
        messages.success(request, "Your record was created!")
        return redirect("bic_setup")
    
    context = {'form': form}
    return render(request, 'webapp/admin/bic/bic_setup_create.html', context)

@login_required(login_url='my-login')
def bic_setup_update(request, bic_setup_id):
    bic_setup = BICSetup.objects.get(pk=bic_setup_id)
    if request.method == 'POST':
        form = BICSetupForm(request.POST, instance=bic_setup)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('bic_setup')
    else:
        form = BICSetupForm(instance=bic_setup)
        
    return render(request, 'webapp/admin/bic/bic_setup_update.html', {'form': form})


@login_required(login_url='my-login')
def bic_setup_delete(request, pk):

    bic_setup = BICSetup.objects.get(id=pk)
    bic_setup.delete()
    messages.success(request, "Your record was deleted!")
    return redirect('bic_setup')











# Cashier Dashboard
@login_required(login_url='my-login')
def cashier_dashboard(request):

    user_profile = UserProfile.objects.get(user=request.user)
    branch_type = user_profile.branch_type

    filtered_records = MCRegister.objects.filter(branch=branch_type) 

    context = {
        'branch_type': branch_type,
        'mc_registers': filtered_records,
    }

    return render(request, 'webapp/cashier/mcregister/cashier.html', context=context)


#cashier add
@login_required(login_url='my-login')
def mc_register_create(request):
    user_profile = UserProfile.objects.get(user=request.user)
    form = MCRegisterForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        new_record = form.save(commit=False)
        new_record.branch = user_profile.branch_type 
        new_record.save()
        
        messages.success(request, "Your record was created!")
        return redirect("mc_register")
    
    context = {'form': form}
    return render(request, 'webapp/cashier/mcregister/mc_create.html', {'form': form})


#edit
@login_required(login_url='my-login')
def mc_register_update(request, mc_register_id):
    mc_register = MCRegister.objects.get(pk=mc_register_id)
    if request.method == 'POST':
        form = MCRegisterForm(request.POST, instance=mc_register)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('mc_register')
    else:
        form = MCRegisterForm(instance=mc_register)
        
    return render(request, 'webapp/cashier/mcregister/mc_update.html', {'form': form})








#PESONET
@login_required(login_url='my-login')
def peso_net(request):

    user_profile = UserProfile.objects.get(user=request.user)
    branch_type = user_profile.branch_type

    filtered_records = PesoNet.objects.filter(branch=branch_type) 

    context = {
        'branch_type': branch_type,
        'peso_nets': filtered_records,
    }

    return render(request, 'webapp/cashier/pesonet/peso_net.html', context=context)


@login_required(login_url='my-login')
def peso_create(request):

    user_profile = UserProfile.objects.get(user=request.user)
    form = PesoNetForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        new_record = form.save(commit=False)
        new_record.branch = user_profile.branch_type
        new_record.save()
        
        messages.success(request, "Your record was created!")
        return redirect("peso_net")
    
    context = {'form': form}
    return render(request, 'webapp/cashier/pesonet/peso_create.html', {'form': form})

#edit
@login_required(login_url='my-login')
def peso_update(request, peso_net_id):
    peso_net = PesoNet.objects.get(pk=peso_net_id)
    if request.method == 'POST':
        form = PesoNetForm(request.POST, instance=peso_net)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('peso_net')
    else:
        form = PesoNetForm(instance=peso_net)
        
    return render(request, 'webapp/cashier/pesonet/peso_update.html', {'form': form})




#logout
def user_logout(request):
    auth.logout(request)
    messages.success(request, "Logout success!")
    return redirect("my-login")




