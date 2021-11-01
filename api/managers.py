from django.contrib.auth.base_user import BaseUserManager


class EmployeeManager(BaseUserManager):

    def create_user(self, username, first_name, last_name, middle_name, password=None):
        if not username:
            raise ValueError('Users must have an username')
        if not first_name:
            raise ValueError('Users must have an name')
        if not last_name:
            raise ValueError('Users must have an surname')
        if not middle_name:
            raise ValueError('Users must have an middlename')

        user = self.model(
            username=username,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, middle_name, password=None):

        user = self.create_user(
            password=password,
            username=username,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.userType = 'admin'
        user.save(using=self._db)
        return user
