from rest_framework import serializers
from libaray.models import Book 

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book 
        fields ='__all__'
        
    def validate_price(self, price): # la validateur pour le prix est positive > 0
        if price < 0:
            raise serializers.ValidationError('price must be > 0')
        return price 