from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .models import PhoneInfo


def user_login(request, method="POST"):
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = authenticate(email=email, password=password)

        if user is None:
            my_message = (
                "Your email address or password is incorrect. Please login again!"
            )
            messages.error(request, my_message)

            return render(request, "layouts/login.html")

        login(request, user)
        return HttpResponseRedirect("dashboard/")

    return render(request, "layouts/login.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def dashboard(request):
    return render(request, "dashboard/index.html")

    
def listcontact(request, method="GET"):
    phonenumber=PhoneInfo.objects.all
    return render(request, "list_contact/listcontact.html", {"phonenumber": phonenumber})

def create_contact (request):
    if request.method == "GET":
        return render(request,"list_contact/create_contact.html")
    elif request.method == "POST":
        data = request.POST
        name = data.get("hovaten","")
        position = data.get("chucdanh","")
        department = data.get("tenphongban","")
        phonenumber = data.get("sodienthoai","")
        email = data.get("Email","")
        phonenumber=PhoneInfo(fullname=name,email=email,department=department,position=position,phone_number= phonenumber)
        phonenumber.save()
        return redirect('listcontact')
        
def edit_contact(request, pk):
    contact = get_object_or_404(PhoneInfo, pk=pk)
    
    if request.method == "POST":
        data = request.POST
        contact.name = data.get("hovaten","")
        contact.position = data.get("chucdanh","")
        contact.department = data.get("tenphongban","")
        contact.phonenumber = data.get("sodienthoai","")
        contact.email = data.get("Email","")
        contact.save()

        messages.success(request, "Create contact successful")
        return redirect('listcontact')
    # else:
        # print(model_to_dict(contact))
        # form = create_contact(model_to_dict(contact))

    context = {"contact": model_to_dict(contact)}
    return render(request, "list_contact/edit_contact.html", context=context)

def delete_contact(request, pk):
    contact = get_object_or_404(PhoneInfo,pk=pk)
    # if request.method == "POST":
    #     data = request.POST
    #     contact.name = data.get("hovaten","")
    #     contact.position = data.get("chucdanh","")
    #     contact.department = data.get("tenphongban","")
    #     contact.phonenumber = data.get("sodienthoai","")
    #     contact.email = data.get("Email","")
    contact.delete()
       

    messages.success(request, "Delete contact successful")
  
    return redirect('listcontact')
