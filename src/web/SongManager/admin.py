import json
import os.path
from django import forms
from django.contrib import admin
from .models import Map, Difficulty, MapDifficulty, PermittedName, User, Score
from django.forms import BaseInlineFormSet, ModelForm

admin.site.site_header = "Rankedle Bot Administration"
admin.site.index_title = "RankedleBot"
admin.site.site_title = "Admin Panel"


def get_next_map():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'songs_to_add.json')

    if os.path.isfile(file_path):
        with open(file_path) as file:
            data = json.load(file)
            if data and 'difficulties' in data[0]:
                return data[1]
    return None


def BaseMapDifficultyFormSetWithParams(diffs, id):

    class BaseMapDifficultyFormSet(BaseInlineFormSet):

        def add_fields(self, form, index):
            super().add_fields(form, index)
            if diffs and index is not None:
                form.fields['map'].initial = id
                form.fields['difficulty'].initial = Difficulty.objects.get(
                    name=diffs[index][0])
                form.fields['stars'].initial = diffs[index][1]

    return BaseMapDifficultyFormSet


def BasePermittedNameFormsetWithParams(map):

    class BasePermittedNameFormset(BaseInlineFormSet):

        def add_fields(self, form, index):
            super().add_fields(form, index)
            if map and index is not None:
                form.fields['map'].initial = map['id']
                if index == 0:
                    form.fields['name'].initial = map['name']
                elif index == 1:
                    if map['subname']:
                        form.fields[
                            'name'].initial = f"{map['name']} {map['subname']}"

    return BasePermittedNameFormset


def MapDifficultyInLineWithParam(map):

    class AlwaysChangedModelForm(ModelForm):

        def has_changed(self):
            """ Should returns True if data differs from initial. 
            By always returning true even unchanged inlines will get validated and saved."""
            return True

    class MapDifficultyInLine(admin.TabularInline):
        model = MapDifficulty
        difficulties = map['difficulties'] if map else None
        id = map['id'] if map else None
        extra = len(difficulties) if difficulties else 1
        form = AlwaysChangedModelForm
        formset = BaseMapDifficultyFormSetWithParams(difficulties, id)

    return MapDifficultyInLine


def PermittedNameInlineWithParam(map):

    class AlwaysChangedModelForm(ModelForm):

        def has_changed(self):
            """ Should returns True if data differs from initial. 
            By always returning true even unchanged inlines will get validated and saved."""
            return True

    class PermittedNameInline(admin.TabularInline):
        model = PermittedName
        extra = 2 if map and map['subname'] else 1
        form = AlwaysChangedModelForm
        formset = BasePermittedNameFormsetWithParams(map)

    return PermittedNameInline


def MapAdminFormWithParam(map):

    class MapAdminForm(forms.ModelForm):

        class Meta:
            model = Map
            fields = "__all__"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if map and not self.instance.pk:
                self.fields['id'].initial = map['id']
                self.fields['duration'].initial = map['duration']
                self.fields['name'].initial = map['name']
                self.fields['subname'].initial = map['subname']
                self.fields['author'].initial = map['author']
                self.fields['mapper'].initial = map['mapper']
                self.fields['upload_date'].initial = map['upload_date']
                self.fields['download_url'].initial = map['downloadURL']
                self.fields['cover_url'].initial = map['coverURL']

    return MapAdminForm


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    fields = ('id', 'duration', 'name', 'subname', 'author', 'mapper',
              'upload_date', 'download_url', 'cover_url')
    list_display = ('id', 'name')
    map = get_next_map()
    form = MapAdminFormWithParam(map)
    inlines = [
        PermittedNameInlineWithParam(map),
        MapDifficultyInLineWithParam(map)
    ]


@admin.register(PermittedName)
class PermittedNameAdmin(admin.ModelAdmin):
    fields = ['name', 'map']
    list_display = ['name', 'map']


@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']


@admin.register(MapDifficulty)
class MapDifficultyAdmin(admin.ModelAdmin):
    fields = ('map', 'difficulty', 'stars')
    list_display = ('map', 'difficulty', 'stars')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    fields = ('user', 'map')
    list_display = ('user', 'map')
