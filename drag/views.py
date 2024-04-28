# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Customer,Category , YourModel

def move_customer(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        category_id = request.POST.get('category_id')
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.category_id = category_id
            customer.save()
            return JsonResponse({'success': True})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Customer not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})



def add_formdata(request):
    return render(request, 'index1.html')



def table_view(request):
    data = YourModel.objects.all()
    return render(request, 'edit.html', {'data': data})

def edit_row(request, pk):
    print("edid save",pk)
    instance = YourModel.objects.get(pk=pk)
    print("instance",instance)
    if request.method == 'POST':
        instance.field1 = request.POST.get('field1')
        instance.field2 = request.POST.get('field2')
        instance.field3 = request.POST.get('field3')
        instance.field4 = request.POST.get('field4')
        instance.field5 = request.POST.get('field5')
        instance.field6 = request.POST.get('field6')
        instance.field7 = request.POST.get('field7')
        instance.field8 = request.POST.get('field8')
        instance.field9 = request.POST.get('field9')
        instance.field10 = request.POST.get('field10')
        instance.field11 = request.POST.get('field11')
        instance.field12 = request.POST.get('field12')
        instance.field13 = request.POST.get('field13')
        instance.field14 = request.POST.get('field14')
        instance.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
