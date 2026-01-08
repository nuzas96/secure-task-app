import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.dispatch import receiver

audit_logger = logging.getLogger("audit")

def get_ip(request):
    if not request:
        return "-"
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "-")

@receiver(user_logged_in)
def log_login_success(sender, request, user, **kwargs):
    audit_logger.info(f"LOGIN_SUCCESS | user={user.username} | ip={get_ip(request)}")

@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    username = credentials.get("username", "<unknown>")
    audit_logger.info(f"LOGIN_FAILED | user={username} | ip={get_ip(request)}")

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user:
        audit_logger.info(f"LOGOUT | user={user.username} | ip={get_ip(request)}")
