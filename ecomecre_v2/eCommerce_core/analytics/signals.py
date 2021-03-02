from django.dispatch import Signal

"""
# this signal is coming from the product.view -> detailView 
# for ech person that enter the some product it will sent signal 
"""
object_viewed_signal = Signal(providing_args=['instance', 'request'])
