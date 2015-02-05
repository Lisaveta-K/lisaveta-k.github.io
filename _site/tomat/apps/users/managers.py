from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        user = self.model(email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None):
        user = self.model(email=email)
        user.status = self.model.STATUS_ADMIN
        user.set_password(password)
        user.save()

        return user

    def get_by_natural_key(self, username):
        return self.get(**{'%s__iexact' % self.model.USERNAME_FIELD: username})
