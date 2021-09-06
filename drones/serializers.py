from rest_framework import serializers 
from drones.models import DroneCategory
from drones.models import Drone
from drones.models import Pilot
from drones.models import Competition

class DroneCategorySerializer(serializers.HyperLinkedModelSerializer):
    drones = serializers.HyperLinkedRelatedField(read_only = True, view_name = 'drone-detail', many = True)
    
    class Meta: 
        model = DroneCategory
        fields = (
            
            'url'
            'pk',
            'name',
            'drones',
            
        )
        
class DroneSerializer(serializers.HyperLinkedModelSerializer): 
    drone_category = serializers.SlugRelatedField(queryset = DroneCategory.objects.all(), slug_field = 'name')
    
    class Meta: 
        model = Drone
        fields = (
            
            'url',
            'name',
            'drone_category',
            'manufacturing_date',
            'has_it_competed',
            'inserted_timestamp'
        )
        
class CompetitionSerializer(serializers.HyperLinkedModelSerializer): 
    drone = DroneSerializer()
    
    class Meta:
        model = Competition
        fields = (
            
            'url',
            'pk',
            'distance_in_feet',
            'distance_achievement_date',
            'drone',
        )
        
class PilotSerializer(serializers.HyperLinkedModelSerializer): 
    competitions = CompetitionSerializer(many = True, read_only = True)
    gender = serializers.ChoiceField(choices = Pilot.GENDER_CHOICES)
    gender_description = serializers.CharField(source = 'get_gender_display', read_only = True)
    
    class Meta: 
        model = Pilot
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'races_count',
            'inserted_timestamps',
            'competitions'
        )

class PilotCompetitionSerializer(serializers.ModelSerializers): 
    pilot = serializers.SlugRelatedField(queryset = Pilot.objects.all(), slug_field = 'name')
    drone = serializers.SlugRelatedField(queryset = Drone.objects.all(), slug_field = 'name')
    
    class  Meta: 
        model = Competition
        fields = (
            'url',
            'pk',
            'distance_in_feet',
            'distance_achievement_date',
            'pilot',
            'drone'
        )