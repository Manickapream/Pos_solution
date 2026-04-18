import os
import sys
import django

# Set up Django environment
sys.path.append(r'c:\Users\Manicka pream\OneDrive\Desktop\POS\pos_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_backend.settings')
django.setup()

from api.models import Inquiry

def test_delete():
    print(f"Total inquiries before: {Inquiry.objects.count()}")
    first = Inquiry.objects.first()
    if first:
        print(f"Deleting inquiry with ID: {first.id}")
        first.delete()
        print(f"Total inquiries after: {Inquiry.objects.count()}")
    else:
        print("No inquiries found to delete.")

if __name__ == "__main__":
    test_delete()
