from django.db import models
from django.contrib.auth.models import User
import pandas as pd
from django.utils import timezone
import json
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext as _


mental_disorder_df = pd.read_csv('static/mentalDisorder.csv')
pcos_df = pd.read_csv('static/CLEAN- PCOS SURVEY SPREADSHEET.csv')
obesity_df = pd.read_csv('static/obesity_data.csv')


from django.contrib.auth.models import AbstractUser


class userHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_type = models.CharField(max_length = 120)
    symptoms = models.CharField(max_length = 500)
    result = models.CharField(max_length = 120)
    date = models.DateField(default=timezone.now)
    
    def set_symptoms(self, symptoms_list):
        self.symptoms = json.dumps(symptoms_list)

    def get_symptoms(self):
        return json.loads(self.symptoms)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)

    @property
    def bmi(self):
        if self.height and self.weight:
            return round(self.weight / ((self.height / 100) ** 2), 2)
        return None


class mentalDisorder(models.Model):
    
    choices_dict = {}
    for column in mental_disorder_df.columns:
        unique_values = mental_disorder_df[column].unique()
        choices = [(val, val) for val in unique_values]
        choices_dict[column] = choices
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sadness = models.CharField(max_length=100, choices=choices_dict['Sadness'])
    euphoric = models.CharField(max_length=100, choices=choices_dict['Euphoric'])
    exhausted = models.CharField(max_length=100, choices=choices_dict['Exhausted'])
    sleep_disorder = models.CharField(max_length=100, choices=choices_dict['Sleep dissorder'])
    mood_swing = models.CharField(max_length=100, choices=choices_dict['Mood Swing'])
    suicidal_thoughts = models.CharField(max_length=100, choices=choices_dict['Suicidal thoughts'])
    anorxia = models.CharField(max_length=100, choices=choices_dict['Anorxia'])
    authority_respect = models.CharField(max_length=100, choices=choices_dict['Authority Respect'])
    try_explanation = models.CharField(max_length=100, choices=choices_dict['Try-Explanation'])
    aggressive_response = models.CharField(max_length=100, choices=choices_dict['Aggressive Response'])
    ignore_moveon = models.CharField(max_length=100, choices=choices_dict['Ignore & Move-On'])
    nervous_breakdown = models.CharField(max_length=100, choices=choices_dict['Nervous Break-down'])
    admit_mistakes = models.CharField(max_length=100, choices=choices_dict['Admit Mistakes'])
    overthink = models.CharField(max_length=100, choices=choices_dict['Overthinking'])
    sexual_activity = models.CharField(max_length=100, choices=choices_dict['Sexual Activity'])
    concentration = models.CharField(max_length=100, choices=choices_dict['Concentration'])
    optimisim = models.CharField(max_length=100, choices=choices_dict['Optimisim'])

class pcosDisorder(models.Model):
    BLOOD_GROUP_CHOICES = (
        ('11', 'A+'),
        ('12', 'A-'),
        ('13', 'B+'),
        ('14', 'B-'),
        ('15', 'O+'),
        ('16', 'O-'),
        ('17', 'AB+'),
        ('18', 'AB-'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period_frequency = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    gained_weight = models.BooleanField(max_length = 10, choices = ((1, 'YES'), (0, 'NO')))
    body_hair_growth = models.BooleanField(max_length = 10, choices = ((1, 'YES'), (0, 'NO')))
    skin_dark = models.BooleanField(max_length = 10, choices = ((1, 'YES'), (0, 'NO')))
    hair_problem = models.BooleanField(max_length = 10, choices = ((1, 'YES'), (0, 'NO')))
    pimples = models.BooleanField(max_length = 10, choices = ((1, 'YES'), (0, 'NO')))
    fast_food = models.BooleanField(max_length = 10, choices = ((1, 'YES'), (0, 'NO')))
    exercise = models.BooleanField(max_length = 10, choices = ((1, 'YES'), (0, 'NO')))
    mood_swing = models.BooleanField(max_length = 10, choices = ((1, 'YES'), (0, 'NO')))
    mentrual_regularity = models.BooleanField(max_length = 10, choices = ((1, 'YES'), (0, 'NO')))
    duration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    blood_grp = models.CharField(max_length=100, choices=BLOOD_GROUP_CHOICES)


class obesityDisorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activityLevel = models.CharField(max_length = 10, choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')))
    
class ObesityData(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length = 6)
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    activityLevel = models.FloatField()
    ObesityCategory = models.CharField(max_length = 20)
    
    def __str__(self) -> str:
        return self.ObesityCategory

    