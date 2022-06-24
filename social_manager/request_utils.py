from threading import current_thread
from django.utils.deprecation import MiddlewareMixin

_requests = {}

# function to get request anywhere in project like to get request.user in models.py, template_tags.py etc.
def get_current_request():
    t = current_thread()
    if t not in _requests:
        return None
    return _requests[t]


class RequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _requests[current_thread()] = request