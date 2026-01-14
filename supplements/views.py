from django.shortcuts import render
from .models import Sale
from django.db.models import Sum
from django.utils import timezone # Use this instead of datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import Sale, Supplement  # <--- ADD 'Supplement' HERE
# from django.shortcuts import render
# from django.db.models import Sum
# from django.utils import timezone
# from datetime import timedelta
# from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # 1. Get the search query from the URL (e.g., ?q=protein)
    query = request.GET.get('q')
    
    # 2. Fetch supplements
    items = Supplement.objects.all()
    
    # 3. If there is a search query, filter the results
    if query:
        items = items.filter(name__icontains=query)
    
    low_stock = items.filter(stock_quantity__lt=5).count()
    
    context = {
        'supplements': items,
        'low_stock_count': low_stock,
        'query': query, # We pass this back to keep the text in the search bar
    }
    return render(request, 'supplements/home.html', context)

@login_required
def monthly_report(request):
    # Use timezone.now() to avoid the "naive datetime" warning
    last_month = timezone.now() - timedelta(days=30)
    sales = Sale.objects.filter(sale_date__gte=last_month).order_by('-sale_date')
    
    total_revenue = sum(s.supplement.selling_price * s.quantity_sold for s in sales)
    total_profit = sales.aggregate(Sum('total_profit'))['total_profit__sum'] or 0
    
    context = {
        'sales': sales,
        'total_profit': total_profit,
        'total_revenue': total_revenue,
        'report_date': timezone.now()
    }
    return render(request, 'supplements/report.html', context)


from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin_once(request):
    # Check if admin already exists to prevent errors
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'chauhanraj3103@gmail.com', 'Admin@123')
        return HttpResponse("Admin created successfully! Username: admin, Password: Admin@123")
    else:
        return HttpResponse("Admin already exists.")