from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission,User
class Demo(models.Model):
    name=models.CharField(max_length=250)
    price=models.IntegerField()

    def __str__(self):
        return self.name

class PharmacyUser(AbstractUser):
    pharmacy_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    groups = models.ManyToManyField(Group, related_name="pharmacy_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="pharmacy_users_permissions", blank=True)

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.name} - {self.email}"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', null=True)
    name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.name} - {self.amount}"
    
class Medicine(models.Model):
    MEDICINE_TYPES = [
        ('Tablet', 'Tablet'),
        ('Syrup', 'Syrup'),
        ('Capsule', 'Capsule'),
        ('Injection', 'Injection'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=MEDICINE_TYPES)
    dosage = models.CharField(max_length=50)
    expiry_date = models.DateField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.dosage})"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} booked {self.medicine.name}"
    


    
class Medicines(models.Model):
    MEDICINE_TYPES = [
        ('Tablet', 'Tablet'),
        ('Syrup', 'Syrup'),
        ('Capsule', 'Capsule'),
        ('Injection', 'Injection'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=MEDICINE_TYPES)
    dosage = models.CharField(max_length=50)
    expiry_date = models.DateField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image2 = models.ImageField(upload_to='med/', blank=True, default='')

    def __str__(self):
        return f"{self.name} ({self.dosage})"
    