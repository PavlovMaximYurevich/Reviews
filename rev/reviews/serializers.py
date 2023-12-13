from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Review, Organization


class ReviewSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     slug_field='username',
    #     read_only=True,
    # )

    estimation = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ('id', 'text', 'organization', 'estimation', 'pub_date')
        read_only = ('id',)

    def validate(self, data):
        request = self.context.get('request')

        if request.method == 'POST':
            org_id = self.context['view'].kwargs.get('org_id')
            organization = get_object_or_404(Organization, pk=org_id)
            if Review.objects.filter(
                    # author=request.user,
                    organization=organization
            ).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв!')
        return data


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = (
            'id', 'full_name', 'short_name',
            'inn', 'factual_address',
            'date_added', 'longitude',
            'latitude', 'site',
            'email', 'is_gov',
            'is_full_time', 'about'
        )

    def create(self, validated_data):
        try:
            organization = super().create(validated_data)
            return organization
        except IntegrityError as e:
            raise serializers.ValidationError(
                'Организация с таким именем уже существует') from e

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret
