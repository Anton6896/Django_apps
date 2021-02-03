from django.views import generic
from .models import Car
from .filters import CarFilter
from django.shortcuts import get_object_or_404


class Index(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # query for new and used cars for tabs section in index page
        context['new_cars'] = Car.objects.filter(
            category='new').order_by('-date_posted')[:6]
        context['used_cars'] = Car.objects.filter(
            category='used').order_by('-date_posted')[:6]

        # query for carousell index item , i didn't adjust image size !
        # ist ok for me like that
        context['low_mile'] = Car.objects.all().order_by('miles')

        # create the search fields
        my_filter = CarFilter(self.request.GET, queryset=Car.objects.all())
        all = my_filter.qs
        context['all'] = all
        context['my_filter'] = my_filter

        return context


class About(generic.TemplateView):
    template_name = 'about.html'


class FilterResults(generic.TemplateView):
    template_name = 'filter_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        my_filter = CarFilter(self.request.GET, queryset=Car.objects.all())
        all_cars = my_filter.qs

        context['all_cars'] = all_cars
        context['my_filter'] = my_filter

        context['low_mile'] = Car.objects.all().order_by('miles')

        return context


class CarDetail(generic.DetailView):
    model = Car
    template_name = 'car_details.html'
    context_object_name = 'car'


class InventoryList(generic.ListView):
    model = Car
    template_name = 'inventory_cars.html'
    context_object_name = 'cars_set'

    def get_queryset(self):
        return Car.objects.all()
