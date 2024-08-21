import sys; sys.path.append("src")
from schemas.Process import ProcessSchema


def test_time_interval_without_days():
    process = ProcessSchema(
        id=1,
        process="apache",
        user="www",
        cpu=0.1,
        memory=0.1,
        command="apache",
        time="10:23:04"
    )
    result = process.time_interval
    expected = "10:23:04"
    assert expected == result

def test_time_interval_with_days():
    process = ProcessSchema(
        id=1,
        process="apache",
        user="www",
        cpu=0.1,
        memory=0.1,
        command="apache",
        time="2-43:23:04"
    )
    result = process.time_interval
    expected = "3 days, 19:23:04"
    assert expected == result


def test_time_interval_without_days_over_24_hours():
    process = ProcessSchema(
        id=1,
        process="apache",
        user="www",
        cpu=0.1,
        memory=0.1,
        command="apache",
        time="43:23:04"
    )
    result = process.time_interval
    expected = "1 day, 19:23:04"
    assert expected == result
