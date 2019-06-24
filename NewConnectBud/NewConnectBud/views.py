from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.conf import settings
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK)
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from . models import UserProfile,UserWithroles


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register_user(request):
    import json
    import base64
    rtn_obj = {}

    user = User.objects.create_user(
        username=request.POST['email'],
        password=request.POST['password'],
        email=request.POST['email'],
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
    )
    user.save()
    userID = user.id

    rtn_obj['user_id'] = userID
    rtn_obj['first_name'] = request.POST['first_name']
    rtn_obj['last_name'] = request.POST['last_name']
    rtn_obj['email'] = request.POST['email']
    rtn_obj['username'] = request.POST['email']

    rtn_obj['msg_error'] = "Registration is done successfully.."
    data = json.dumps(rtn_obj)
    return HttpResponse(data)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def facebook_login(request):
    import json
    rtn_obj = {}

    # if 'member_id' in request.session:
    #    return HttpResponse('0') # already logged in
    # else:
    if request.method == 'POST':
        fbid = request.POST['fbid']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        if request.POST['date'] == '':
            date = 00
        else:
            date = request.POST['date']

        if request.POST['month'] == '':
            month = 00
        else:
            month = request.POST['month']

        if request.POST['year'] == '0':
            year = 00
        else:
            year = request.POST['year']

        if request.POST['gender'] == '':
            gender = ''
        else:
            gender = request.POST['gender']

        if User.objects.filter(email=email).exists():
            UserData = User.objects.get(email=email)
            fbprofile = UserProfile.objects.get(user_id=UserData.id)
            fbprofile.facebook_id = fbid
            fbprofile.save()
            rtn_obj['ack'] = "1"
            rtn_obj['user_id'] = str(UserData.id)
            rtn_obj['first_name'] = fname
            rtn_obj['last_name'] = lname
            rtn_obj['email'] = email
            rtn_obj['fb_id'] = fbid
            rtn_obj['date'] = date
            rtn_obj['month'] = month
            rtn_obj['year'] = year
            rtn_obj['gender'] = gender
            rtn_obj['msg_error'] = " Log In Successfull! "
            data = json.dumps(rtn_obj)
            return HttpResponse(data)

        else:
            if UserProfile.objects.filter(facebook_id=fbid).exists():
                fbprofile = UserProfile.objects.get(facebook_id=fbid)
                UserData = User.objects.get(email=email)
                rtn_obj['ack'] = "1"
                rtn_obj['user_id'] = str(UserData.id)
                rtn_obj['first_name'] = fname
                rtn_obj['last_name'] = lname
                rtn_obj['email'] = email
                rtn_obj['fb_id'] = fbid
                rtn_obj['date'] = date
                rtn_obj['month'] = month
                rtn_obj['year'] = year
                rtn_obj['gender'] = gender
                rtn_obj['msg_error'] = " Log In Successfull! "
                data = json.dumps(rtn_obj)
                return HttpResponse(data)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=fname,
                    last_name=lname
                )
                user.save()

                userID = user.id

                new_profile = UserProfile(
                    user=user,
                    facebook_id=fbid,
                    date=date,
                    year=year,
                    month=month,
                    gender=gender
                )
                new_profile.save()

                # cursor1 = connection.cursor()
                # cursor1.execute("update adminpanel_userprofile set facebook_id="+str(fbid)+",date="+str(date)+",month="+str(month)+",year="+str(year)+",gender="+gender+" WHERE user_id = "+str(userID))

                user_withroles = UserWithroles(
                    user=user,
                    userroles_id=2
                )
                user_withroles.save()

def google_login(request):
    import json
    rtn_obj = {}

    # if 'member_id' in request.session:
    #    return HttpResponse('0') # already logged in
    # else:
    if request.method == 'POST':
        gpid = request.POST['gpid']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        if request.POST['date'] == '':
            date = 00
        else:
            date = request.POST['date']

        if request.POST['month'] == '':
            month = 00
        else:
            month = request.POST['month']

        if request.POST['year'] == '0':
            year = 00
        else:
            year = request.POST['year']

        if request.POST['gender'] == '':
            gender = ''
        else:
            gender = request.POST['gender']
        if User.objects.filter(email=email).exists():
            UserData = User.objects.get(email=email)
            fbprofile = UserProfile.objects.get(user_id=UserData.id)
            fbprofile.google_id = gpid
            fbprofile.save()
            rtn_obj['ack'] = "1"
            rtn_obj['user_id'] = str(UserData.id)
            rtn_obj['first_name'] = fname
            rtn_obj['last_name'] = lname
            rtn_obj['email'] = email
            rtn_obj['gp_id'] = gpid
            rtn_obj['date'] = date
            rtn_obj['month'] = month
            rtn_obj['year'] = year
            rtn_obj['gender'] = gender
            rtn_obj['msg_error'] = " Log In Successfull! "
            data = json.dumps(rtn_obj)
            return HttpResponse(data)
        else:
            if UserProfile.objects.filter(google_id=gpid).exists():
                fbprofile = UserProfile.objects.get(google_id=gpid)
                UserData = User.objects.get(email=email)
                # request.session['member_id'] = fbprofile.user_id
                rtn_obj['ack'] = "1"
                rtn_obj['user_id'] = str(UserData.id)
                rtn_obj['first_name'] = fname
                rtn_obj['last_name'] = lname
                rtn_obj['email'] = email
                rtn_obj['gp_id'] = gpid
                rtn_obj['date'] = date
                rtn_obj['month'] = month
                rtn_obj['year'] = year
                rtn_obj['gender'] = gender
                rtn_obj['msg_error'] = " Log In Successfull! "
                data = json.dumps(rtn_obj)
                return HttpResponse(data)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=fname,
                    last_name=lname
                )
                user.save()

                userID = user.id

                new_profile = UserProfile(
                    user=user,
                    google_id=gpid,
                    date=date,
                    year=year,
                    month=month,
                    gender=gender
                )
                new_profile.save()
                user_withroles = UserWithroles(
                    user=user,
                    userroles_id=2
                )
                user_withroles.save()

