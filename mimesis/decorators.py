from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.core.handlers.wsgi import WSGIRequest


def flashify(func):
    def wrapped(*args, **kwargs):
        if len(args) > 0 and isinstance(args[0], WSGIRequest):
            request = args[0]
            if request.method == "POST":
                s = SessionStore(session_key=request.POST.get("session_key"))
                request.user = User.objects.get(id=s["user_id"])
            elif not request.user.is_anonymous():
                request.session["user_id"] = request.user.id
        return func(*args, **kwargs)
    return wrapped
