from django.shortcuts import render, redirect

def landing_page(request):
    if request.user.is_authenticated:
        return redirect("eventos:dashboard")
    return render(request, "landing.html")

