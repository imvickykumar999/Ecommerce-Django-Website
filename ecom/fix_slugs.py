#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from store.models import Category

for cat in Category.objects.all():
    cat.save()

print("Categories updated with slugs")
print(f"Total categories: {Category.objects.count()}")
for cat in Category.objects.all():
    print(f"  - {cat.name} → {cat.slug}")
