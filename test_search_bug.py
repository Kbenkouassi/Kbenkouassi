import os
import django
import json
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popivoire.settings')
import django
django.setup()

from Postulants.views import get_ranking_json
from Postulants.models import Postulant

# Create some dummy data if needed, or rely on existing data
# Checking existing data matching "toure"
toures = Postulant.objects.filter(name__icontains='toure')
print(f"Postulants matching 'toure' in DB: {toures.count()}")
for p in toures:
    print(f" - {p.name} (ID: {p.id}, Pts: {p.cur_pts})")

factory = RequestFactory()
# Simulate the request made by JS: /api/ranking/?filtre=&q=toure
request = factory.get('/api/ranking/', {'q': 'toure', 'filtre': ''})
response = get_ranking_json(request)

print(f"API Status Code: {response.status_code}")
content = json.loads(response.content)
ranking = content['ranking']

print(f"API Returned Count: {len(ranking)}")
for p in ranking:
    print(f" - API: {p['name']} (ID: {p['id']}, Pts: {p['cur_pts']})")

# Simulate JS sort logic
print("\nSimulating JS Sort Logic:")
# Let's say we have the list from API. The JS sorts the DOM elements based on this list.
# If the DOM elements are the same as API return, the sort should be consistent.

# JS Logic:
# if (ptsB !== ptsA) return ptsB - ptsA;
# else return nameA.localeCompare(nameB);

sorted_ranking = sorted(ranking, key=lambda x: (-x['cur_pts'], x['name'].lower()))

print("Expected JS Sort Order:")
for p in sorted_ranking:
    print(f" - {p['name']} ({p['cur_pts']})")

# Check if the API return itself is sorted
print("\nIs API return sorted?")
is_sorted = True
for i in range(len(ranking) - 1):
    current = ranking[i]
    next_p = ranking[i+1]
    if current['cur_pts'] < next_p['cur_pts']:
        print(f"Sort Error at index {i}: {current['cur_pts']} < {next_p['cur_pts']}")
        is_sorted = False
    elif current['cur_pts'] == next_p['cur_pts']:
        if current['name'] > next_p['name']:
            print(f"Sort Error (Name) at index {i}: {current['name']} > {next_p['name']}")
            is_sorted = False

if is_sorted:
    print("API is sorted correctly.")
else:
    print("API is NOT sorted correctly.")
