"""
Definition of views.
"""
 
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

def request(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
       'testA'
    )

