# coding: utf-8
from django.test import TestCase

from django.contrib.auth.models import User

from milkman.dairy import milkman

from mimesis.forms import AlbumForm
from mimesis.models import Album


class TestAlbumForm(TestCase):
    
    def setUp(self):
        self.user = milkman.deliver(User)
        self.user.set_password("letmein")
        self.user.save()
        self.album = milkman.deliver(Album, owner=self.user)
        
    def tearDown(self):
        self.user.delete()
        self.album.delete()
    
    def test_edit_album_form(self):
        data = {
            "name": "Eldarion Adventures",
            "description": "Photographs of the various Eldarion Team meetups.",
            "private": False
        }
        form = AlbumForm(data, instance=self.album)
        
        self.assertEquals(True, form.is_valid())
        instance = form.save()
        self.assertEquals(instance.name, data["name"])
        self.assertEquals(instance.description, data["description"])
        self.assertEquals(instance.private, data["private"])
    
    def test_new_album_form(self):
        data = {
            "name": "Eldarion Adventures",
            "description": "Photographs of the various Eldarion Team meetups.",
            "private": False
        }
        form = AlbumForm(data)
        self.assertEquals(True, form.is_valid())
        instance = form.save(commit=False)
        instance.owner = self.user
        instance.save()
        self.assertEquals(instance.name, data["name"])
        self.assertEquals(instance.description, data["description"])
        self.assertEquals(instance.private, data["private"])
        self.assertEquals(instance.owner, self.user)
    
    def test_new_album_invalid_form(self):
        form = AlbumForm()
        
        data = {
            "description": "Photographs of the various Eldarion Team meetups.",
            "private": False,
            "owner": self.user
        }
        form = AlbumForm(data)
        self.assertEquals(False, form.is_valid())
