from collections import OrderedDict
from datetime import date

from django.utils import timezone
from django_email_verification import send_email as sendConfirm
from rest_framework import serializers

from .models import FieldValidationDate, SmallInteger, Team, Technology, User


class ModifiedRelatedField(serializers.RelatedField):
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])


class UserField(ModifiedRelatedField):
    queryset = User.objects.all()

    def to_internal_value(self, data):
        return User.objects.get(id=int(data))

    def to_representation(self, value):
        return {
            'id': value.id,
            'first_name': value.first_name,
            'last_name': value.last_name,
            'email': value.email,
            'form': value.form,
            'is_captain': value.is_captain,
            'discord_id': value.discord_id,
        }


class TechnologyField(serializers.StringRelatedField):
    def to_internal_value(self, data):
        return Technology.objects.get(name=data)


class TeamSerializer(serializers.ModelSerializer):
    users = UserField(many=True)
    technologies = TechnologyField(many=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'github_link', 'is_full', 'confirmed',
                  'project_name', 'project_description', 'users',
                  'technologies', 'captain')
        read_only_fields = 'confirmed',

    def create(self, validated_data):
        self.check_editable()
        max_teams = SmallInteger.objects.get(name='max_teams').value
        users = validated_data.get('users')
        self.check_users_count(users)
        self.check_not_in_team(users)

        instance = super().create(validated_data)

        if instance.is_confirmed is False:
            instance.is_full = False
        elif Team.objects.count() > max_teams:
            instance.ready = timezone.now()
        else:
            instance.confirmed = instance.is_confirmed

        instance.save()
        return instance

    def update(self, instance, validated_data):
        if users := validated_data.get('users'):
            self.check_users_count(users)
            before = [user for user in instance.users.all()]
            after = users
            if before != after:
                self.check_editable()
                users = [user for user in after if user not in before]
            if users:
                self.check_not_in_team(users)

        was_confirmed = instance.confirmed
        max_teams = SmallInteger.objects.get(name='max_teams').value

        instance = super().update(instance, validated_data)

        if instance.is_confirmed is False:
            instance.is_full = False
            instance.confirmed = False
            instance.save()
            if was_confirmed:
                team = Team.objects.filter(ready__lte=timezone.now()).first()
                if team:
                    team.ready = None
                    team.confirmed = True
                    team.save()
        elif Team.objects.count() > max_teams:
            instance.ready = timezone.now()
        else:
            instance.confirmed = instance.is_confirmed

        return instance

    @staticmethod
    def check_users_count(users):
        max_users = SmallInteger.objects.get(name='max_users_in_team').value
        if len(users) > max_users:
            err = 'reached maximum users in team limit'
            raise serializers.ValidationError(err)

    @staticmethod
    def check_editable():
        editable = FieldValidationDate.objects.get(field='team_editable').date
        if editable < date.today():
            err = f'team is not editable after {editable}'
            raise serializers.ValidationError(err)

    @staticmethod
    def check_not_in_team(users):
        if any(user.team_set.count() for user in users):
            err = 'one of the users already has team'
            raise serializers.ValidationError(err)


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_active', 'first_name', 'last_name', 'email',
                  'technologies', 'form', 'food_preferences', 'tshirt_size',
                  'alergies', 'is_online', 'password', 'phone',
                  'team_set', 'discord_id', 'avatar', 'is_captain')
        read_only_fields = 'team_set', 'is_active'
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def confirm_user(user):
        try:
            sendConfirm(user)
        except Exception as e:
            with open('email_log.txt', 'a') as f:
                f.write(str(e) + '\n')

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(instance.password)
        instance.save()
        self.confirm_user(instance)
        return instance

    def update(self, instance, validated_data):
        initial_email = instance.email
        initial_password = instance.password
        if not validated_data.get('password'):
            validated_data['password'] = initial_password

        super().update(instance, validated_data)

        new_email = instance.email
        if initial_email != new_email:
            self.confirm_user(instance)
        new_password = instance.password
        if initial_password != new_password:
            instance.set_password(new_password)
            instance.save()
        return instance

    def is_valid(self, *args, **kwargs):
        """
        some fields should not be editable after specific date
        """
        for field_object in FieldValidationDate.objects.all():
            field = field_object.field
            # new_value = validaed_data.get(field) if field in validated_data
            if new_value := self.initial_data.get(field):
                try:
                    initial_value = getattr(self.instance, field)
                except AttributeError:
                    if field_object.date < date.today():
                        err = f'users not creatable after {field_object.date}'
                        raise serializers.ValidationError(err)
                    else:
                        continue

                if initial_value != new_value:
                    if field_object.date < date.today():
                        er = f'{field} was editable untill {field_object.date}'
                        raise serializers.ValidationError(er)

        return super().is_valid(*args, **kwargs)
