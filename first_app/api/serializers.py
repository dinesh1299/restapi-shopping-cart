from rest_framework import serializers
from first_app.models import *

class RatingSerializer(serializers.ModelSerializer):
    product=serializers.CharField(source = 'product.name',read_only=True)
    class Meta:
        model = Ratings
        exclude = ['user']

class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        exclude = ['user','product']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Order
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name',read_only=True)
    # order = OrderSerializer(many=True,read_only=True)
    # ratings = RatingSerializer(many=True, read_only = True)
    class Meta:
        model = Product
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = Category
        fields = '__all__'


# def title_length(val):
#     if len(val)<3:
#         raise serializers.ValidationError('Title length should be greater than 2')

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)   
#     language = serializers.CharField()
#     title = serializers.CharField(validators=[title_length])
#     release = serializers.DateField()

#     def create(self, validated_data):
#         return movies.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.language = validated_data.get('language',instance.language)
#         instance.title = validated_data.get('title', instance.title)
#         instance.release = validated_data.get('release', instance.release)
#         instance.save()
#         return instance
    
#     def validate(self, attrs):
#         if attrs['title'] == attrs['language']:
#             raise serializers.ValidationError('Title and language should not same')
#         return attrs
    
#     def validate_language(self, value):
#         if value!='tamil':
#             raise serializers.ValidationError('Language shoulbd be tamil')
#         else:
#             return value