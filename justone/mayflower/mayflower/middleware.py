#coding:utf8
from django.http import HttpResponse


class DebugMiddleware(object):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if not request.user.is_authenticated() and not request.path.startswith('/admin') and not request.path.startswith('/payment/'):
            return HttpResponse(u'Сайт заработает в ближайшее время. Приносим свои извинения.', status=503)
