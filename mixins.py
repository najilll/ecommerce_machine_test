import re

from django.contrib.auth.mixins import LoginRequiredMixin


def check_access(request, permissions):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return True
        if 'staff' in permissions and request.user.is_staff:
            return True
        if 'regular' in permissions and not request.user.is_staff:
            return True
    return False


class CustomLoginRequiredMixin(LoginRequiredMixin):
    permissions = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.permissions and not check_access(request, self.permissions):
            return self.handle_no_permission()

        return super().dispatch(request, *args,**kwargs)