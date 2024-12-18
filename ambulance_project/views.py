from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # Create index.html file
