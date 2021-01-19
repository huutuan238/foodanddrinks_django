from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import SearchResultsView

urlpatterns = [
                  path('', views.index, name='index'),
                  path('register/', views.register, name='register'),
                  path('register/inform/', views.inform, name='inform'),
                  path('register/success_activation/', views.success_activation, name='success_activation'),
                  path('register/fail_activation/', views.fail_activation, name='fail_activation'),
                  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
                  path('accounts/profile/', views.profile, name='profile'),
                  path('accounts/profile/edit', views.updateProfile, name='edit_profile'),

                  path('product/<int:pk>', views.product_detail_view, name='product_details'),

                  path('order/', views.cart_detail, name='order'),
                  path('item_clear/<int:pk>/', views.item_clear, name='item_clear'),
                  path('make_order/', views.make_order, name='make_order'),
                  path('item_increment/<int:pk>/', views.item_increment, name='item_increment'),
                  path('item_decrement/<int:pk>/', views.item_decrement, name='item_decrement'),

                  # path('review/<int:pk>', views.review_product, name='review_product'),
                  path('search/', SearchResultsView.as_view(), name='search_results'),
                  path('category/<int:pk>/price/', views.filter_price, name='filter_price'),

                  path('add_to_cart/<int:pk>/', views.cart_add, name='add_to_cart'),
                  path('order/', views.cart_detail, name='order'),

                  path('addcomment/<int:pk>', views.addcomment, name='addcomment'),
                  path('category/<int:pk>', views.product_by_category, name='product_by_category'),

                  path('accounts/profile/approved_order', views.approved_order, name='approved_order'),
                  path('accounts/profile/pending_order', views.pending_order, name='pending_order'),
                  path('accounts/profile/past_order', views.past_order, name='past_order'),

                  path('order_detail/<int:pk>/', views.order_detail, name='order_detail'),

                  path('contact',views.show_contact, name='contact'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
