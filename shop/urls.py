# it is one type of controller
from django.urls import path,include
from . import views

urlpatterns = [

    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    # path("mail/<int:id>",views.sendmail,name="mail"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout", views.checkout, name="Checkout"),
    path("contact/chat", views.chat, name="chat"),
    path("contact/chatbot/<str:chat>", views.chatbot, name="Chatbot"),
    #path("handlerequest", views.handlerequest, name="HandleRequest"),
]