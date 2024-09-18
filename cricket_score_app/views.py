from django.shortcuts import render, redirect

def redirect_view(request):
    return redirect('/scoring/')
