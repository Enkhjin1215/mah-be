from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone



class UserManager(BaseUserManager):
    def create_user(self, phone_number, firstname, surname, password=None):
        if not phone_number:
            raise ValueError('User must have a phone number')

        user = self.model(
            phone_number=phone_number,
            firstname=firstname,
            surname=surname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, firstname, surname, password):
        user = self.create_user(
            phone_number=phone_number,
            firstname=firstname,
            surname=surname,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(verbose_name='First Name', max_length=100)
    surname = models.CharField(verbose_name='Surname', max_length=100)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=20, unique=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['firstname', 'surname']

    def __str__(self):
        return f"{self.firstname} {self.surname}"

    class Meta:
        db_table = 'users'


class LotteryCampaign(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_ongoing(self):
        today = timezone.now().date()
        return self.is_active and self.start_date <= today <= self.end_date

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"

    class Meta:
        db_table = 'lottery_campaign'
        verbose_name = 'Lottery Campaign'
        verbose_name_plural = 'Lottery Campaigns'


class Lottery(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        REJECTED = 'rejected', 'Rejected'

    campaign = models.ForeignKey(LotteryCampaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='lotteries')
    phone_number = models.CharField(max_length=15)
    lottery_number = models.CharField(max_length=50, unique=True, blank=True)
    ebarimt_picture = models.FileField(upload_to='ebarimt_pictures/')
    aimag = models.CharField(max_length=50)
    sum = models.CharField(max_length=50)
    horoo = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        if not self.lottery_number:
            super().save(*args, **kwargs)
            self.lottery_number = f"LOT-{self.id:06d}"
            Lottery.objects.filter(pk=self.pk).update(lottery_number=self.lottery_number)
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone_number} - {self.lottery_number}"

    class Meta:
        db_table = 'lottery_table'
        verbose_name = 'Lottery'
        verbose_name_plural = 'Lotteries'
