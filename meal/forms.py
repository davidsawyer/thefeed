# -*- coding: utf-8 -*-
from django import forms

class MealForm(forms.Form):
    title       = forms.CharField(max_length=100, label="Name This Meal")
    image       = forms.FileField(label="Upload Photo")
    ingredients = forms.CharField(label="Ingredients (one per line)", max_length=1000, required=False, widget=forms.Textarea)
    instructions= forms.CharField(max_length=1000, required=False, widget=forms.Textarea)
    time_period = forms.CharField(label="Cook Time")
    serves      = forms.CharField(label="Number It Serves")
