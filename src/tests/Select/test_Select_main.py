from ak_sap.Select.main import selected_parse


def test_selected_parse():
    ret = [0, (), (), 0]
    assert selected_parse(ret) == []

    ret = [3, (1, 1, 2), ("3", "5", "4"), 0]
    assert selected_parse(ret) == [
        {"ObjectType": "Point", "ObjectName": "3"},
        {"ObjectType": "Point", "ObjectName": "5"},
        {"ObjectType": "Frame", "ObjectName": "4"},
    ]

    ret = [1, (1,), ("3",), 0]
    assert selected_parse(ret) == [{"ObjectType": "Point", "ObjectName": "3"}]
