from activity.views.import_data import *
from activity.views.page_permission import *

def send_mail(mydata, page, subject):
    mail_setting = Mail_settings.objects.get(priority=2)
    html_content = render_to_string("email/"+page, mydata)
    text_content = strip_tags(html_content)
    if page == 'reset_password.html':
        receiver = [mydata['email']]
    else:
        receiver = [mydata['email'],'amit@integertel.com']
    email = EmailMultiAlternatives(
        # subject
        subject,
        # msg
        text_content,
        # from email
        mail_setting,
        # recipient list
        receiver
    )
    email.attach_alternative(html_content,"text/html")
    email.send()

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def index(request):
    return redirect('handleLogin')

rec=0
def autoIncrement(digit,st_f):
    global rec
    pStart = st_f+1 #adjust start value, if req'd 
    pInterval = 1 #adjust interval value, if req'd
    if (rec == 0): 
        rec = pStart 
    else: 
        rec = rec + pInterval 
    return str(rec).zfill(digit)

    
def Enquiry(lis1):
    if len(lis1) == 0:
        return 0
    else:
        return 1

@login_required(login_url="/login")
def create_activity(request):
    current_url = resolve(request.path_info).url_name
    user_id = request.user.id
    page_check = permision_check(current_url,user_id)
    if page_check == False:
        return render(request,'404.html')
    ##driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.implicitly_wait(30)
    #driver.get('http://127.0.0.1:8000/create_activity')
    activity_id = request.GET.get("id")
    edit_recdate=None
    #edit_ecd=None
    if activity_id:
        edit_data = Activity.objects.get(id=activity_id)
        edit_recdate = datetime.datetime.strptime(str(edit_data.rec_date), '%Y-%m-%d').strftime('%m-%d-%Y')
        
        if edit_data.ecd!=None:
            edit_ecd = datetime.datetime.strptime(str(edit_data.ecd), '%Y-%m-%d').strftime('%m-%d-%Y')
        #select = Select(driver.find_element(By.ID,'Client'))
        

        # select by value 
        #select.select_by_value('2')
    else:
        edit_data={}
    activities_list = Activities.objects.all()
    clients_list = Clients.objects.order_by('name')
    bay_role = Bay_roles.objects.get(id=10)
    feusers_list = Bay_users.objects.filter(role=bay_role, is_active=True).order_by('fname')
    bayusers_list = Bay_users.objects.filter(is_active=True).order_by('fname')
    
    if request.method == "POST":
        
        activity_data = Activity.objects.first()
        if activity_data:
            act_id = Activity.objects.latest('id').id
        else:
            act_id = 0
        str1 = autoIncrement(4,act_id)
        today = date.today()
        todate = today.strftime("%d%m%Y")
        ticket_no = todate+"-"+str1
        formedit = request.POST.get("form_edit_id")
        client_ticket = request.POST.get("client_ticket")
        rec_date = request.POST.get("rec_date")
        rec_date = datetime.datetime.strptime(rec_date, '%m-%d-%Y').strftime('%Y-%m-%d')
        ecd = request.POST.get("ecd")
        if ecd:
            ecd = datetime.datetime.strptime(ecd, '%m-%d-%Y').strftime('%Y-%m-%d')
        else:
            ecd = None
        revised_ecd = request.POST.get("revised_ecd")
        if revised_ecd:
            revised_ecd = datetime.datetime.strptime(revised_ecd, '%m-%d-%Y').strftime('%Y-%m-%d')
        else:
            revised_ecd = None
        client_id = request.POST.get("client")
        client = Clients.objects.get(id=client_id)
        market = request.POST.get("market")
        ewo = request.POST.get("ewo")
        da = request.POST.get("da")
        lus = request.POST.get("lus")
        wire_center = request.POST.get("wire_center")
        pfp = request.POST.get("pfp")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        job_type = request.POST.get("job_type")
        job_no = request.POST.get("job_no")
        f1cfas = request.POST.get("f1cfas")
        f1job_no = request.POST.get("f1job_no")
        f1_sow = request.POST.get("f1_sow")
        f2cfas = request.POST.get("f2cfas")
        f2job_no = request.POST.get("f2job_no")
        f2_sow = request.POST.get("f2_sow")
        notes = request.POST.get("notes")
        activitylist = request.POST.getlist("activity")
        
        assign_fielder = request.POST.get("assign_fielder")
        try:
            assign_fielder = Bay_users.objects.get(id=assign_fielder)
        except Bay_users.DoesNotExist:
            assign_fielder = None        
        assign_int_eng = request.POST.get("assign_int_eng")
        try:
            assign_int_eng = Bay_users.objects.get(id=assign_int_eng)
        except Bay_users.DoesNotExist:
            assign_int_eng = None 
        
        int_eng2 = request.POST.get("int_eng2")
        try:
            int_eng2 = Bay_users.objects.get(id=int_eng2)
        except Bay_users.DoesNotExist:
            int_eng2 = None
       
        lead_eng = request.POST.get("lead_eng")
        try:
            lead_eng = Bay_users.objects.get(id=lead_eng)
        except Bay_users.DoesNotExist:
            lead_eng = None
        
        work_print = request.POST.get("work_print")
        footage = request.POST.get("footage")
        appr_footage = request.POST.get("appr_footage")
        terminal = request.POST.get("terminal")
        added_by = request.POST.get("added_by")
        added_by = Bay_users.objects.get(id=added_by)
        added_date = request.POST.get("added_date")
        fielding_start_date = request.POST.get("fielding_start_date")
        if fielding_start_date:
            fielding_start_date = datetime.datetime.strptime(fielding_start_date, '%m-%d-%Y').strftime('%Y-%m-%d')
        else:
            fielding_start_date = None
        
        fielder_ecd = request.POST.get("fielder_ecd")
        if fielder_ecd:
            fielder_ecd = datetime.datetime.strptime(fielder_ecd, '%m-%d-%Y').strftime('%Y-%m-%d')
        else:
            fielder_ecd = None
        #file_name = request.FILES.get("build_package1")
        
        if rec_date != '':
            activity_data = Activity(ticket=ticket_no, client_ticket=client_ticket,rec_date=rec_date, ecd=ecd, revised_ecd=revised_ecd, client_id=client, market=market, ewo=ewo, da=da, lus=lus, wire_center=wire_center, pfp=pfp, latitude=latitude, longitude=longitude, job_type=job_type, job_no=job_no, f1cfas=f1cfas, f1job_no=f1job_no, f1_sow=f1_sow, f2cfas=f2cfas, f2job_no=f2job_no, f2_sow=f2_sow, notes=notes, assign_fielder=assign_fielder, assign_int_eng=assign_int_eng, int_eng2=int_eng2, lead_eng=lead_eng, work_print=work_print, footage=footage, appr_footage=appr_footage, terminal=terminal, added_by=added_by, added_date=added_date, fielding_start_date=fielding_start_date, fielder_ecd=fielder_ecd)
            if formedit != '':
                if Enquiry(activitylist):
                    Activity.objects.filter(id=formedit).update(client_ticket=client_ticket, rec_date=rec_date, ecd=ecd, revised_ecd=revised_ecd, client_id=client, market=market, ewo=ewo, da=da, lus=lus, wire_center=wire_center, pfp=pfp, latitude=latitude, longitude=longitude, job_type=job_type, job_no=job_no, f1cfas=f1cfas, f1job_no=f1job_no, f1_sow=f1_sow, f2cfas=f2cfas, f2job_no=f2job_no, f2_sow=f2_sow, notes=notes, assign_fielder=assign_fielder, assign_int_eng=assign_int_eng, int_eng2=int_eng2, lead_eng=lead_eng, work_print=work_print, footage=footage, appr_footage=appr_footage, terminal=terminal, fielding_start_date=fielding_start_date, fielder_ecd=fielder_ecd)
                    u = Activity.objects.get(pk=formedit)
                    u.activity.clear()
                    u.activity.add(*activitylist)
                    messages.success(request, " Your activity has been updated successfully")
                    return redirect('activity_list')
                else:
                    edit_recdate = request.POST.get("rec_date")
                    edit_ecd = request.POST.get("ecd")
                    edit_data = activity_data
                    #print(edit_data)
                    #params = {'edit_data':edit_data}
                    messages.error(request, " Please fill all the required fields")
                    #return redirect(reverse('create_activity') + '?id='+formedit)
                    
                
            else:
                if Enquiry(activitylist):
                    activity_data.save()
                    new_act_id = Activity.objects.latest('id').id
                    #print(new_act_id)
                    new_act_id = Activity.objects.get(id=new_act_id)
                    bill_data = Bill(activity=new_act_id, added_by=added_by)
                    bill_data.save()

                    client_data = Clients.objects.get(pk=client_id)
                    if assign_int_eng is not None:
                        params = {'ticket_number':ticket_no, 'da_value':da, 'ewo':ewo, 'job_type':job_type, 'job_no':job_no, 'lus':lus, 'email':assign_int_eng.email, 'client':client_data.name}
                        send_mail(params, 'activity_mail.html', 'New ticket assigned')

                    if int_eng2 is not None:
                        params = {'ticket_number':ticket_no, 'da_value':da, 'ewo':ewo, 'job_type':job_type, 'job_no':job_no, 'lus':lus, 'email':int_eng2.email, 'client':client_data.name}
                        send_mail(params, 'activity_mail.html', 'New ticket assigned')

                    if assign_fielder is not None:
                        params = {'ticket_number':ticket_no, 'da_value':da, 'ewo_value':ewo,'job_type':job_type, 'job_no':job_no, 'lus':lus, 'email':assign_fielder.email, 'client':client_data.name}
                        send_mail(params, 'activity_mail.html', 'New ticket assigned')  
                        
                    #Activity.objects.filter(id=act_id).update(ticket=ticket_no)
                    for x in activitylist:
                        activity_data.activity.add(Activities.objects.get(id=x))
                    #Activity_media(activity_id=act_id,file_name=file_name,added_by=added_by).save()
                    
                    messages.success(request, " Your activity has been added successfully")
                    return redirect('activity_list')
                else:
                    edit_recdate = request.POST.get("rec_date")
                    edit_ecd = request.POST.get("ecd")
                    edit_data = activity_data
                    messages.error(request, " Please fill all the required fields")
                    #return redirect('create_activity')
        else:
            messages.error(request, " Please fill all the required fields")
            return redirect('create_activity')
    params = {"activities_list": activities_list, "clients_list": clients_list, "feusers_list": feusers_list, "bayusers_list": bayusers_list,"added_by":request.user.pk,"edit_data":edit_data,"edit_recdate":edit_recdate}            
    
    return render(request, 'create_activity.html', params)

