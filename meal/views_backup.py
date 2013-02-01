from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from thefeed.meal.models import Meal
from thefeed.meal.models import Ingredient
#from thefeed.meal.models import ShoppingList
from thefeed.meal.models import Entry
from thefeed.meal.forms import MealForm
import string
import random

def list(request):
    if request.method == 'POST':
        Entry.objects.all().delete()
    
    entries = Entry.objects.all()
    context = {'entries': entries}
    return render_to_response('list.html', context, context_instance=RequestContext(request))

def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
                        
            this_meal = Meal(title        = form.cleaned_data['title'],
                        image        = request.FILES['image'],
                        slug         = random_id(),
                        instructions = form.cleaned_data['instructions'],
                        time_period  = form.cleaned_data['time_period'],
                        serves       = form.cleaned_data['serves'],
                        uploader     = 'C',
                        )

            this_meal.save()

            
            all_ingredients = str(form.cleaned_data['ingredients']).split('\n')

            for line in all_ingredients:
                if len(line) > 2: # if line is not empty and later than or equal to a SPACE in ASCII
                    ingredient = Ingredient(name = line, meal = this_meal)
                    ingredient.save()
    

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('meal.views.upload'))
    else:
        form = MealForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response('upload.html', {'form': form}, context_instance=RequestContext(request))

# creates an id for each meal
def random_id(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def the_feed(request):
    meals = Meal.objects.all().order_by('?')
    context = {'meals': meals}
    return render_to_response('feed.html', context, context_instance=RequestContext(request))

def meal_details(request, mealslug):
    
    # set meal and ingredient objects
    meal = Meal.objects.get(slug=mealslug)
    ingredients = meal.ingredient_set.all()
    context = {'meal': meal, 'ingredients': ingredients}

    if request.method == 'POST':
        for ingredient in ingredients:
            entry = Entry(name = ingredient.name)
            entry.save()
        
    return render_to_response('recipe.html', context, context_instance=RequestContext(request))

def classes(request):
    return render_to_response('classes.html', None, context_instance=RequestContext(request))