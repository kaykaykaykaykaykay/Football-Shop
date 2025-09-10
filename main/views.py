from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        "app_name": "main",
        "student_name": "Khayru Rafa Kartajaya",
        "student_class": "PBP KKI",
    }
    return render(request, "main/main.html", context)