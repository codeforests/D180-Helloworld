from django.shortcuts import render
from django.contrib.gis.geoip2 import GeoIP2


def get_client_ip(request):
    # Works even behind proxies/load balancers
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # First in list
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_country(request):
    ip = get_client_ip(request)
    g = GeoIP2()
    try:
        country = g.country(ip)
        return country  # {'country_code': 'US', 'country_name': 'United States'}
    except:
        return None

def index(request):
    country_info = get_user_country(request)
    country = country_info["country_name"] if country_info is not None else ""
    return render(request, "index.html", {"country" : country})