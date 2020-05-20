from math import ceil

from django.shortcuts import render
# it is dao class file
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from .Checksum1 import generate_checksum,verify_checksum
# so using  csrf_exempt thi aapde ne csrf ni chuthchath mali jay cha
# using this we do not required to use csrf token for this page using csrf_exempt so using this
from .models import Product, Contact, Order,OrderUpdate
from math import ceil
import json
import os
import smtplib
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

    #order=Order.objects.filter(order_id=id)
    #line=[f"{name} your order details",f"{name} your order id is {id} and order amount is {amount}.Payment of {amount} is successfully done.your dilivery address:{address} and city:{city} state:{state} and your phone is {phone}. please verify delivery address details this will not change. if any query then contact on no.7802043370",'nisargadalja24680@gmail.com',email]
    #send_mail(line)
def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    allProds = []
    catprods = Product.objects.values('category', 'id')
    # using this catprods have all categorys are store in table
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        # using this prod have the all product which have same categorys
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')
def contact(request):
    thank=False;
    if request.method=="POST":
        thank = True;
        name = request.POST.get('name');
        # here parameter of get is the value of the name attr. of the input tag which of the tag's data we wants.
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        # use for insert data into database and table name is Contact
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save();
    return render(request, 'shop/contact.html',{'thank':thank})


def send_mail_student(sender, reciever, mail_body, mail_subject):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()  # The client sends this command to the SMTP server to identify itself and initiate the SMTP conversation.
    server.starttls()  # encrypts are connection
    server.ehlo()

    server.login('nisargadalja24680@gmail.com', 'NisargHitesh@2620029164#')

    subject = mail_subject
    body = mail_body

    msg = f"Subject: {subject}\n\n{body}"  # new f-string way to format in python like we use ``  and ${} in js

    server.sendmail(
        sender,  # from
        reciever,  # to
        msg
    )
    print('mail sent!')
    server.quit()


def send_mail(line):
    print(line)
    sender = line[2]
    reciever = line[3]
    mail_body = line[1]
    mail_subject = line[0]
    send_mail_student(sender, reciever, mail_body, mail_subject)

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    #response = json.dumps([updates, order[0].items_json],default=str)
                    # it send list of data in the tracker.html page
                    # so in that page we parse the data into json then use data[0],data[1] bcz it is list
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json},default=str)
                    # it send dictinary of data into json form in the tracker.html page
                    # we parse data into json.parse to convert into dictionary from the json form
                    # we use data['update'] and so on.
                return HttpResponse(response)

            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.subcategory.lower() or query in item.desc.lower()  or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0],'id':myid})



def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        amount=request.POST.get('amount','')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json,amount=amount, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        name=name
        amountRs=amount
        amount=int(amount)*0.01368;
        amount=round(amount,4);
        #bcz convert into doller
        line = [f"{name} your order details",f"{name} your order id is {id} and order amount is Rs.{amountRs}.Payment of Rs.{amountRs} is successfully done.your dilivery address:{address} and city:{city} state:{state} and your phone is {phone}. please verify delivery address details this will not change. if any query then contact on no.7802043370",'nisargadalja24680@gmail.com', email]
        send_mail(line);
        #sendmail(id, name, email, phone, amount, address, city, state, zip_code);
        return render(request, 'shop/test.html',{'amount':amount,'thank':thank, 'id': id,'name':name})



    return render(request, 'shop/checkout.html')
    # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    # Request paytm to transfer the amount to your account after payment by user
    # it is for Paytm
    # param_dict = {
    #     'MID': 'WorldP64425807474247',
    #     'ORDER_ID': str(order.order_id),
    #     'TXN_AMOUNT': str(amount),
    #     'CUST_ID': email,
    #     'INDUSTRY_TYPE_ID': 'Retail',
    #     'WEBSITE': 'WEBSTAGING',
    #     'CHANNEL_ID': 'WEB',
    #     'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handleRequest/',
    # }
    # param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, MERCHANT_KEY)

#this is for paytm
# using csrf_exempt give the  permisition to the other website(paytm) to use this this method
# @csrf_exempt
# def handlerequest(request):
    #return HttpResponse('done')
    # form = request.POST
    # response_dict = {}
    # for i in form.keys():
    #     response_dict[i] = form[i]
    #     if i == 'CHECKSUMHASH':
    #         checksum = form[i]
    #
    # verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    # if verify:
    #     if response_dict['RESPCODE'] == '01':
    #         print('order successful')
    #     else:
    #         print('order was not successful because' + response_dict['RESPMSG'])
    # return render(request, 'shop/paymentstatus.html', {'response': response_dict})

