from enum import Enum, unique

@unique
class Gender(Enum):
    F = 'Female'
    M = 'Male'
    N = 'None'


GENDER_CHOICES = (
    (Gender.F.value,    'Female'),
    (Gender.M.value,    'Male'),
    (Gender.N.value,    'None'),
)
assert set(s.value for s in Gender) == set(dict(GENDER_CHOICES))
