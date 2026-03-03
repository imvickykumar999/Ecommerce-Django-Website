from .models import Category

def categories(request):
    """Make categories available to all templates"""
    return {
        'categories': Category.objects.all()
    }
