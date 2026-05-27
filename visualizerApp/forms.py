from django import forms

class ProjectileForm(forms.Form):
    angle = forms.FloatField(
        label='Angle of launch (degrees)',
        min_value=0,
        max_value=90,
        initial=45,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2.5 rounded-lg border bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white focus:ring-green-500 focus:border-green-500',
            'placeholder': 'e.g., 45',
            'step': '1'
        })
    )
    velocity = forms.FloatField(
        label='Initial velocity (m/s)',
        min_value=0,
        initial=100,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2.5 rounded-lg border bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white focus:ring-green-500 focus:border-green-500',
            'placeholder': 'e.g., 100',
            'step': '1'
        })
    )
    initial_height = forms.FloatField(
        label='Initial height (meters)',
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2.5 rounded-lg border bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white focus:ring-green-500 focus:border-green-500',
            'placeholder': 'e.g., 0',
            'step': '1'
        })
    )
    # NO final_height field