from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import List, Link, UserExtra
from .forms import NewListForm, NewLinkForm, RegisterForm
import json
from django.contrib.auth.models import User


def json_response(json_str):
    return HttpResponse( json.dumps( json_str ), content_type = "application/json" ) 

def home(request):
	allLists = List.objects.all()
	return render_to_response("lists.html", {'lists': allLists }, RequestContext(request))

#Render the login page
def login(request):
	return render_to_response("login.html")

def logged_out(request):
	return render_to_response("logout.html")

#Render
def list(request, id):
	bookMarList = List.objects.get( id = id )
	items = bookMarList.links.all()
	return render_to_response("list.html", { 'items': items, 'listName': bookMarList.name, 'listId': id }, RequestContext(request))

def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email    = form.cleaned_data['email']
			password = form.cleaned_data['password'].strip()
			try:
				newUser = User.objects.create_user( username, email,  password )
				newUser.save()
				id = User.objects.latest('id')
				verified = UserExtra.objects.create( userid = id.pk, verified = True, approval_date = datetime.now() )
				verified.save()
			except Exception as e:
				return render_to_response("register.html", { 'form': form, 'e': e  }, RequestContext(request)) 
			return render_to_response('registered.html', { 'name': username, 'date': datetime.now() } )
		else:
			return render_to_response("register.html", { 'form': form }, RequestContext(request))
	else:
		return render_to_response("register.html", { 'form': RegisterForm() }, RequestContext(request))

@login_required
def newList(request):
	if request.method == "POST":
		form = NewListForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name'].strip()
			try:
				newBookmark = List.objects.create( name=name, dateCreated = datetime.now(), dateUpdated = datetime.now() )
				newBookmark.save()
			except Exception as e:
				# Error
				return json_response( { 'error': str(e) } )
			# Inserted succes
			id = List.objects.latest('id')
			return json_response( { 'added': { 'msg': 'The list was created.', 'id': id.pk, 'name': name, 'url': 'list/' + str( id.pk ) } } )
		else:
			# Form Errors were detected
			return json_response( form.errors )

@login_required
def newLink(request, listId):
	if request.method == "POST":
		form = NewLinkForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name'].strip()
			link = form.cleaned_data['link'].strip()
			tags = form.cleaned_data['tags'].strip()
			try: 
				addLink = Link.objects.create( name = name, link = link, dateCreated = datetime.now(), dateUpdated = datetime.now(), tags = tags )
				addLink.save()
				addToList = List.objects.get( id = listId )
				addToList.links.add( addLink )
			except Exception as e:
				return json_response( { 'error': str(e) } )
			id = Link.objects.latest('id')
			return json_response( { 'added': { 'msg': 'The link was added.', 'id': id.pk, 'name': name, 'url': link } } )
		else:
			# Form Errors were detected
			return json_response( form.errors )

@login_required
def deleteLists(request):
	if request.method == "POST":
		lists = request.POST.getlist( 'lists[]', False )
		if lists == False:
			return json_response( { 'error': 'None Selected' } )
		else:
			try:
				# find the lists depending on the posted ids
				listsDel = List.objects.filter( id__in = lists )
				# find all the links conncted to those lists
				links    = Link.objects.exclude( pk__in= listsDel )
				# delete the lists and all of its linkss
				links.delete()
				listsDel.delete()
			except Exception as e:
				return json_response( { 'error': str(e) } )
			return json_response( {'deleted' : { 'items' : lists, 'msg': 'Deleted!' } } )

@login_required
def deleteLinks(request):
	if request.method == "POST":
		links = request.POST.getlist( 'links[]', False )
		if links == False:
			return json_response( { 'error': 'None Selected' } )
		else:
			try:
				Link.objects.filter( id__in = links ).delete()
			except Exception as e:
				return json_response( { 'error': str(e) } )
			return json_response( {'deleted' : {'items' : links, 'msg': 'Deleted!' } } )


