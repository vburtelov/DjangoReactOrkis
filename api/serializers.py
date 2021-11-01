from rest_framework import serializers
from rest_framework.fields import ChoiceField

from .models import Employee, Passport, Client, Organization, Country, City, PreAgreement, Currency, Hotel, Room,\
    Route, Tour, Contract, Payment, Voucher


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'


class PassportSerializer(serializers.ModelSerializer):
    type = ChoiceField(choices=Passport.PASSPORT_TYPE)

    class Meta:
        model = Passport
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class PreAgreementSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreAgreement
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tour
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class VoucherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voucher
        fields = '__all__'
