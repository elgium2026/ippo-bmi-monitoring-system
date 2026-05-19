from datetime import date
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    RANK_CHOICES = [
        ('PBGEN', 'PBGEN'), ('PCOL', 'PCOL'), ('PLTCOL', 'PLTCOL'), ('PMAJ', 'PMAJ'),
        ('PCPT', 'PCPT'), ('PLT', 'PLT'), ('PEMS', 'PEMS'), ('PCMS', 'PCMS'),
        ('PSMS', 'PSMS'), ('PMSg', 'PMSg'), ('PSSg', 'PSSg'), ('PCpl', 'PCpl'),
        ('Pat', 'Pat'), ('NUP', 'NUP'),
    ]
    CLASSIFICATION_CHOICES = [
        ('PCO', 'PCO'), ('PNCO', 'PNCO'), ('NUP', 'NUP'),
    ]
    UNIT_CHOICES = [
        ('PHQ', 'PHQ'), ('1st IPMFC', '1st IPMFC'), ('2nd IPMFC', '2nd IPMFC'),
        ('Aguinaldo MPS', 'Aguinaldo MPS'), ('Alfonso Lista MPS', 'Alfonso Lista MPS'),
        ('Asipulo MPS', 'Asipulo MPS'), ('Banaue MPS', 'Banaue MPS'), ('Hingyon MPS', 'Hingyon MPS'),
        ('Hungduan MPS', 'Hungduan MPS'), ('Kiangan MPS', 'Kiangan MPS'), ('Lagawe MPS', 'Lagawe MPS'),
        ('Lamut MPS', 'Lamut MPS'), ('Mayoyao MPS', 'Mayoyao MPS'), ('Tinoc MPS', 'Tinoc MPS'),
        ('Other Units (Please Specify)', 'Other Units (Please Specify)'),
    ]
    SEX_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    rank = models.CharField(max_length=15, choices=RANK_CHOICES)
    rank_classification = models.CharField(max_length=10, choices=CLASSIFICATION_CHOICES)
    middle_name = models.CharField(max_length=100, blank=True)
    qualifier = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    unit_other = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    height_cm = models.FloatField(null=True, blank=True)
    waist_cm = models.FloatField(null=True, blank=True)
    hip_cm = models.FloatField(null=True, blank=True)
    wrist_cm = models.FloatField(null=True, blank=True)
    must_change_password = models.BooleanField(default=True)
    admin_totp_secret = models.CharField(max_length=128, blank=True, null=True)
    is_personnel = models.BooleanField(default=True)

    PCO_RANKS = {'PBGEN', 'PCOL', 'PLTCOL', 'PMAJ', 'PCPT', 'PLT'}
    PNCO_RANKS = {'PEMS', 'PCMS', 'PSMS', 'PMSg', 'PSSg', 'PCpl', 'Pat'}

    @property
    def age(self):
        if not self.birthdate:
            return None
        today = date.today()
        years = today.year - self.birthdate.year
        if (today.month, today.day) < (self.birthdate.month, self.birthdate.day):
            years -= 1
        return years

    @property
    def bmi(self):
        if not self.height_cm or not self.weight_kg or self.height_cm <= 0:
            return None
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m * height_m), 1)

    @property
    def pnp_bmi_classification(self):
        bmi = self.bmi
        if bmi is None:
            return None
        if bmi <= 18.5:
            return 'UNDERWEIGHT'
        if bmi <= 25:
            return 'NORMAL'
        if bmi <= 26:
            return 'ACCEPTABLE BMI'
        if bmi <= 29.9:
            return 'OVERWEIGHT'
        if bmi <= 34.9:
            return 'OBESE CLASS 1'
        if bmi <= 39.9:
            return 'OBESE CLASS 2'
        return 'OBESE CLASS 3'

    @property
    def who_bmi_classification(self):
        bmi = self.bmi
        if bmi is None:
            return None
        if bmi < 18.5:
            return 'UNDERWEIGHT'
        if bmi <= 25:
            return 'NORMAL'
        if bmi < 30:
            return 'OVERWEIGHT'
        if bmi < 35:
            return 'OBESE CLASS 1'
        if bmi < 40:
            return 'OBESE CLASS 2'
        return 'OBESE CLASS 3'

    def _target_bmi(self):
        age = self.age or 0
        if age < 30:
            return 24.9
        if age <= 34:
            return 25
        if age <= 39:
            return 25.5
        if age <= 44:
            return 26
        if age <= 50:
            return 26.5
        return 27

    @property
    def max_normal_weight(self):
        if not self.height_cm:
            return None
        height_m = self.height_cm / 100
        return round((height_m * height_m) * self._target_bmi(), 1)

    @property
    def weight_to_lose(self):
        if self.weight_kg is None or self.max_normal_weight is None:
            return None
        result = round(self.weight_kg - self.max_normal_weight, 1)
        return result

    @property
    def remarks(self):
        category = self.pnp_bmi_classification
        if category == 'NORMAL':
            return 'Congratulations your BMI is Normal. Please maintain your healthy lifestyle.'
        if category == 'ACCEPTABLE BMI':
            return 'You look great, but try to exert more effort to have normal BMI.'
        if category == 'OVERWEIGHT':
            return 'Oh no, you are overweight! Diet, diet at exercise din pag may time.'
        if category == 'OBESE CLASS 1':
            return 'Ay Grabe ka naman. try your best to lose weight. Take care of your health.'
        if category in ('OBESE CLASS 2', 'OBESE CLASS 3'):
            return 'Warning! This is not good anymore. Please find time to be in good shape. Crave for a healthy body not foods.'
        if category == 'UNDERWEIGHT':
            return 'You are underweight. Please maintain a healthy diet and consult health staff if needed.'
        return None

    def save(self, *args, **kwargs):
        if self.rank in self.PCO_RANKS:
            self.rank_classification = 'PCO'
        elif self.rank in self.PNCO_RANKS:
            self.rank_classification = 'PNCO'
        else:
            self.rank_classification = 'NUP'

        if self.rank_classification == 'PCO':
            if self.first_name:
                self.first_name = self.first_name.upper()
            if self.middle_name:
                self.middle_name = self.middle_name.upper()
            if self.last_name:
                self.last_name = self.last_name.upper()
            if self.qualifier:
                self.qualifier = self.qualifier.upper()

        super().save(*args, **kwargs)

class LoginHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=150)
    action = models.CharField(max_length=80)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.username} - {self.action} - {self.timestamp:%Y-%m-%d %H:%M:%S}'
