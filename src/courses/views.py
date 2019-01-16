from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Course

class CourseListView(ListView):
    """
    View for Course List
    """

    model = Course

class CourseDetailView(DetailView):
    """
    View for Course Detail
    """

    model = Course