from shared.utils.picking import pick


def test_pick():
    data = {
        "name": "John",
        "age": 30,
        "address": {"street": "123 Main St", "city": "Anytown", "zip": "12345"},
        "phoneNumbers": [
            {"type": "home", "number": "555-555-1234"},
            {"type": "work", "number": "555-555-5678"},
        ],
    }
    structure = {
        "name": True,
        "address": {"street": True, "city": True},
        "phoneNumbers": [{"type": True, "number": True}],
    }
    expected_output = {
        "name": "John",
        "address": {"street": "123 Main St", "city": "Anytown"},
        "phoneNumbers": [
            {"type": "home", "number": "555-555-1234"},
            {"type": "work", "number": "555-555-5678"},
        ],
    }
    output = pick(data, structure)
    assert output == expected_output
