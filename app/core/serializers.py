# import ulid
# from django.utils.translation import gettext as _
# from rest_framework import fields, serializers

# from . import models


# class ULIDField(fields.Field):
#     """
#     Django REST Framework (DRF) serializer field type for handling ULID's.
#     """
#     default_error_messages = {
#         'invalid': _('"{value}" is not a valid ULID.'),
#     }

#     def to_internal_value(self, data):
#         try:
#             return ulid.parse(data)
#         except (AttributeError, ValueError):
#             self.fail('invalid', value=data)

#     def to_representation(self, value):
#         return str(ulid.parse(value))


# serializers.ModelSerializer.serializer_field_ma\
# pping[models.ULIDField] = ULIDField
