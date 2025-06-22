import pytest
from apps.employees.models import Passport

'''
@pytest.mark.django_db
def test_post_creation():
    post = Passport.objects.create(
        series="0000",
        number="000000",
        date_of_issue="2018-09-05",
        birthdate="1983-05-01",
        birthplace="Г. КАЗАНЬ РЕСПУБЛИКА ТАТАРСТАН",
        code="160-013",
    )
    assert post.series == "0000"
    assert post.number == "000000"
    assert post.date_of_issue == "2018-09-05"
    assert post.birthdate == "1983-05-01"
    assert post.birthplace == "Г. КАЗАНЬ РЕСПУБЛИКА ТАТАРСТАН"
    assert post.code == "160-013"
    assert Passport.objects.count() == 1
'''