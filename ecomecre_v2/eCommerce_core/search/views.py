from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product


class SearchProductsList(ListView):
    template_name = "search/search_product_list.html"
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get('q')  # <- get data from q
        featured = self.request.GET.get('featured')  # <- "on" or None

        return Product.objects.search(q, featured)

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductsList, self).get_context_data(**kwargs)
        context["title"] = "Products Search List"

        """ !!!! 
        # from here can use an query for analytics data in your app
        # query = self.request.GET.get('q')
        # context["query"] = query  # <- also option
        """

        return context
