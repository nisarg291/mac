from math import ceil
from datetime import datetime,timedelta
from django.shortcuts import render
# it is dao class file
# Create your views here.
from django.shortcuts import render,HttpResponse
from ast import literal_eval
import ctypes
from django.views.decorators.csrf import csrf_exempt
#from .Checksum1 import generate_checksum,verify_checksum
# so using  csrf_exempt thi aapde ne csrf ni chuthchath mali jay cha
# using this we do not required to use csrf token for this page using csrf_exempt so using this
from .models import Product, Contact, Order,OrderUpdate
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from math import ceil
import json
import os
import smtplib
import nltk
words = []
classes = []
documents = []
ignore = ['?']
model=0
intents=0
# tokenize sentences into individul words
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
# lancasterstemmer word stammer this is req. for word stamming
# word stamming the process we create varint of morphological words
# for example waits waiting an waited this words are reduce into root word is wait
# if cooks,cooking cooked is converted into root word is cook
stemmer = LancasterStemmer()

# Libraries needed for Tensorflow processing
import tensorflow as tf
import numpy as np
# import tensorflow.contrib.tensorrt as trt
import tflearn
import random

import json
# from screeninfo import get_monitors
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
with open('intents.json') as json_data:
    intents = json.load(json_data)
    # loop through each sentence in the intent's patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each and every word in the sentence
        w = nltk.word_tokenize(pattern)
        # add word to the words list
        words.extend(w)
        # add word(s) to documents
        documents.append((w, intent['tag']))
        # add tags to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

    # Perform stemming and lower each word as well as remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore]
words = sorted(list(set(words)))

    # remove duplicate classes
classes = sorted(list(set(classes)))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)
    # create training data
training = []
output = []
# create an empty array for output
output_empty = [0] * len(classes)

# create training set, bag of words for each sentence
for doc in documents:
    # initialize bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stemming each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is '1' for current tag and '0' for rest of other tags
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

    # shuffling features and turning it into np.array
random.shuffle(training)
training = np.array(training)

    # creating training lists
train_x = list(training[:,0])
train_y = list(training[:,1])

    # resetting underlying graph data
tf.reset_default_graph()

# Building neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 100)
net = tflearn.fully_connected(net, 100)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
    # Defining model and setting up tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

# Start training 
# increase no. of n_epoch for better result
model.fit(train_x, train_y, n_epoch=300, batch_size=8, show_metric=True)
model.save('model.tflearn')

import pickle
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )

# restoring all the data structures
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

with open('intents.json') as json_data:
    intents = json.load(json_data)
    # load the saved model
model.load('./model.tflearn')
def index(request):
    query=request.COOKIES.get("searchquery","z");
    print("query",query)
    if str(query)!='z':
        query=literal_eval(query)
    allProds = []
    catprods = Product.objects.values('category', 'id')
    # using this catprods have all categorys are store in table
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        # using this prod have the all product which have same categorys
        n = len(prod)
        nSlides=n
        # nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    user32=ctypes.windll.user32
    user32.SetProcessDPIAware()
    w,h=user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
    length=1;
    print(w)
    if w<700:
        length:1;
    params = {'allProds': allProds,'length':length,'recommanded':query}
    print(query[0])
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
    server.login('nisargadalja24680@gmail.com', 'nisarghitesh@2620029164#')

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
        orderId = request.POST.get('orderId')
        email = request.POST.get('email')
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
    # here max_age means cookie ketla time sudhi rehse ana mate che for defult value is None.it means it will destroy cookie when browser close if we give seconds then it store cookies for that seconds
    # expires var also use to expire the cookie in given date value
    # domain="www.example.com" for access value to that domain and subdomain
    # secure=True httponly=true so client-side javascript they cannot access cookies 
    searchquery=request.COOKIES.get('searchquery','z');
    print("searchquery",searchquery)
    if str(searchquery)=='z':
        lst=[]
        lst.append(str(query))
        searchquery=str(lst)
    else:
        searchquery=literal_eval(searchquery);
        searchquery.append(str(query))
        searchquery=str(searchquery)
        print("update",searchquery)
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
    params = {'allProds': allProds, "msg": "","recommanded":searchquery}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query","recommanded":searchquery}
    response=render(request, 'shop/search.html', params)
    response.set_cookie("searchquery",searchquery,max_age=60*60*24*365,expires=datetime.utcnow()+timedelta(days=365))
    return response

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

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def chatbot(request,chat):
    global words,classes,documents,ignore,model,intents
    usersentance=chat
    print(usersentance)
    
    
    def clean_up_sentence(sentence):
    # tokenizing the pattern
        sentence_words = nltk.word_tokenize(sentence)
    # stemming each word
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    # returning bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    def bow(sentence, words, show_details=False):
        # tokenizing the pattern
        sentence_words = clean_up_sentence(sentence)
        # generating bag of words
        bag = [0]*len(words)  
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s: 
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)

        return(np.array(bag))
    ERROR_THRESHOLD = 0.30
    def classify(sentence):
        # generate probabilities from the model
        results = model.predict([bow(sentence, words)])[0]
        # filter out predictions below a threshold
        results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append((classes[r[0]], r[1]))
        # return tuple of intent and probability
        return return_list

    def response(sentence, userID='123', show_details=False):
        results = classify(sentence)
        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            while results:
                for i in intents['intents']:
                    # find a tag matching the first result
                    if i['tag'] == results[0][0]:
                        # a random response from the intent
                        return random.choice(i['responses'])

                results.pop(0)

    context = {}
    ERROR_THRESHOLD = 0.25
    def classify(sentence):
        # generate probabilities from the model
        results = model.predict([bow(sentence, words)])[0]
        # filter out predictions below a threshold
        results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append((classes[r[0]], r[1]))
        # return tuple of intent and probability
        return return_list

    def response(sentence, userID='123', show_details=False):
        results = classify(sentence)
        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            while results:
                for i in intents['intents']:
                    # find a tag matching the first result
                    if i['tag'] == results[0][0]:
                        # set context for this intent if necessary
                        if 'context_set' in i:
                            if show_details: print ('context:', i['context_set'])
                            context[userID] = i['context_set']
                        # check if this intent is contextual and applies to this user's conversation
                        if not 'context_filter' in i or \
                            (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                            if show_details: print ('tag:', i['tag'])
                            # a random response from the intent             
                            return random.choice(i['responses'])
                results.pop(0)
    ans=response(usersentance)
    print(ans)
    return HttpResponse({ans}, status=200)

def chat(request):
    global words,classes,documents,ignore,model,intents
    return render(request,'shop/chatdemo.html')
  