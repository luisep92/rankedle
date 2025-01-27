from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
class Map(models.Model):
    id = models.CharField(max_length=7,
                          primary_key=True,
                          verbose_name="ID",
                          null=False,
                          blank=False)
    duration = models.SmallIntegerField(verbose_name="Duration(s)",
                                        null=False,
                                        blank=False)
    name = models.CharField(max_length=200,
                            verbose_name="Name",
                            null=False,
                            blank=False)
    subname = models.CharField(max_length=200,
                               verbose_name="Subname",
                               null=True,
                               blank=True)
    author = models.CharField(max_length=200,
                              verbose_name="Author",
                              null=True,
                              blank=True)
    mapper = models.CharField(max_length=200,
                              verbose_name="Mapper",
                              null=True,
                              blank=True)
    upload_date = models.DateField(verbose_name="Upload date",
                                   null=False,
                                   blank=False)
    download_url = models.CharField(max_length=2048,
                                    verbose_name="Download URL",
                                    null=False,
                                    blank=False)
    cover_url = models.CharField(max_length=2048,
                                 verbose_name="Cover URL",
                                 null=False,
                                 blank=False)

    class Meta:
        db_table = "Map"
        verbose_name = "Map"
        verbose_name_plural = "Maps"

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"


class Difficulty(models.Model):
    name = models.CharField(max_length=10,
                            verbose_name="Name",
                            null=False,
                            blank=False)

    class Meta:
        db_table = "Difficulty"
        verbose_name = "Difficulty"
        verbose_name_plural = "Difficulties"

    def __str__(self) -> str:
        return f"{self.name}"


class MapDifficulty(models.Model):
    map = models.ForeignKey(Map,
                            on_delete=models.CASCADE,
                            related_name="difficulties",
                            verbose_name="Map ID",
                            null=False,
                            blank=False)
    difficulty = models.ForeignKey(Difficulty,
                                   on_delete=models.CASCADE,
                                   verbose_name="Difficulty",
                                   null=False,
                                   blank=False)
    stars = models.DecimalField(max_digits=4,
                                decimal_places=2,
                                verbose_name="Stars",
                                null=True,
                                blank=True)

    class Meta:
        db_table = "MapDifficulty"
        verbose_name = "MapDifficulty"
        verbose_name_plural = "MapDifficulties"

    def __str__(self) -> str:
        return f"{self.difficulty} - {self.stars}"


class PermittedName(models.Model):
    map = models.ForeignKey(Map,
                            on_delete=models.CASCADE,
                            related_name="permitted_names",
                            null=False,
                            blank=False)
    name = models.CharField(max_length=200,
                            verbose_name="Name",
                            null=False,
                            blank=False)

    class Meta:
        db_table = "PermittedName"
        verbose_name = "PermittedName"
        verbose_name_plural = "PermittedNames"

    def __str__(self) -> str:
        return f"{self.name}"


class User(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name="User Name",
                            null=False,
                            blank=False)

    class Meta:
        db_table = "User"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return f"{self.name}"


class Score(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="scores",
                             null=False,
                             blank=False)
    map = models.ForeignKey(Map,
                            on_delete=models.CASCADE,
                            related_name="scores",
                            null=False,
                            blank=False)

    def __str__(self) -> str:
        return f"{self.user} - {self.map}"
