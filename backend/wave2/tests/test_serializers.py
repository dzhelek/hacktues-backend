from unittest.mock import patch

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from wave2.models import FieldValidationDate, SmallInteger, Team, User
from wave2.serializers import date


def set_up(func):

    def setUp(self):
        self.data = {
            'first_name': 'First', 'last_name': 'Last',
            'email': 'firstlast@abv.bg', 'password': 'hello',
            'username': 'josen#3212', 'is_active': True, 'tshirt_size': 'l',
            'form': '11g', 'is_superuser': True
        }
        self.user = User.objects.create_user(**self.data)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        func(self)

    return setUp


class TestTeam(APITestCase):
    @set_up
    def setUp(self):
        self.min = 3
        self.max = 5
        self.max_teams = 2
        SmallInteger.objects.create(name='min_users_in_team', value=self.min)
        SmallInteger.objects.create(name='max_users_in_team', value=self.max)
        SmallInteger.objects.create(name='max_teams', value=self.max_teams)

        self.team = Team.objects.create()

    @staticmethod
    def create_users(count):
        for i in range(count):
            yield User.objects.create(username=str(i)).id

    def test_post_400_team_with_users_gt_the_maximum(self):
        data = {
            'name': 'hello',
            'github_link': 'https://github.com/././',
            'users': (
                [f'http://testserver/users/{i}/'
                 for i in self.create_users(self.max + 1)]
            ),
        }

        response = self.client.post('/teams/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_201_team_with_users_equal_to_the_maximum(self):
        data = {
            'name': 'hello',
            'github_link': 'https://github.com/././',
            'users': (
                [f'http://testserver/users/{i}/'
                 for i in self.create_users(self.max)]
            ),
        }

        response = self.client.post('/teams/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_400_team_with_users_gt_the_maximum(self):
        data = {
            'users': (
                [f'http://testserver/users/{i}/'
                 for i in self.create_users(self.max + 1)]
            ),
        }

        response = self.client.patch(f'/teams/{self.team.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_200_team_with_users_equal_to_the_maximum(self):
        data = {
            'users': (
                [f'http://testserver/users/{i}/'
                 for i in self.create_users(self.max)]
            ),
        }

        response = self.client.patch(f'/teams/{self.team.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_201_is_full_returns_false_when_not_confirmed(self):
        data = {
            'name': 'hello',
            'github_link': 'https://github.com/././',
            'users': [f'http://testserver/users/{self.user.id}/'],
            'is_full': True,
        }

        response = self.client.post('/teams/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(self.team.is_full, 'team should not be full')

    def test_patch_200_is_full_returns_false_when_not_confirmed(self):

        response = self.client.patch(f'/teams/{self.team.id}/',
                                     {'is_full': True})
        self.team.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.team.is_full, 'team should not be full')

    def test_patch_200_team_may_be_full_when_confirmed(self):
        self.team.users.set(
            [User.objects.create(username=str(i)) for i in range(self.min)]
        )

        response = self.client.patch(f'/teams/{self.team.id}/',
                                     {'is_full': True})
        self.team.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.team.is_full, 'team should be full')

    def test_post_201_maximum_teams_limit_exceeded_team_is_not_ready(self):
        data = {
            'name': 'hello',
            'github_link': 'https://github.com/././',
            'users': [f'http://testserver/users/{self.user.id}/'],
        }
        Team.objects.create(name='team')

        response = self.client.post('/teams/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(Team.objects.last().ready)

    def test_post_201_team_is_ready_if_confirmed_but_max_limit_exceeded(self):
        data = {
            'name': 'hello',
            'github_link': 'https://github.com/././',
            'users': [f'http://testserver/users/{i}/'
                      for i in self.create_users(self.min)],
        }
        Team.objects.create(name='team')

        response = self.client.post('/teams/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertAlmostEqual(Team.objects.last().ready, timezone.now(),
                               delta=timezone.timedelta(seconds=1))

    def test_patch_200_first_ready_team_gets_confirmed_on_team_unconf(self):
        self.team.confirmed = True
        self.team.save()
        team = Team.objects.create(name='team')
        team.confirmed = True
        team.save()
        ready_team = Team.objects.create(name='ready')
        ready_team.ready = timezone.now() - timezone.timedelta(days=1)
        ready_team.save()
        second_ready = Team.objects.create(name='second')
        second_ready.ready = timezone.now()
        second_ready.save()
        data = {'users': [f'http://testserver/users/{self.user.id}/']}

        response = self.client.patch(f'/teams/{self.team.id}/', data)
        self.team.refresh_from_db()
        ready_team.refresh_from_db()
        second_ready.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.team.confirmed, 'team should not be confirmed')
        self.assertTrue(ready_team.confirmed, 'team should get confirmed')
        self.assertIsNone(ready_team.ready, 'should not be ready')
        self.assertFalse(second_ready.confirmed, 'team shouldnt get confirmed')


class TestUserPasswordManagement(APITestCase):
    @set_up
    def setUp(self):
        pass

    def test_get_password_not_visible(self):
        response = self.client.get(f'/users/{self.user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)

    def test_post_password_is_hashed_correctly_on_creation(self):
        self.data['username'] = 'pass#9321'
        self.user.is_staff = True
        self.user.save()

        response = self.client.post('/users/', self.data)
        user = User.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password('hello'),
                        "Passsword created incorectly")

    def test_patch_password_is_hashed_correctly_on_update(self):
        user_id = self.user.id

        response = self.client.patch(f'/users/{user_id}/',
                                     {'password': 'pass'})
        user = User.objects.get(id=user_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password('pass'),
                        "Passsword updated incorectly")

    def test_put_password_is_not_changed_on_other_fields_update(self):
        user_id = self.user.id
        del self.data['password']

        response = self.client.put(f'/users/{user_id}/', self.data)
        user = User.objects.get(id=user_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password('hello'),
                        "Passsword should not be changed")

    def test_put_password_is_not_changed_if_blank(self):
        """
        When making PUT request from drf generated html,
        blank password is sent as the password is in the
        serializer fields
        """
        user_id = self.user.id
        self.data['password'] = ''

        response = self.client.put(f'/users/{user_id}/', self.data)
        user = User.objects.get(id=user_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password('hello'),
                        "Passsword should not be changed")


@patch('wave2.serializers.date', autospec=True)
class TestUserFieldValidationOnSpecificDates(APITestCase):
    @set_up
    def setUp(self):
        pass

    def test_get_200(self, *args):
        response = self.client.get(f'/users/{self.user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_field_uneditable_on_this_date_400(self, date_mock):
        date_mock.today.return_value = date(2019, 1, 2)  # today is 2.1.2019
        validation_date = date(2019, 1, 1)  # 1.1.2019 - befote today
        FieldValidationDate.objects.create(field='tshirt_size',
                                           date=validation_date)
        user_id = self.user.id

        response = self.client.patch(f'/users/{user_id}/',
                                     {'tshirt_size': 'm'})
        user = User.objects.get(id=user_id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.tshirt_size, 'l')

    def test_patch_field_editable_on_this_date_200(self, date_mock):
        date_mock.today.return_value = date(2019, 1, 2)  # today is 2.1.2019
        validation_date = date(2019, 1, 2)
        FieldValidationDate.objects.create(field='tshirt_size',
                                           date=validation_date)
        user_id = self.user.id

        response = self.client.patch(f'/users/{user_id}/',
                                     {'tshirt_size': 'm'})
        user = User.objects.get(id=user_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.tshirt_size, 'm')

    def test_patch_field_uneditable_but_not_edited_200(self, date_mock):
        date_mock.today.return_value = date(2019, 1, 2)  # today is 2.1.2019
        validation_date = date(2019, 1, 1)  # 1.1.2019 - befote today
        FieldValidationDate.objects.create(field='tshirt_size',
                                           date=validation_date)
        user_id = self.user.id

        response = self.client.patch(f'/users/{user_id}/',
                                     {'tshirt_size': 'l'})
        user = User.objects.get(id=user_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.tshirt_size, 'l')

    def test_patch_editable_field_200(self, date_mock):
        user_id = self.user.id

        response = self.client.patch(f'/users/{user_id}/',
                                     {'first_name': 'First name'})
        user = User.objects.get(id=user_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.first_name, 'First name')

    def test_patch_one_editable_one_uneditable_on_date_400(self, date_mock):
        date_mock.today.return_value = date(2019, 1, 2)  # today is 2.1.2019
        validation_date1 = date(2019, 1, 1)  # 1.1.2019 - befote today
        validation_date2 = date(2019, 1, 2)  # today
        FieldValidationDate.objects.create(field='alergies',
                                           date=validation_date1)
        FieldValidationDate.objects.create(field='tshirt_size',
                                           date=validation_date2)
        user_id = self.user.id

        response = self.client.patch(f'/users/{user_id}/',
                                     {'tshirt_size': 'm', 'alergies': 'no'})
        user = User.objects.get(id=user_id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.tshirt_size, 'l')
        self.assertFalse(user.alergies,
                         'alergies changed after validation date')
