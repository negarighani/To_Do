from rest_framework import serializers
from tasks.models import Task

from rest_framework import serializers
from tasks.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields='__all__'
        read_only_fields = ['owner']
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().update(instance, validated_data) 

class TaskSerializerWithoutOwner(TaskSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('owner')  
        
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().update(instance, validated_data) 

class CommentSerializer(serializers.ModelSerializer):
    model = Comment
    fields = '__all__'
    

