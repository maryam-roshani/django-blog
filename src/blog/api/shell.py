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