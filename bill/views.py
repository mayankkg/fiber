from email.message import EmailMessage
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bill.models import *
import datetime
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from .forms import BillForm

#html email required stuff
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@login_required(login_url="/login")
def create_bill(request):
    edit_data={}
    msg=""
    form = BillForm(request.POST or None)
    activity_id = request.GET.get("id")  
    if activity_id:
        edit_data = Activity.objects.filter(id=activity_id)
        bill_data = Bill.objects.filter(activity=activity_id)
        if edit_data:
            edit_data = edit_data[0]
            if edit_data.appr_footage == None:
                appr_footage = 0
            else:
                appr_footage = edit_data.appr_footage
            if edit_data.assign_fielder == None:
                ass_fielder = 0
            else:
                ass_fielder = edit_data.assign_fielder.id 
            if bill_data:
                bill_data = bill_data[0]
                form = BillForm(initial={'fielder_name':ass_fielder, 'app_footage':appr_footage, 'activity_id':activity_id, 'added_by_id':request.user.id},instance = bill_data)
            else:
                form = BillForm(initial={'fielder_name':ass_fielder, 'app_footage':appr_footage, 'activity_id':activity_id, 'added_by_id':request.user.id})
    else:
        edit_data={}
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            assigned_fielder = form.cleaned_data.get("fielder_name")
            app_footage = form.cleaned_data.get("app_footage")
            activity_id = request.POST.get("activity_id")
            added_by_id = request.POST.get("added_by_id")
            exist_check = Bill.objects.filter(activity_id=activity_id)
            if exist_check:
                update_form = BillForm(request.POST, instance=exist_check[0])
                update_form.save()
                Bill.objects.filter(id=exist_check[0].id).update(activity=activity_id, added_by=added_by_id)
                Activity.objects.filter(id=activity_id).update(assign_fielder=assigned_fielder, appr_footage=app_footage)
                messages.success(request, " Your bill has been updated successfully")
                return redirect('billview')
            else:
                form.save()
                bill_id = Bill.objects.latest('id').id
                Bill.objects.filter(id=bill_id).update(activity=activity_id, added_by=added_by_id)
                Activity.objects.filter(id=activity_id).update(assign_fielder=assigned_fielder, appr_footage=app_footage)
                messages.success(request, " Your bill has been added successfully")
                return redirect('billview')
        
    context = {"form": form, 'activity_data':edit_data}
    html_template = loader.get_template('create_bill.html')
    return HttpResponse(html_template.render(context, request))