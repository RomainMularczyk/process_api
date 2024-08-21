import sys; sys.path.append("src")
from datetime import timedelta
from schemas.Process import ProcessSchema

def test_validate_time_with_days():
    time = "1-124:12:32"
    result = ProcessSchema.validate_time(time)
    expected = timedelta(
        days=1,
        hours=124,
        minutes=12,
        seconds=32
    )
    assert expected == result

def test_validate_time_no_day():
    time = "124:12:32"
    result = ProcessSchema.validate_time(time)
    expected = timedelta(
        hours=124,
        minutes=12,
        seconds=32
    )
    assert expected == result
