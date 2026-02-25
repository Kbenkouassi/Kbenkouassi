
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "popivoire.settings")
django.setup()

from Advertisements.models import AdSpace

print("AdSpace slugs:")
for s in AdSpace.objects.all():
    print(f"- {s.name}: {s.slug}")
