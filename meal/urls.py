from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('meal.views',
                       (r'^admin/', include(admin.site.urls)),
                       (r'^$', 'the_feed'),
                       (r'^meal/(?P<mealslug>.*)$', 'meal_details'),
                       ('upload.html', 'upload'),
                       ('list.html', 'list'),
                       ('classes.html', 'classes'),
					   ('about.html','about'),
                       )
