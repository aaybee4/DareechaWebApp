from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.urls import reverse


from dareecha.baham.constants import COLOURS
from dareecha.baham.enum_types import VehicleStatus
from dareecha.baham.models import Vehicle, VehicleModel, UserProfile, ActivityLog

# Create your views here.
def view_home(request):
    temp = loader.get_template('index.html')
    context = {
        'p' : 'home'
    }
    return HttpResponse(temp.render(context, request))
    #return HttpResponse("<h1>Welcome to Baham</h1>")

def view_p1(request):
    temp = loader.get_template('page1.html')
    context = {
        'p' : 'p1'
    }
    return HttpResponse(temp.render(context, request))

def create_vehicle(request):
    template = loader.get_template('createvehicle.html')
    models = VehicleModel.objects.all().values_list('model_id', 'vendor', 'model', 'type').order_by('type', 'vendor', 'model').values()
    users = User.objects.filter(is_superuser=False, is_active=True).all().values_list('id', 'first_name', 'last_name', 'email').order_by('first_name', 'last_name').values()
    context = {
        "navbar": "vehicles",
        "models": models,
        "users": users,
        "colours": COLOURS,
    }
    return HttpResponse(template.render(context, request))


def save_vehicle(request):
    registration_number = request.POST.get('registrationNumberText', None)
    colour = request.POST.get('colourSelection', None)
    model_id = request.POST.get('modelSelection', None)
    owner_id = request.user.id
    status = request.POST.get('statusCheck', None)
    if not registration_number or not model_id or not owner_id:
        return HttpResponse('<h3 class="danger">Error! Required parameters are missing.<h3>')
    model = VehicleModel.objects.filter(pk=model_id).get()
    owner = UserProfile.objects.filter(pk=owner_id).get()
    obj = Vehicle(registration_number=registration_number, colour=colour, model=model, owner=owner.user, status=status)
    obj.save()
    return HttpResponseRedirect(reverse(view_p1))

def log_create_or_update(sender, instance, created, **kwargs):
    if created:
        action = 'C'
        details = f'New Object created with Id {instance.id}'
    else:
        action = 'U'
        details = f'Object updated with Id {instance.id}'
    logEntry = ActivityLog(user=User.objects.get(username = 'admin'),
                           action=action, model=instance, details=details)
    logEntry.save()

def log_delete(sender, instance, **kwargs):
    logEntry = ActivityLog(user=User.objects.get(username = 'admin'),
                           action='D', model=instance, details=f'Object Deleted with Id {instance.id}')
    logEntry.save()