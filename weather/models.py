from django.db import models


class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def __eq__(self, other):
    	return self.name == other.name

    def __hash__(self):
      return hash(self.name)
