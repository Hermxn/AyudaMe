from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r"^\d{9}$", message="Only 9 digits are allowed.")
