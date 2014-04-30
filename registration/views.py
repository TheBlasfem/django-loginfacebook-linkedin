import facebook
from linkedin import linkedin
#from linkedin import server
import urllib2
import urlparse
import json
from xml.dom import minidom

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.contrib.auth.views import password_reset
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings

from registration.forms import UserCreationForm, UserChangeForm, UserLoginForm
from hackusername.models import MyUser


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')

    return render(request, 'registration/index.html')


def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')

    return render(request, 'registration/login.html')

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')

    return render(request, 'registration/register.html')

def register_email(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)     # create form object
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.email,
                                password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect('/profile')
    else:
        form = UserCreationForm() # An unbound form

    args = {'form':form}

    return render(request, 'registration/register_email.html', args)



def authlinkedin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')

    if request.GET.has_key('code'):
        code = request.GET['code']
        #print code

        #HACER CONSULTA A LINKEDIN POR EL TOKEN
        try:
            response=urllib2.urlopen("https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code&code="+code+
            "&redirect_uri="+request.build_absolute_uri()+"&client_id="+settings.LINKEDIN_APP_ID+"&client_secret="+settings.LINKEDIN_APP_SECRET)

        except urllib2.HTTPError:
            return HttpResponseRedirect('/')

        #print response.read()
        #print json.loads(response.read())
        access_token = json.loads(response.read())['access_token']
        print access_token
        response.close()

        #utilizo el access_token para obtener los datos del usuario
        url='https://api.linkedin.com/v1/people/~:(id,first-name,last-name,industry,emailAddress)?' \
            'oauth2_access_token='+access_token

        try:
            response=urllib2.urlopen(url)
            my_linkedin_xml = response.read()
            response.close()

        except urllib2.HTTPError:
            return HttpResponseRedirect('/')

        xmldoc = minidom.parseString(my_linkedin_xml)

        item=xmldoc.getElementsByTagName('first-name')
        first_name = item[0].firstChild.nodeValue

        item=xmldoc.getElementsByTagName('last-name')
        last_name = item[0].firstChild.nodeValue

        item=xmldoc.getElementsByTagName('email-address')
        email = item[0].firstChild.nodeValue

        item=xmldoc.getElementsByTagName('id')
        linkedin_id = item[0].firstChild.nodeValue

        name = first_name + ' ' + last_name

        try:
            #ya esta registrado (login)
            MyUser.objects.get(email=email, linkedin_id=linkedin_id)

        except MyUser.DoesNotExist:
            try:
                user = MyUser.objects.get(email=email)
                user.linkedin_id = linkedin_id
                user.save()
            except MyUser.DoesNotExist:
                #recien se va a registrar (registro, creo el usuario)
                user = MyUser(email=email, linkedin_id=linkedin_id, name=name)
                user.save()

        #logueo con mi usuario linkedin
        user = authenticate(email=email, linkedin_id=linkedin_id)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/profile/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect("https://www.linkedin.com/uas/oauth2/authorization?"
        "response_type=code&client_id="+settings.LINKEDIN_APP_ID+
        "=r_fullprofile%20r_emailaddress"
        "&state=DCEEFWF45453sdffef424&redirect_uri="+request.build_absolute_uri())



def authfacebook(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')

    if request.GET.has_key('code'):
        code = request.GET['code']

        #HACER CONSULTA A FACEBOOK POR EL TOKEN
        try:
            response=urllib2.urlopen("https://graph.facebook.com/oauth/"
                          "access_token?client_id=" +
                                 settings.FACEBOOK_APP_ID + "&"
                          "redirect_uri=" + request.build_absolute_uri() +
                          "&client_secret=" +
                                 settings.FACEBOOK_APP_SECRET +
                                 "&code="+code)
        except urllib2.HTTPError:
            return HttpResponseRedirect('/')

        access_token = urlparse.parse_qs(response.read())['access_token'][0]
        response.close()

        #utilizo el access_token para obtener los datos del usuario
        graph = facebook.GraphAPI(access_token)

        data = graph.get_object("me")
        facebook_id = data['id']
        email = data['email']
        name = data['name']

        try:
            #ya esta registrado (login)
            MyUser.objects.get(email=email, facebook_id=facebook_id)

        except MyUser.DoesNotExist:
            try:
                user = MyUser.objects.get(email=email)
                user.facebook_id = facebook_id
                user.save()
            except MyUser.DoesNotExist:
                #recien se va a registrar (registro, creo el usuario)
                user = MyUser(email=email, facebook_id=facebook_id, name=name)
                user.save()

        #logueo con mi usuario facebook
        user = authenticate(email=email, facebook_id=facebook_id)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/profile/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect("https://www.facebook.com/dialog/oauth?"
                                   "client_id="+settings.FACEBOOK_APP_ID+"&"
                                   "redirect_uri="+
                                   request.build_absolute_uri()
                                   +"&scope=publish_stream,email")

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_profile/')
    else:
        form = UserChangeForm(instance=request.user) # An unbound form

    args = {'form':form}

    return render(request, 'registration/edit_profile.html', args)


def login_user_email(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')

    message = ''
    if request.method == 'POST':
        form = UserLoginForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/profile/') # Redirect after POST
            else:
                message = _(u'username or password incorrect')
    else:
        form = UserLoginForm() # An unbound form

    return render(request, 'registration/login_email.html', {
        'form': form, 'message':message
    })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def my_password_reset(request):

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            if MyUser.objects.filter(
                    email=form.cleaned_data['email']).count() == 0:
                return render(request,
                    'registration/password_reset_email_error.html'
                )

    return password_reset(request,
                    template_name='registration/password_reset_form.html',
                     post_reset_redirect= '/user/password/reset/done/')