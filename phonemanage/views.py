from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required,permission_required
from django.forms.models import model_to_dict
from .models import PhoneInfo
from django.shortcuts import render
import openpyxl




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
        identity = data.get("manhansu","")
        dateofbirth = data.get("ngaysinh","")
        position = data.get("chucdanh","")
        department = data.get("tenphongban","")
        phonenumber = data.get("sodienthoai","")
        email = data.get("Email","")
        phonenumber=PhoneInfo(fullname=name,identity=identity, date_of_birth=dateofbirth,email=email,department=department,position=position,phone_number= phonenumber)
        phonenumber.save()
        return redirect('listcontact')
        
def edit_contact(request, pk):
    contact = get_object_or_404(PhoneInfo, pk=pk)
    
    if request.method == "POST":
        data = request.POST
        contact.fullname = data.get("hovaten","")
        contact.identity = data.get("manhansu","")
        contact.dateofbirth = data.get("ngaysinh","")
        contact.position = data.get("chucdanh","")
        contact.department = data.get("tenphongban","")
        contact.phone_number = data.get("sodienthoai","")
        contact.email = data.get("Email","")
        contact.save()

   
        return redirect('listcontact')
    # else:
        # print(model_to_dict(contact))
        # form = create_contact(model_to_dict(contact))

    context = {"contact": model_to_dict(contact)}
    return render(request, "list_contact/edit_contact.html", context=context)

def show_contact(request, pk):
    contact = get_object_or_404(PhoneInfo, pk=pk)
    context = {"contact": contact}
    return render(request, "list_contact/show_contact.html", context=context)

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


def impo(request):
    if "GET" == request.method:
        return render(request, 'list_contact/import.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        list_headers = excel_data[0]
        index_headers = { j: i for i, j in enumerate(list_headers)}
        for item in excel_data[1:]:
            department = item[index_headers['Department']]
            fullname = item[index_headers['Fullname']]
            dateofbirth = item[index_headers['Dateofbirth']]
            identity = item[index_headers['Identity']]
            email= item[index_headers['Email']]
            position= item[index_headers['Position']]
            phone_number=item[index_headers['Phonenumber']]

            phonenumber=PhoneInfo(fullname=fullname,identity=identity, date_of_birth=dateofbirth,email=email,department=department,position=position,phone_number= phone_number)
            phonenumber.save()

        return render(request, "list_contact/import.html", {"excel_data":excel_data})