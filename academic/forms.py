from typing import Any
from django import forms
from django.contrib.auth import get_user_model

from . import models


class NilaiKHSInlineFormset(forms.models.BaseInlineFormSet):
    def get_huruf_mutu(self, nilai):
        if nilai > 80:
            return "A"
        elif nilai > 70:
            return "B"
        elif nilai > 60:
            return "C"
        elif nilai > 50:
            return "D"
        else:
            return "E"
        
    def get_angka_mutu(self, nilai):
        if nilai > 80:
            return 4
        elif nilai > 70:
            return 3
        elif nilai > 60:
            return 2
        else:
            return 1
        
    def set_auto_populated_attribute(self, obj, commit):
        obj.huruf_mutu = self.get_huruf_mutu(obj.nilai)
        obj.angka_mutu = self.get_angka_mutu(obj.nilai)
        
        #TODO: Violate the Single Responsibility Principle, Refactor it in the future
        if commit:
            obj.save()

        return obj
        
    def save_existing(self, form: Any, instance: Any, commit: bool = ...) -> Any:
        obj = super(NilaiKHSInlineFormset, self).save_existing(form, instance, commit)
        return self.set_auto_populated_attribute(obj, commit)
    
    def save_new(self, form: Any, commit: bool = ...) -> Any:
        obj = super(NilaiKHSInlineFormset, self).save_new(form, commit=False)
        return self.set_auto_populated_attribute(obj, commit)


class UserDosenAdminForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class UserDosenAdminFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = kwargs.get('instance')
        if obj and obj.user:
            self.user_form = UserDosenAdminForm(
                prefix='user', instance=obj.user
            )
        else:
            self.user_form = UserDosenAdminForm(prefix='user')

        self.user_fields = self.user_form.fields
        # Here we extend the main form fields with the fields 
        # coming from the SEOFlag model
        self.fields.update(self.user_form.fields)

        for field_name, value in self.user_form.initial.items():
            if field_name == 'id':
                continue
            self.initial[field_name] = value
 
    def add_prefix(self, field_name):
        """
        Ensure flag_form has a prefix appended to avoid field values crash on
        form submit and also set prefix on the main form if it exists as well.
        """
        if field_name in self.user_form.fields:
            prefix = (
                self.user_form.prefix
                if self.user_form.prefix
                else 'user'
            )
            return '%s-%s' % (prefix, field_name)
        return (
            '%s-%s' % (self.prefix, field_name)
            if self.prefix
            else field_name
        )
    
    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.user:
            user_form = UserDosenAdminForm(
                data=self.cleaned_data,
                files=self.cleaned_data,
                instance=instance.user
            )
        else:
            user_form = UserDosenAdminForm(
                data=self.cleaned_data,
                files=self.cleaned_data
            )


        if user_form.is_valid():
            user = user_form.save()
            if not instance.user:
                instance.user = user

        if commit:
            instance.save()

        return instance
        

class DosenAdminForm(UserDosenAdminFormMixin, forms.ModelForm):
    class Meta:
        model = models.Dosen
        exclude = ['user']
        
