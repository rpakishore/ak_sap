from ak_sap.Results.main import joint_displacements_parse, joint_reactions_parse


def test_joint_reactions():
    ret = [
        2,
        ("1", "1"),
        ("1", "1"),
        ("UDSTL1", "UDSTL2"),
        (None, None),
        (0.0, 0.0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        0,
    ]
    expected = [
        {
            "ObjectName": "1",
            "ElementName": "1",
            "LoadCase": "UDSTL1",
            "StepType": None,
            "StepNum": 0.0,
            "F1": 1,
            "F2": 2,
            "F3": 3,
            "M1": 4,
            "M2": 5,
            "M3": 6,
        },
        {
            "ObjectName": "1",
            "ElementName": "1",
            "LoadCase": "UDSTL2",
            "StepType": None,
            "StepNum": 0.0,
            "F1": 1,
            "F2": 2,
            "F3": 3,
            "M1": 4,
            "M2": 5,
            "M3": 6,
        },
    ]
    assert joint_reactions_parse(ret=ret) == expected

    ret = [1, ("1",), ("1"), ("UDSTL1"), (None), (0.0), (1), (2), (3), (4), (5), (6), 0]

    assert joint_reactions_parse(ret=ret) == [
        {
            "ObjectName": ("1",),
            "ElementName": "1",
            "LoadCase": "UDSTL1",
            "StepType": None,
            "StepNum": 0.0,
            "F1": 1,
            "F2": 2,
            "F3": 3,
            "M1": 4,
            "M2": 5,
            "M3": 6,
        }
    ]


def test_joint_displacements():
    ret = [
        2,
        ("1", "1"),
        ("1", "1"),
        ("UDSTL1", "UDSTL2"),
        (None, None),
        (0.0, 0.0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        0,
    ]
    expected = [
        {
            "ObjectName": "1",
            "ElementName": "1",
            "LoadCase": "UDSTL1",
            "StepType": None,
            "StepNum": 0.0,
            "U1": 1,
            "U2": 2,
            "U3": 3,
            "R1": 4,
            "R2": 5,
            "R3": 6,
        },
        {
            "ObjectName": "1",
            "ElementName": "1",
            "LoadCase": "UDSTL2",
            "StepType": None,
            "StepNum": 0.0,
            "U1": 1,
            "U2": 2,
            "U3": 3,
            "R1": 4,
            "R2": 5,
            "R3": 6,
        },
    ]
    assert joint_displacements_parse(ret=ret) == expected

    ret = [1, ("1",), ("1"), ("UDSTL1"), (None), (0.0), (1), (2), (3), (4), (5), (6), 0]

    assert joint_displacements_parse(ret=ret) == [
        {
            "ObjectName": ("1",),
            "ElementName": "1",
            "LoadCase": "UDSTL1",
            "StepType": None,
            "StepNum": 0.0,
            "U1": 1,
            "U2": 2,
            "U3": 3,
            "R1": 4,
            "R2": 5,
            "R3": 6,
        }
    ]
