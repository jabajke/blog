from django.contrib.auth.mixins import UserPassesTestMixin


class AdminPassTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
