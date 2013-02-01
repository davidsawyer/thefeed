from django.db import models

UPLOADER_CHOICES = (
                    ('C', 'Common User'),
                    ('N', 'Nutrition Kitchen'),
                    )

#UNIT_CHOICES = (
#                ('',''),
#                ('',''),
#                )

class Entry(models.Model):
    name =  models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Meal(models.Model):
    title		= models.CharField(max_length=100)
    slug		= models.SlugField(unique=True)
    image		= models.ImageField(upload_to='documents/')
    serves		= models.CharField(max_length=100, blank=True)
    instructions= models.CharField(max_length=3000, blank=True)
    time_period = models.CharField(max_length=100, blank=True)
    uploader	= models.CharField(max_length=1, choices=UPLOADER_CHOICES)
    date		= models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.title

class Ingredient(models.Model):
    name = models.CharField(max_length=200, blank=True)
    meal = models.ForeignKey(Meal)

    def __unicode__(self):
        return self.name

## maybe merge what's below with the Ingredients class
#class Measurement(models.Model):
#    amount = models.CharField(max_length=200, blank=True)
#    unit_of_measurement = models.CharField(choices=UNIT_CHOICES, blank=True)
#    ingredient = models.OneToOneField(Ingredient)
#
#    def __unicode__(self):
#        return u"%s %s" % (self.amount, self.unit_of_measurement)
