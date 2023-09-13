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


def name_length(val):
    if len(val)<3:
        raise serializers.ValidationError('Name length should be greater than 2')

class OrderrSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)   
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    name = serializers.CharField(validators=[name_length])
    product=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),allow_null=True)
    dateOrdered=serializers.DateTimeField(read_only=True)
    ordered=serializers.BooleanField(default=False)
    

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user',instance.user)
        instance.name = validated_data.get('name', instance.name)
        instance.product = validated_data.get('product', instance.product)
        instance.dateOrdered = validated_data.get('dateOrdered', instance.dateOrdered)
        instance.ordered = validated_data.get('ordered', instance.ordered)
        instance.save()
        return instance
    
    def validate(self, attrs):
        if attrs['name'] == attrs['product']:
            raise serializers.ValidationError('Name and Product should not same')
        return attrs
    
    def validate_order(self, value):
        if value=='order':
            raise serializers.ValidationError("Name shouldn't be order")
        else:
            return value