from enum import Enum

class VehicleType(Enum):
    auto_rickshaw = 'Auto Rickshaw'
    sedan = 'Sedan'
    hatchback = 'Hatchback'
    suv = 'Sub-Urban Vehicle'
    van = 'Van'
    high_roof = 'High Roof'
    motorcycle = 'Motocycle'

class VehicleStatus(Enum):
    available = "Available"
    full = "Full"
    inactive = "Inactive"
    removed = "Removed"

class UserType(Enum):
    owner = "Owner"
    companion = "Companion"
