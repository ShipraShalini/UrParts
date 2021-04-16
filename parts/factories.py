import string

from factory import Faker
from factory.django import DjangoModelFactory

from parts.models import Part


class PartFactory(DjangoModelFactory):
    """Declare factory to create Part objects."""

    class Meta:
        """Declare model class."""

        model = Part

    manufacturer = Faker("company")
    category = Faker("domain_word")
    model = Faker("pystr_format", letters=string.ascii_uppercase + string.digits)
    part = Faker("pystr_format", letters=string.ascii_uppercase + string.digits)
    part_category = Faker("pystr_format", letters=string.ascii_uppercase + " ")
