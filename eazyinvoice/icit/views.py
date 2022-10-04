
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django import forms
from django.contrib.auth import get_user_model


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


from icit.models import IcitState, DummyMachineToken, IcitMessage
from api.models import USERAPPS
from icit.services import create_md5_hash, validate_secret_token


@login_required
def icit_landing(request):
    if USERAPPS.USER_ACCESS_ICIT not in request.user.userprofile.user_access:
        return HttpResponse('Unauthorized', status=401)
    
    icit_state = get_object_or_404(IcitState, user=request.user)
    messages = IcitMessage.objects.filter(user=request.user).order_by("-created_at")[:10]

    return render(
        request,
        "dummy_puncher.html",
        {"icit_state": icit_state, "messages": messages}
    )


@login_required
@require_POST
def toggle_state(request):
    if USERAPPS.USER_ACCESS_ICIT not in request.user.userprofile.user_access:
        return HttpResponse('Unauthorized', status=401)
    
    icit_state = get_object_or_404(IcitState, user=request.user)
    icit_state.should_be_logged_in = not icit_state.should_be_logged_in
    icit_state.save()

    return HttpResponse('ok', status=200)


# Dummy Machine endpoints

class MessageForm(forms.Form):
    message = forms.CharField(required=True, max_length=1000)

class UsernameForm(forms.Form):
    username = forms.CharField(required=True, max_length=255)


@api_view(['POST'])
@permission_classes([])
def record_messages(request):

    ua = request.META.get('HTTP_USER_AGENT')
    if ua != "dummypuncher":
        return Response("ua", 403)

    secret_token = request.META.get('HTTP_X_SECRET_TOKEN')
    if not secret_token:
        return Response("secret", 403)
    validate_secret_token(secret_token)

    token = request.META.get('HTTP_X_AUTH_TOKEN')
    if not token:
        return Response("auth", 403)
    
    thash = create_md5_hash(token)
    db_thash = DummyMachineToken.objects.first().token_hash
    if thash != db_thash:
        return Response("hash", 403)
    
    print(request.data)
    print(type(request.data))
    
    messages = []
    for msg in request.data.get("messages", []):
        msg_form = MessageForm(msg)
        if not msg_form.is_valid():
            return Response("", 400)
        else:
            messages.append(msg_form.cleaned_data['message'])
    if not len(messages):
        Response("no messages", 400)
    
    username_form = UsernameForm(request.data)
    if not username_form.is_valid():
        return Response("", 400)
    user = get_object_or_404(
        get_user_model(),
        username=username_form.cleaned_data['username']
    )

    IcitMessage.objects.bulk_create([
        IcitMessage.objects.create(
            user=user, message=m
        )
        for m in messages
    ])
    return Response("", 201)


@api_view(['GET'])
@permission_classes([])
def get_state(request):

    ua = request.META.get('HTTP_USER_AGENT')
    if ua != "dummypuncher":
        return Response("ua", 403)

    secret_token = request.META.get('HTTP_X_SECRET_TOKEN')
    if not secret_token:
        return Response("secret", 403)
    validate_secret_token(secret_token)

    token = request.META.get('HTTP_X_AUTH_TOKEN')
    if not token:
        return Response("auth", 403)
    
    thash = create_md5_hash(token)
    db_thash = DummyMachineToken.objects.first().token_hash
    if thash != db_thash:
        return Response("hash", 403)
    
    icit_states = IcitState.objects.values(
        "user__username",
        "should_be_logged_in",
    )
    return Response(icit_states, 200)
