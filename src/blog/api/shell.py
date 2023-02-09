python manage.py shell

from app.models import ModelName
from app.api.serializers import ModelSerializer

obj = Model.objects.all().first()
obj = Model.objects.first()
obj = Model.objects.last()
obj.id
obj.title
obj_data = ModelSerializer(obj)
obj_data.data 
obj_data.data['one of the fields in ModelSerializer']

data = {
		"topic" : "history" ,
		"title" : "world war" ,
		"text" : "today is the day." ,
}

new_item = ModelSerializer(data=data)
new_item.initial_data
if new_item.is_valid():
	new_item.save()
else:
	print(new_item.errors)