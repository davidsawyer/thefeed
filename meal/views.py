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
import os, sys
from PIL import Image, ImageOps
import StringIO
from django.core.files import File
import hashlib

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
                             image       = request.FILES['image'],
                             #image        = request.FILES['image'].resize(250, Image.ANTIALIAS),
                             slug         = random_id(8),
                             instructions = form.cleaned_data['instructions'],
                             time_period  = form.cleaned_data['time_period'],
                             serves       = form.cleaned_data['serves'],
                             uploader     = 'C',
                             )

                ######################################################################################
                        #views.py

            try:
                im = handle_uploaded_image(this_meal.image)
                this_meal.image.save(im[0],im[1])
            except KeyError:
                this_meal.save()
            ######################################################################################
            # save the meal then save the image
            this_meal.save()
            #this_meal.image.save(compress(this_meal.image), "JPEG")

            all_ingredients = str(form.cleaned_data['ingredients']).split('\n')

            for line in all_ingredients:
                if len(line) > 2: # if line is not empty and later than or equal to a SPACE in ASCII
                    ingredient = Ingredient(name = line, meal = this_meal)
                    ingredient.save()
    

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('meal.views.the_feed'))
    else:
        form = MealForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response('upload.html', {'form': form}, context_instance=RequestContext(request))



def handle_uploaded_image(i):
    # read image from InMemoryUploadedFile
    str = ""
    for c in i.chunks():
        str += c
    
    # create PIL Image instance
    imagefile  = StringIO.StringIO(str)
    image = Image.open(imagefile)
    
    # if not RGB, convert
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")
    
    #define file output dimensions (ex 60x60)
    x = 250
    y = 250
    
    #get orginal image ratio
    img_ratio = float(image.size[0]) / image.size[1]
    
    # resize but constrain proportions?
    if x==0.0:
        x = y * img_ratio
    elif y==0.0:
        y = x / img_ratio
    
    # output file ratio
    resize_ratio = float(x) / y
    x = int(x); y = int(y)
    
    # get output with and height to do the first crop
    if(img_ratio > resize_ratio):
        output_width = x * image.size[1] / y
        output_height = image.size[1]
        originX = image.size[0] / 2 - output_width / 2
        originY = 0
    else:
        output_width = image.size[0]
        output_height = y * image.size[0] / x
        originX = 0
        originY = image.size[1] / 2 - output_height / 2
    
    #crop
    cropBox = (originX, originY, originX + output_width, originY + output_height)
    image = image.crop(cropBox)
    
    # resize (doing a thumb)
    image.thumbnail([x, y], Image.ANTIALIAS)
    
    # re-initialize imageFile and set a hash (unique filename)
    imagefile = StringIO.StringIO()
    filename = hashlib.md5(imagefile.getvalue()).hexdigest()+'.jpg'
    
    #save to disk
    imagefile = open(os.path.join('/tmp',filename), 'w')
    image.save(imagefile,'JPEG', quality=90)
    imagefile = open(os.path.join('/tmp',filename), 'r')
    content = File(imagefile)
    
    return (filename, content)






# compress image size
def compress(infile):
    size = 128, 128
    im = None
    outfile = os.path.splitext(infile)[0] + random_id(4)
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
        except IOError:
            print "cannot create thumbnail for '%s'" % infile
    return im

# creates an id for each meal
def random_id(size):
    chars=string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

def the_feed(request):
    meals = Meal.objects.all().order_by('-date')
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

def about(request):
    return render_to_response('about.html', None, context_instance=RequestContext(request))
