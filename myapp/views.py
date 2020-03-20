from django.shortcuts import render
from myapp.mail_filter import main


def filtering(request):
    d = {"kekka":go_ans(request.GET.get('database'),
                      request.GET.get('content'))}
    return render(request, "myapp/form.html", d)

def go_ans(database=None, content=None):
    if database:
        return main(database, content)
    else:
        return None

# Create your views here.
