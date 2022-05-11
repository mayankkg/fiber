from email.message import EmailMessage
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from activity.models import *
import datetime
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from random import randint

#html email required stuff
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required(login_url="/login")
def view_activity(request):
    if request.method == "GET":
        get_id = request.GET.get("id", "off")
        if get_id != 'off':
            viewdata = Activity.objects.filter(id=get_id)[0]
            params = {'viewdata': viewdata}
            return render(request, 'view_activity.html', params)
        else:
            return redirect('activity_list')