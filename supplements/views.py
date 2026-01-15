# from django.shortcuts import render
# from .models import Sale
# from django.db.models import Sum
# from django.utils import timezone # Use this instead of datetime
# from datetime import timedelta
# from django.contrib.auth.decorators import login_required
# from .models import Sale, Supplement  # <--- ADD 'Supplement' HERE
# from django.shortcuts import render
# from django.db.models import Sum
# from django.utils import timezone
# from datetime import timedelta
# from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Sale, Supplement
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.http import HttpResponse

# --- THE BOUNCER FUNCTION ---
def is_trainer_or_admin(user):
    # Returns True ONLY if user is Superuser OR in '619-Trainer' group
    return user.is_superuser or user.groups.filter(name='619-Trainer').exists()

@login_required
@user_passes_test(is_trainer_or_admin)  # <--- Strictly Enforces Access
def home(request):
    query = request.GET.get('q')
    items = Supplement.objects.all()
    
    if query:
        items = items.filter(name__icontains=query)
    
    low_stock = items.filter(stock_quantity__lt=5).count()
    
    context = {
        'supplements': items,
        'query': query,
        'low_stock_count': low_stock,
    }
    return render(request, 'supplements/home.html', context)

@login_required
@user_passes_test(is_trainer_or_admin)  # <--- Strictly Enforces Access
def monthly_report(request):
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