#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from django.utils.http import urlquote
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from domoweb.models import Parameters
from django.shortcuts import redirect
from domoweb.rinor.pipes import InfoPipe
from domoweb.exceptions import RinorNotAvailable, RinorError
from httplib import BadStatusLine

def go_to_page(request, html_page, page_title, page_messages, **attribute_list):
    """
    Common method called to go to an html page
    @param request : HTTP request
    @param html_page : the page to go to
    @param page_title : page title
    @param **attribute_list : list of attributes (dictionnary) that need to be
           put in the HTTP response
    @return an HttpResponse object
    """
    
    if (not page_messages) :
        page_messages = []
        
    status = request.GET.get('status', None)
    msg = request.GET.get('msg', None)
    if (msg):
        page_messages.append({'status':status, 'msg':msg })
        
    response_attr_list = {}
    response_attr_list['page_title'] = page_title
    response_attr_list['page_messages'] = page_messages    
    response_attr_list['version'] = settings.DOMOWEB_VERSION
    response_attr_list['is_user_connected'] = __is_user_connected(request)
    for attribute in attribute_list:
        response_attr_list[attribute] = attribute_list[attribute]
    response = render_to_response(html_page, response_attr_list,
                              context_instance=RequestContext(request))
    response['Pragma'] = 'no-cache'
    response['Cache-Control'] = 'no-cache, must-revalidate'
    response['Expires'] = '0'
    return response

def admin_required(f):
    def wrap(request, *args, **kwargs):
        #this check the session if userid key exist, if not it will redirect to login page
        if not __is_user_admin(request):
            path = urlquote(request.get_full_path())
            return redirect("/admin/login/?next=%s" % path)
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

def __get_user_connected(request):
    """
    Get current user connected
    @param request : HTTP request
    @return the user or None
    """
    try:
        return request.session['user']
    except KeyError:
        return None

def __is_user_connected(request):
    """
    Check if the user is connected
    @param request : HTTP request
    @return True or False
    """
    try:
        request.session['user']
        return True
    except KeyError:
        return False

def __is_user_admin(request):
    """
    Check if user has administrator rights
    @param request : HTTP request
    @return True or False
    """
    user = __get_user_connected(request)
    return user is not None and user['is_admin']

def rinor_isconfigured(function):
    """
    Check if rinor is configured
    """
    def _dec(request, *args, **kwargs):
        try:
            _ip = Parameters.objects.get(key='rinor_ip')
            _port = Parameters.objects.get(key='rinor_port')
            if not 'rinor_api_version'  in request.session:
                try:
                    _info = InfoPipe().get_info_extended()
                except BadStatusLine:
                    return redirect("error_badstatusline_view")
                except RinorNotAvailable:
                    return redirect("error_resourcenotavailable_view")
                if (not _info.info.rinor_version_superior and not _info.info.rinor_version_inferior):
                    request.session['rinor_api_version'] = _info.info.rinor_version                    
                else:
                    return redirect("error_baddomogikversion_view")
            if not 'normal_mode' in request.session:
                try:
                    mode = InfoPipe().get_mode()
                except BadStatusLine:
                    return redirect("error_badstatusline_view")
                except RinorNotAvailable:
                    return redirect("error_resourcenotavailable_view")

                request.session['normal_mode'] = (mode == "normal")
        except Parameters.DoesNotExist:
            return redirect("config_welcome_view")
        else:
            return function(request, *args, **kwargs)
    return _dec

def ipFormatChk(ip_str):
   pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
   if re.match(pattern, ip_str):
      return True
   else:
      return False