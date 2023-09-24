#from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.

#def index(request):
#    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")


import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv, find_dotenv



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

ENV_FILE = find_dotenv()
if ENV_FILE:
	load_dotenv(ENV_FILE)

MONGO_DB_USERNAME = os.environ.get("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.environ.get("MONGO_DB_PASSWORD")
MONGO_DB_HOST = os.environ.get("MONGO_DB_HOST")

#uri = 'mongodb+srv://'+MONGO_DB_USERNAME+':'+MONGO_DB_PASSWORD+'@'+MONGO_DB_HOST+'/?retryWrites=true&w=majority'
#client = MongoClient(uri)

# Send a ping to confirm a successful connection
#try:
#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)

# AUTH0
oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))

def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

def index(request):
    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )
