
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popivoire.settings')
django.setup()

from Postulants.models import Category

print("Categories in DB:")
for c in Category.objects.all():
    print(f"Name: {c.name}, Slug: {c.slug}, Parent: {c.parent}")
