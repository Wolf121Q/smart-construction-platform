def get_client_ip(request):
	from ipware import get_client_ip as getClientIp
	client_ip, is_routable = getClientIp(request)
	if client_ip is None:
	    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	    if x_forwarded_for:
	        ip = x_forwarded_for.split(',')[-1].strip()
	    else:
	        ip = request.META.get('REMOTE_ADDR')
	    return ip
	else:
		return client_ip