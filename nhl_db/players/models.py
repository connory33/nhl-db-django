from django.db import models

class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    triCode = models.CharField(max_length=3)
    teamLogo = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Player(models.Model):
    STATUS_CHOICES = [
        ('True', 'Active'),
        ('False', 'Inactive'),
    ]
    
    playerId = models.IntegerField(primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    heightInInches = models.IntegerField(null=True, blank=True)
    heightInCentimeters = models.IntegerField(null=True, blank=True)
    weightInPounds = models.IntegerField(null=True, blank=True) 
    weightInKilograms = models.IntegerField(null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    birthCountry = models.CharField(max_length=100, null=True, blank=True)
    shootsCatches = models.CharField(max_length=10, null=True, blank=True)
    isActive = models.CharField(max_length=5, choices=STATUS_CHOICES, default='True')
    sweaterNumber = models.CharField(max_length=3, null=True, blank=True)
    currentTeamID = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    class Meta:
        ordering = ['-playerId']
