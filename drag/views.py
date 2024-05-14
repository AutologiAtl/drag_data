# views.py

from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from datetime import datetime , date
from django.db.models import Max
from django.db.models import Max, OuterRef, Subquery
from django.utils import timezone
import pyodbc
from django.contrib import messages
from django.core.cache import cache
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


# Define the connection parameters
server = 'autologisticsjapan-testing.database.windows.net'
database = 'ATLDbBackup'
username = 'db_admin'
password = 'atlit_1234'

# Define the connection string with the ODBC driver name
conn_str = (
    f'DRIVER=ODBC Driver 18 for SQL Server;'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)


def move_customer(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        category_id = request.POST.get('category_id')
        print("customer_id",customer_id)
        print("category_id",category_id)



        try:
            customer = Customercompany.objects.get(id=customer_id)
            get_cat = Customercategory.objects.get(id = int(category_id))
            print("customer 67",customer)
            customer.customercategoryid = get_cat
            customer.save()
            return JsonResponse({'success': True})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Customer not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def index(request):
    print("database work")
    categories = Customercategory.objects.all()
    return render(request, 'index.html', {'categories': categories})



def add_formdata(request):
    return render(request, 'index1.html')



from django.http import JsonResponse

def Search(request):
    if request.method == 'POST':
        pol = request.POST.get('pols')
        pod = request.POST.get('pods')
        continer = request.POST.get('continers')
        liner = request.POST.get('liners')
        print("liner", liner)
        print("pol", pol)
        print("pod", pod)
        print("container", continer)

        # Create a dictionary containing the data
        data = {
            'liner': liner,
            'pol': pol,
            'pod': pod,
            'container': continer
        }

        request.session['search-d'] = data

        # Return a JSON response with the data
        return redirect("/table")


def table_view(request):
    context = {}
    try:
        # Check if data exists in cache
        if 'table_data' in cache:
            data = cache.get('table_data')
            context = data
        else:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Fetching Company Names from ShippingCompany table
            fetch_companies_query = "SELECT CompanyNameEng, Id FROM ShippingCompany"
            cursor.execute(fetch_companies_query)
            companies = cursor.fetchall()
            context['liners'] = [{'CompanyNameEng': row[0], 'Id': row[1]} for row in companies]

            # Fetching Port Names where PortCountryId is 106
            fetch_pol_query = "SELECT PortNameEng, Id FROM Port WHERE PortCountryId = 106"
            cursor.execute(fetch_pol_query)
            ports_pol = cursor.fetchall()
            context['ports_pol'] = [{'PortNameEng': row[0], 'Id': row[1]} for row in ports_pol]

            fetch_pod_query = "SELECT PortNameEng, Id FROM Port WHERE PortCountryId NOT IN (106, 1)"
            cursor.execute(fetch_pod_query)
            ports_pod = cursor.fetchall()
            context['ports_pod'] = [{'PortNameEng': row[0], 'Id': row[1]} for row in ports_pod]

            # Fetching Container Sizes
            fetch_container_size_query = "SELECT Size, Id FROM ShippingContainerSize"
            cursor.execute(fetch_container_size_query)
            container_sizes = cursor.fetchall()
            context['container_sizes'] = [{'Size': row[0], 'Id': row[1]} for row in container_sizes]


            # Fetching Currency Descriptions
            fetch_currency_query = "SELECT CurrencyDesc, Id FROM CurrencyMst"
            cursor.execute(fetch_currency_query)
            currencies = cursor.fetchall()
            context['currencies'] = [{'CurrencyDesc': row[0], 'Id': row[1]} for row in currencies]
            print("context['currencies']",context['currencies'])
            # Close the connection
            conn.close()
            # Store data in cache for future requests
            a = cache.set('table_data', context, timeout=3600) # Cache for 1 hour


        pol = request.POST.get('pols')
        pod = request.POST.get('pods')
        continer = request.POST.get('continers')
        liner = request.POST.get('liners')

        if pol or pod or continer or liner:
            latest_records = Freightrate.objects.all()
            print("pol pod",pol)
            if pol:
                pol = Port.objects.get(id = pol)
            if pod:
                pod = Port.objects.get(id = pod)
            if continer:    
                containerid = Shippingcontainersize.objects.get(id = continer)
            if liner:
                 liner = Shippingcompany.objects.get(id = liner)

            if pol:
                latest_records = latest_records.filter(polid=pol)
            if pod:
                latest_records = latest_records.filter(podid=pod)
            if continer:
                latest_records = latest_records.filter(shippingcontainersizeid=continer)
            if liner:
                latest_records = latest_records.filter(shippingcompanyid=liner)    

        else:
            print("this is run")
            latest_records_subquery = Freightrate.objects.filter(
                polid=OuterRef('polid'),podid=OuterRef('podid'),shippingcompanyid=OuterRef('shippingcompanyid'),type=OuterRef('type'),
                shippingcontainersizeid=OuterRef('shippingcontainersizeid'),
            ).order_by('-id').values('id')[:1]

            print("yess running")


            # Query to retrieve the latest record for each unique name
            # latest_records = Freightrate.objects.filter(
            #     id__in=Subquery(latest_records_subquery)
            # )

            latest_records = Freightrate.objects.filter(
            id__in=Subquery(latest_records_subquery)
        )    

        current_date = date.today()
        for record in latest_records:
            print("record check",record)
            record_date = record.validityto.date()
            print("record_date",record_date)
            print("current_date",current_date)
            record.has_expired = record_date < current_date

        try:
            paginator = Paginator(latest_records, 10)
            page = request.GET.get('page')
            data = paginator.get_page(page)
            context['data'] = data
        except PageNotAnInteger:
            data = paginator.page(1)
            context['data'] = data
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
            context['data'] = data
        return render(request, 'edit.html', context)

    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")


def edit_row(request, pk):
    print("edid save",pk)
    instance = Freightrate.objects.get(pk=pk)
    print("instance",instance)
    if request.method == 'POST':
        instance.thc = request.POST.get('field5')
        instance.oceanfreight = request.POST.get('field9')
        instance.sealamount = request.POST.get('field10')
        instance.docfee = request.POST.get('field11')
        instance.freedays = request.POST.get('field12')
        instance.validityfrom = request.POST.get('field13')
        instance.validityto = request.POST.get('field14')

        print("instance.validityfrom ",instance.validityfrom )

        from_date = datetime.strptime(instance.validityfrom, '%d-%m-%Y')
        to_date = datetime.strptime(instance.validityto, '%d-%m-%Y')

        instance.validityfrom = from_date 
        instance.validityto = to_date 

        # Now, you can save the instance to update the database
        instance.save()
        print("check print",to_date)

        
        instance.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


def add_row(request):
    print("add data")
    if request.method == 'POST':
        # Retrieve the data from the POST request
        pol = request.POST.get('polr')
        pod = request.POST.get('podr')
        liner = request.POST.get('linerr')
        currency = request.POST.get("currency")
        typer = request.POST.get('typer')
        cntr = request.POST.get('cntrr')
        cntr_price = request.POST.get('cntrpricer')
        thc = request.POST.get('thcr')
        sealamt = request.POST.get('sealamtr')
        docfee = request.POST.get('docfeer')
        freedays = request.POST.get('freedays')
        validityf = request.POST.get('validityfromr')
        validityto = request.POST.get('validitytor')
        
        # to_date = datetime.strptime(validityto, '%d-%m-%Y').strftime('%d-%m-%Y')
        # from_date = datetime.strptime(validityf, '%d-%m-%Y').strftime('%d-%m-%Y')

        from_date = datetime.strptime(validityf, '%d-%m-%Y')
        to_date = datetime.strptime(validityto, '%d-%m-%Y')


        print("check data")
        print("from_date",from_date)
        print("to_date",to_date)

        print("pol id",pol)
        print("pod id",pod)
        print("cntr id",cntr)
        print("liner id",liner)
        print("currency check ",currency)

        pol = Port.objects.get(id = pol)
        pod = Port.objects.get(id = pod)
        currecy_id = Currencymst.objects.get(id = currency)
        containerid = Shippingcontainersize.objects.get(id = cntr)
        liner = Shippingcompany.objects.get(id = liner)
        print('currecy_id obj',currecy_id)

        input_date = datetime.strptime(validityf, "%d-%m-%Y")
        formatted_date = input_date.strftime("%Y-%m-%d")

        input_dateto = datetime.strptime(validityto, "%d-%m-%Y")
        formatted_dateto = input_dateto.strftime("%Y-%m-%d")

        if from_date < to_date:
            print("less date")
            if not Freightrate.objects.filter(validityfrom__lte=from_date, validityto__gte=to_date).exists():
                print("not esists")
                instance = Freightrate(
                    polid=pol,
                    podid=pod,
                    shippingcompanyid=liner,
                    type=typer,
                    shippingcontainersizeid=containerid,
                    oceanfreight=cntr_price,
                    thc=thc,
                    sealamount=sealamt,
                    docfee=docfee,
                    freedays=freedays,
                    validityfrom=formatted_date,
                    validityto=formatted_dateto,
                    currencyid=currecy_id
                )
                instance.save()
                print("sava h")
                return JsonResponse({'status': 'success'})
            else:
                print("status 400")
                return JsonResponse({'status': 'fail'})
        else:
            print("status 400 e")
            return JsonResponse({'status': 'fail'})        

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def addNewEntry(request):
    if request.method == 'POST':
        print("posted")
        # Retrieve the data from the POST request
        liner = request.POST.get('liner')
        pol = request.POST.get('pol')
        pod = request.POST.get('pod')
        typed = request.POST.get('type')
        continer = request.POST.get('continer')
        thc = request.POST.get('thc')
        ocean = request.POST.get('ocean')
        seal = request.POST.get('seal')
        currency = request.POST.get('currency')
        doc = request.POST.get('doc')
        free = request.POST.get('freedays')
        fromd = request.POST.get('fromdate')
        tod = request.POST.get('todate')
        pol = Port.objects.get(id = pol)
        pod = Port.objects.get(id = pod)
        containerid = Shippingcontainersize.objects.get(id = continer)
        liner = Shippingcompany.objects.get(id = liner)
        currency = Currencymst.objects.get(id = currency)
    
        if Freightrate.objects.filter(polid = pol , podid = pod,shippingcontainersizeid = containerid,shippingcompanyid = liner).exists():
            messages.success(request, 'Entry Already Exists')
            return redirect("/table")
        save_enrty_records = Freightrate(polid = pol , podid = pod, shippingcompanyid = liner, type = typed, thc = thc,oceanfreight = ocean, shippingcontainersizeid = containerid,
        sealamount = seal, docfee = doc, freedays = free , validityfrom = fromd, validityto = tod,currencyid = currency)    
        save_enrty_records.save()
        messages.success(request, 'Entry added successfully')
        return redirect("/table")

# def list_hystory(request):
#     query = request.GET.get('q')

#     if query:
#         all_items = all_items = Freightrate.objects.filter(
#             Q(polid__portnameeng__icontains=query) | 
#             Q(podid__portnameeng__icontains=query) | 
#             Q(shippingcompanyid__companynameeng__icontains=query) | 
#             Q(type__icontains=query) | 
#             Q(thc__icontains=query) | 
#             Q(shippingcontainersizeid__size__icontains=query)
#          )
#     else:
#         all_items = Freightrate.objects.all().order_by('-id')
    
#     paginator = Paginator(all_items, 10) 

#     page = request.GET.get('page')
#     try:
#         items = paginator.page(page)
#     except PageNotAnInteger:
#         items = paginator.page(1)
#     except EmptyPage:
#         items = paginator.page(paginator.num_pages)
#     return render(request, 'hystory.html', {'data': items})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('lemail')
        password = request.POST.get('lpassword')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Pass the HttpRequest object as the first argument
            return redirect('/index/')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')


def list_hystory(request):
    context = {}
    try:

        # Check if data exists in cache
        if 'table_data1' in cache:
            data = cache.get('table_data1')
            context = data

        else:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Fetching Company Names from ShippingCompany table
            fetch_companies_query = "SELECT CompanyNameEng, Id FROM ShippingCompany"
            cursor.execute(fetch_companies_query)
            companies = cursor.fetchall()
            context['liners'] = [{'CompanyNameEng': row[0], 'Id': row[1]} for row in companies]

            # Fetching Port Names where PortCountryId is 106
            fetch_pol_query = "SELECT PortNameEng, Id FROM Port WHERE PortCountryId = 106"
            cursor.execute(fetch_pol_query)
            ports_pol = cursor.fetchall()
            context['ports_pol'] = [{'PortNameEng': row[0], 'Id': row[1]} for row in ports_pol]

            fetch_pod_query = "SELECT PortNameEng, Id FROM Port WHERE PortCountryId NOT IN (106, 1)"
            cursor.execute(fetch_pod_query)
            ports_pod = cursor.fetchall()
            context['ports_pod'] = [{'PortNameEng': row[0], 'Id': row[1]} for row in ports_pod]

            # Fetching Container Sizes
            fetch_container_size_query = "SELECT Size, Id FROM ShippingContainerSize"
            cursor.execute(fetch_container_size_query)
            container_sizes = cursor.fetchall()
            context['container_sizes'] = [{'Size': row[0], 'Id': row[1]} for row in container_sizes]


            # Fetching Currency Descriptions
            fetch_currency_query = "SELECT CurrencyDesc, Id FROM CurrencyMst"
            cursor.execute(fetch_currency_query)
            currencies = cursor.fetchall()
            context['currencies'] = [{'CurrencyDesc': row[0], 'Id': row[1]} for row in currencies]
            print("context['currencies']",context['currencies'])
            # Close the connection
            conn.close()
            # Store data in cache for future requests
            a = cache.set('table_data1', context, timeout=3600) # Cache for 1 hour


        pol = request.POST.get('pols1')
        pod = request.POST.get('pods1')
        continer = request.POST.get('continers1')
        liner = request.POST.get('liners1')

        if pol or pod or continer or liner:
            latest_records = Freightrate.objects.all()
            print("pol pod",pol)
            if pol:
                pol = Port.objects.get(id = pol)
            if pod:
                pod = Port.objects.get(id = pod)
            if continer:    
                containerid = Shippingcontainersize.objects.get(id = continer)
            if liner:
                 liner = Shippingcompany.objects.get(id = liner)

            if pol:
                latest_records = latest_records.filter(polid=pol)
            if pod:
                latest_records = latest_records.filter(podid=pod)
            if continer:
                latest_records = latest_records.filter(shippingcontainersizeid=continer)
            if liner:
                latest_records = latest_records.filter(shippingcompanyid=liner)    

        else:
            print("this is run")
            latest_records = Freightrate.objects.all()

            print("yess running")

        current_date = date.today()
        for record in latest_records:
            print("record check",record)
            record_date = record.validityto.date()
            record.has_expired = record_date < current_date

        try:
            if 'table_data2' in cache:
                start_time = time.time()  # Record start time
                data = cache.get('table_data2')
                context = data
                print("this is running")
                end_time = time.time()    # Record end time
                execution_time = end_time - start_time
                print("Execution time table2:", execution_time, "seconds")
            else:
                print("this is running else")
                a = cache.set('table_data2', context, timeout=3600) # Cache for 1 hour

            paginator = Paginator(latest_records, 10)
            page = request.GET.get('page')
            data = paginator.get_page(page)
            context['data'] = data
        except PageNotAnInteger:
            data = paginator.page(1)
            context['data'] = data
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
            context['data'] = data
        return render(request, 'hystory.html', context)
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")


import time
import pyodbc

def runquery(request):
    start_time = time.time()  # Record start time
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    companies = Freightrate.objects.all()
    print("check @@@@", companies)
    
    end_time = time.time()    # Record end time
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    
    return redirect("/po")


    