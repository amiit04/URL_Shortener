from django.shortcuts import render
from .models import ShortURL
from .forms import CreateNewShortURL
from datetime import datetime
import random, string


# Create your views here.
def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

def all_links(request):
    links = ShortURL.objects.all()
    return render(request, 'all_links.html', {'links': links})

def redirect(request, url):
    current_obj = ShortURL.objects.filter(short_url=url)

    if len(current_obj) == 0:
        return render(request, 'notfound.html')
    
    content = {'obj':current_obj[0]}
    return render(request, 'redirect.html', content)

def generate():
    '''generates unique short codes'''
    random_chars_list = list(string.ascii_letters)
    random_chars = ''.join(random.choice(random_chars_list) for _ in range(6))
    return random_chars

def createShortURL(request):
    if request.method == 'POST':
        form = CreateNewShortURL(request.POST)
        
        if form.is_valid():
            original = form.cleaned_data['original_url']
            
            # Check if the short URL already exists in the database
            existing_short_url = ShortURL.objects.filter(original_url = original).first()
            if existing_short_url:
                return render(request, 'urlcreated.html', {'chars': existing_short_url.short_url})

            # Generate a unique short URL
            random_chars = generate()
            while ShortURL.objects.filter(short_url=random_chars).first():
                random_chars = generate()
            
            # If the short URL doesn't exist, create a new one
            d = datetime.now()
            new_url = ShortURL(original_url = original, short_url = random_chars, time_date_created=d)
            new_url.save()
            return render(request, 'urlcreated.html', {'chars': random_chars})
    else:
        form = CreateNewShortURL()
        content = {'form': form}
        return render(request, 'create.html', content)