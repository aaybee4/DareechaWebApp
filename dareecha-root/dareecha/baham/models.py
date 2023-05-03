from django.db import models as m
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
import datetime

from dareecha.baham.constants import colours, towns
from dareecha.baham.enum_types import VehicleType, VehicleStatus, UserType
from dareecha.baham.models import UserProfile, Vehicle

# Create your models here.

class ActivityLog(m.Model):
    ACTION_CHOICES = [
        {'C', 'CREATE'},
        {'U', 'UPDATE'},
        {'D', 'DELETE'}
        ]
    timestamp = m.DateTimeField(default=datetime.now)
    user = m.ForeignKey(UserProfile, on_delete=m.CASCADE)
    action = m.CharField(max_length=1, choices=ACTION_CHOICES)
    model = m.ForeignKey(Vehicle, on_delete=m.CASCADE)
    details = m.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user.username} - {self.get_action_display()} - {self.model} - {self.details}"

def validate_colour(value):
    '''
    Validate that the value exists in the list of available colours
    '''
    return value.upper() in colours

class VehicleModel(m.Model):
    model_id = m.AutoField(primary_key=True, db_column='id')
    vendor = m.CharField(max_length=20, null=False, blank=False)
    model = m.CharField(max_length=20, null=False, blank=False, default='Unknown')
    vtype = m.CharField(max_length=50, choices=[(t.name, t.value) for t in VehicleType])
    capacity = m.PositiveSmallIntegerField(null=False, default=2)

    class Meta:
        db_table = "baham_vehicle_model"


    def __str__(self):
        return f"{self.vendor} {self.model}"
    
class Vehicle(m.Model):
    model_id = m.AutoField(primary_key=True, db_column='VehicleId')
    registration_number = m.CharField(max_length=10, unique=True, null=False, blank=False, help_text="Unique registration/license plate no. of the vehicle.")
    color = m.CharField(max_length=50, default='white', validators=[validate_colour])
    model = m.ForeignKey(VehicleModel, null=False, on_delete=m.CASCADE)
    owner = m.ForeignKey(User, null=False, on_delete=m.CASCADE)
    date_added = m.DateField(m.DateTimeField(default=datetime.now, editable=False))
    status = m.CharField(max_length=50, choices=[(t.name, t.value) for t in VehicleStatus])

    def save(self,*args, **kwargs):
        is_new = not bool(self.pk)
        super().save(*args, **kwargs)
        if is_new:
            action = 'C'
            details = f'New Object created with Id {self.id}'
        else:
            action = 'U'
            details = f'Object updated with Id {self.id}'
        logEntry = ActivityLog(user=User.objects.get(id),
                           action=action, model=self, details=details)
        logEntry.save()
    
    def delete(self, using=None, keep_parents=False, request_user=None):
        if not request_user or not request_user.is_staff:
            raise PermissionDenied("You do not have permission to delete this object.")
        
        log_entry = ActivityLog(user=User.objects.get(id),
                              action='D',
                              model=self,
                              details=f'Object deleted with id {self.pk}')
        log_entry.save()
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"{self.model.vendor} {self.model.model} {self.colour}"


class UserProfile(m.Model):
    user = m.OneToOneField(User, on_delete=m.CASCADE)
    birthdate = m.DateField()
    gender = m.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    type = m.CharField(max_length=10, choices=[(t.name, t.value) for t in UserType])
    primary_contact = m.CharField(max_length=20, null=False, blank=False)
    alternate_contact = m.CharField(max_length=20, null=True)
    address = m.CharField(max_length=255)
    address_latitude = m.DecimalField(max_digits=9, decimal_places=6, null=True)
    address_longitude = m.DecimalField(max_digits=9, decimal_places=6, null=True)
    landmark = m.CharField(max_length=255, null=False)
    town = m.CharField(max_length=50, null=False, choices=[(c, c) for c in towns])
    date_created = m.DateField(auto_now_add=True)
    active = m.BooleanField(default=True, editable=False)
    date_deactivated = m.DateTimeField(editable=False, null=True)
    bio = m.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"






        
#class Contract(m.Model):
#    model_id = m.AutoField(primary_key=True, db_column='ContractId')
#    vehicle = m.ForeignKey(Vehicle, on_delete=m.CASCADE)
#    
#class UserLocal(m.Model):
#    model_id = m.OneToOneField(User,primary_key=True)
#
#class Owner(UserLocal):
#    model_id = m.AutoField(primary_key=True, db_column='OwnerId')
#    
#class Companion(UserLocal):
#    model_id = m.AutoField(primary_key=True, db_column='CompanionId')
#    contract = m.OneToOneField(Contract, on_delete=m.CASCADE)
