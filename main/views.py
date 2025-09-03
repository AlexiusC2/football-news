from django.shortcuts import render
def show_main(request):
    context = {
        'npm' : '2406496164',
        'name': 'Alexius Christhoper Wijaya',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)
# Create your views here.
