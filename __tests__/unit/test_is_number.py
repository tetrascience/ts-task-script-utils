from task_script_utils.is_number import isnumber


def test_is_number():
    assert isnumber(10)
    assert isnumber("10")
    assert isnumber("NaN")

    assert not isnumber(True)
    assert not isnumber("cheese")
