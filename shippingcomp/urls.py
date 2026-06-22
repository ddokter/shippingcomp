from django.contrib import admin
from django.urls import path, include
from djbosui.urls import urlpatterns as djbosui_patterns
from .views.home import Home
from .views.cart import CartView, CartDeleteView, CartItemView
from .views.cartproduct import CartProductView
from .views.order import OrderContact, OrderPayment, OrderReview, OrderCancel
from .views.bookingproduct import BookingproductCreate
# from .views.booking import BookingCreate
from .views.payment import PaymentFailure, PaymentSuccess
from .views.booking import BookingPayment, BookingCoupon


public_urls = [
    path('cart', CartView.as_view(), name="cart"),

    path('cart', CartView.as_view(), name="cart_nr_of_items"),

    path('rm_cart', CartDeleteView.as_view(), name="cart_delete"),

    path('cartitem/<int:pk>', CartItemView.as_view(), name="cartitem"),

    path('cartproduct', CartProductView.as_view(), name="cartproduct"),

    path('cartproduct/<int:pk>',
         CartProductView.as_view(), name="cartproduct"),

    path("order/add_contact", OrderContact.as_view(),
         name="order_add_contact"),

    path("order/<int:pk>/review", OrderReview.as_view(),
         name="order_review"),

    path("order/<int:pk>/pay", OrderPayment.as_view(),
         name="order_pay"),

    path("order/<int:pk>/payment_failure", PaymentFailure.as_view(),
         name="payment_failure"),

    path("order/<int:pk>/payment_success", PaymentSuccess.as_view(),
         name="payment_success"),

    path("order/<int:pk>/cancel", OrderCancel.as_view(),
         name="order_cancel"),

    path("booking/<int:pk>/add_payment",
         BookingPayment.as_view(),
         name="booking_add_payment"),

    path("booking/<int:pk>/apply_coupon/<int:coupon>",
         BookingCoupon.as_view(),
         name="booking_apply_coupon")

]


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),

    path('payments/', include('payments.urls')),

    path('', Home.as_view(), name="home"),

    path('cart', CartView.as_view(), name="cart"),

    path('rm_cart', CartDeleteView.as_view(), name="cart_delete"),

    path('cartitem/<int:pk>', CartItemView.as_view(), name="cartitem"),

    path('cartproduct', CartProductView.as_view(), name="cartproduct"),

    path('cartproduct/<int:pk>',
         CartProductView.as_view(), name="cartproduct"),

    path('<str:parent_model>/<int:parent_pk>/add_bookingproduct',
         BookingproductCreate.as_view(),
         name="inline_create"),

    #path('shippingcomp.booking/add/',
    #     BookingCreate.as_view(),
    #     name="create_booking"),

] + djbosui_patterns
