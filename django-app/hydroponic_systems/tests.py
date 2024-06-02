from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import HydroponicSystem, Measurement
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class HydroponicSystemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.hydroponic_system = HydroponicSystem.objects.create(owner=self.user, name='Test System')

    def test_create_hydroponic_system(self):
        """Test creating a new hydroponic system."""
        url = reverse('hydroponic-system-list')
        data = {'owner': self.user.id, 'name': 'New System'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HydroponicSystem.objects.count(), 2)

    def test_retrieve_hydroponic_system(self):
        """Test retrieving details of a hydroponic system."""
        url = reverse('hydroponic-system-detail', kwargs={'pk': self.hydroponic_system.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test System')

    def test_update_hydroponic_system(self):
        """Test updating details of a hydroponic system."""
        url = reverse('hydroponic-system-detail', kwargs={'pk': self.hydroponic_system.id})
        data = {
            'owner': self.user.id,
            'name': 'New System',
            'label': 'New Label', 
            'description': 'New Description', 
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New System')
        
    def test_partial_update_hydroponic_system(self):
        """Test partially updating details of a hydroponic system."""
        url = reverse('hydroponic-system-detail', kwargs={'pk': self.hydroponic_system.id})
        data = {'name': 'New System'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New System')

    def test_delete_hydroponic_system(self):
        """Test deleting a hydroponic system."""
        url = reverse('hydroponic-system-detail', kwargs={'pk': self.hydroponic_system.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HydroponicSystem.objects.count(), 0)

    def test_access_user_systems(self):
        """Test accessing hydroponic systems owned by other users."""
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.client.force_authenticate(user=other_user)
        url = reverse('hydroponic-system-detail', kwargs={'pk': self.hydroponic_system.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_hydroponic_system_by_created_at(self):
        """Test ordering hydroponic systems."""
        HydroponicSystem.objects.create(owner=self.user, name='System 1', created_at=datetime.now() - timedelta(days=3))
        HydroponicSystem.objects.create(owner=self.user, name='System 2', created_at=datetime.now() - timedelta(days=2))

        url = reverse('hydroponic-system-list')
        response = self.client.get(url, {'ordering': '-created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        systems = response.data['results']
        self.assertEqual(len(systems), 3)
        self.assertEqual(systems[2]['name'], 'Test System')
        self.assertEqual(systems[1]['name'], 'System 1')
        self.assertEqual(systems[0]['name'], 'System 2')

    def test_filter_hydroponic_system_by_created_at(self):
        """Test filtering hydroponic systems."""
        system = HydroponicSystem.objects.create(owner=self.user, name='New System', created_at=datetime.now() - timedelta(days=3))
        url = reverse('hydroponic-system-list')
        response = self.client.get(url, {'created_at__gte': system.created_at}) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        systems = response.data['results']
        self.assertEqual(len(systems), 1)
        self.assertEqual(systems[0]['name'], 'New System')  

 

class MeasurementTests(TestCase):
    def setUp(self):
        """Set up data for the tests with amount of measurements equal to 2."""

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.hydroponic_system = HydroponicSystem.objects.create(owner=self.user, name='Test System')
        self.measurement = Measurement.objects.create(
            system=self.hydroponic_system,
            pH=7.0,
            water_temperature=25.0,
            TDS=800.0
        )
        self.measurement2 = Measurement.objects.create(
            system=self.hydroponic_system,
            pH=6.5,
            water_temperature=24.5,
            TDS=750.0
        )

    def test_create_measurement(self):
        """Test creating a new measurement."""
        url = reverse('measurement-list')
        data = {
            'system': self.hydroponic_system.id,
            'pH': 7.0,
            'water_temperature': 26.0,
            'TDS': 850.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Measurement.objects.count(), 3)

    def test_retrieve_measurement(self):
        """Test retrieving details of a measurement."""
        url = reverse('measurement-detail', kwargs={'pk': self.measurement.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['pH']), 7.0)

    def test_update_measurement(self):
        """Test updating details of a measurement."""
        url = reverse('measurement-detail', kwargs={'pk': self.measurement.id})
        data = {
            'system': self.hydroponic_system.id,
            'pH': 7.5,
            'water_temperature': 27.0,
            'TDS': 650.0
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Measurement.objects.get(pk=self.measurement.id).pH, 7.5)

    def test_partial_update_measurement(self):
        """Test partially updating details of a measurement."""
        url = reverse('measurement-detail', kwargs={'pk': self.measurement.id})
        data = {'TDS': 900.0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Measurement.objects.get(pk=self.measurement.id).TDS, 900.0)

    def test_delete_measurement(self):
        """Test deleting a measurement."""
        url = reverse('measurement-detail', kwargs={'pk': self.measurement.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Measurement.objects.count(), 1)

    def test_permissions(self):
        """Test permissions for accessing measurements."""
        another_user = User.objects.create_user(username='anotheruser', password='testpassword')
        another_hydroponic_system = HydroponicSystem.objects.create(owner=another_user, name='Another System')
        another_measurement = Measurement.objects.create(
            system=another_hydroponic_system,
            pH=7.0,
            water_temperature=25.0,
            TDS=800.0
        )

        url = reverse('measurement-detail', kwargs={'pk': another_measurement.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_measurement_by_system(self):
        """Test filtering measurements by hydroponic system."""
        url = reverse('measurement-list')
        response = self.client.get(url, {'system': self.hydroponic_system.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_measurement_by_pH(self):
        """Test filtering measurements by pH."""
        url = reverse('measurement-list')
        response = self.client.get(url, {'pH__gte': 6.9})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 

    def test_order_measurement_by_created_at(self):
        """Test ordering measurements by created_at."""
        url = reverse('measurement-list')
        response = self.client.get(url, {'ordering': 'created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) 
        self.assertEqual(response.data['results'][0]['id'], self.measurement.id)
        self.assertEqual(response.data['results'][1]['id'], self.measurement2.id)

    def test_order_measurement_by_water_temperature_desc(self):
        """Test ordering measurements by water_temperature in descending order."""
        url = reverse('measurement-list')
        response = self.client.get(url, {'ordering': 'water_temperature'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][1]['id'], self.measurement.id)
        self.assertEqual(response.data['results'][0]['id'], self.measurement2.id)
