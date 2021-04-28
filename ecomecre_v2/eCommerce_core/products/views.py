from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse
from .models import Product, Comment
from carts.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.http import Http404
from analytics.signals import object_viewed_signal
from analytics.mixins import ObjectViewedMixin


class ListOfProducts(ListView):
    # model = Product  # <- auto lookup
    # template_name = "product_list.html"  # <- convention lookup
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):  # # <- manual lookup
        featured = self.kwargs.get('featured')  #
        if featured:
            return Product.objects.featured
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products List"
        cart_obj = Cart.objects.get_cart(self.request)
        context['cart'] = cart_obj
        return context


# todo add like buttons (voting)
class DetailOfProduct(ObjectViewedMixin, DetailView):
    # model = Product  # <- automate view
    context_object_name = 'product'
    form = CommentForm()

    def __init__(self):
        super(DetailOfProduct, self).__init__()
        self.product = None

    # product detail page  <- manual view
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        self.product = Product.objects.get_by_id(pk)  # <- my created look up

        if not self.product:
            raise Http404("no Product ")

        """
        create an analytic data, before showing the object 
        create an signal with who is looked for this object and when this happened
        in this example is an for function base view ! next will crete an mixin for the detailView   
        that handle this signal
        """
        # object_viewed_signal.send(self.product.__class__, instance=self.product, request=self.request)
        return self.product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Product Detail"
        context['form'] = self.form
        cart_obj = Cart.objects.get_cart(self.request)
        context['cart'] = cart_obj
        prod = self.product in cart_obj.products.all()
        context['product_in_cart'] = prod
        return context

    # template_name = "products/product_detail.html"  # <- convention auto lookup place

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)

        if form.is_valid():
            user = self.request.user
            product = Product.objects.filter(pk=self.kwargs['pk']).first()
            content = form.cleaned_data.get('content')

            comment, created = Comment.objects.get_or_create(
                product=product,
                user=user,
                content=content,
            )

            if created:
                messages.success(
                    self.request, f'thx {user.username} for your comment')

            return HttpResponseRedirect('.')


class CreateProduct(LoginRequiredMixin, CreateView):
    model = Product
    fields = ("title", "description", "price", "image", "featured")

    # template_name = "product_form.html"  # <- convention lookup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Product"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user  # <- add current user to product owner
        if form.instance.title:
            messages.success(
                self.request, f'Product added for {form.instance.title}')
        return super().form_valid(form)


class UpdateProduct(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ("title", "description", "price", "image")
    template_name = "products/product_update.html"  # <- convention auto lookup place

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.title:
            messages.success(
                self.request, f'Product updated ->  {form.instance.title}')
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        # user or admin
        return self.request.user == product.user or self.request.user.is_superuser


class DeleteProduct(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    context_object_name = 'product'

    def test_func(self):
        product = self.get_object()
        # user or admin
        return self.request.user == product.user or self.request.user.is_superuser

    def get_success_url(self):
        return reverse("products:product_list")
