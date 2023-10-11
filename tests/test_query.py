import pytest
from django.db.models import Q
from shared.utils.query import makeQuery

# Test cases for makeQuery function
test_cases = [
    # Equality checks
    ({"field1": {"_eq": 1}}, Q(field1=1)),
    ({"field1": {"_eq": "abc"}}, Q(field1="abc")),
    ({"field1": {"_neq": 1}}, ~Q(field1=1)),
    ({"field1": {"_neq": "abc"}}, ~Q(field1="abc")),
    ({"a": {"_eq": 5}}, Q(a=5)),
    ({"a": {"_neq": 5}}, ~Q(a=5)),
    ({"a": {"_in": [5]}}, Q(a__in=[5])),
    ({"a": {"_eq": 5}, "b": {"_eq": 6}}, Q(a=5, b=6)),
    ({"a__b": {"_eq": 5}}, Q(a__b=5)),
    ({"a": {"b": {"_eq": 5}}}, Q(a__b=5)),
    ({"a": {"b": {"c": {"_eq": 5}}}}, Q(a__b__c=5)),
    ({"a": {"b": {"c": {"_neq": 5}}}}, ~Q(a__b__c=5)),
    # Range checks
    ({"field1": {"_gt": 1}}, Q(field1__gt=1)),
    ({"field1": {"_gte": 1}}, Q(field1__gte=1)),
    ({"field1": {"_lt": 1}}, Q(field1__lt=1)),
    ({"field1": {"_lte": 1}}, Q(field1__lte=1)),
    # Membership checks (cont.)
    ({"field1": {"_in": [1, 2, 3]}}, Q(field1__in=[1, 2, 3])),
    ({"field1": {"_nin": [1, 2, 3]}}, ~Q(field1__in=[1, 2, 3])),
    # String matching checks
    ({"field1": {"_contains": "abc"}}, Q(field1__contains="abc")),
    ({"field1": {"_icontains": "abc"}}, Q(field1__icontains="abc")),
    ({"field1": {"_regex": "^abc"}}, Q(field1__regex="^abc")),
    # Conjunctions
    ({"_and": [{"a": {"_eq": 5}}, {"b": {"_eq": 6}}]}, Q(a=5, b=6)),
    ({"_and": [{"a": {"_eq": 5}}, {"b": {"_eq": 6}}]}, Q(a=5) & Q(b=6)),
    ({"_or": [{"a": {"_eq": 5}}, {"b": {"_eq": 6}}]}, Q(a=5) | Q(b=6)),
    ({"a": {"b": {"_or": [{"_eq": 5}, {"c": {"_eq": 4}}]}}}, Q(a__b=5) | Q(a__b__c=4)),
    (
        {
            "field1": {
                "_or": [
                    {"_eq": 1},
                    {"_eq": 2},
                    {"_eq": 3},
                ]
            }
        },
        Q(field1=1) | Q(field1=2) | Q(field1=3),
    ),
    (
        {
            "field1": {
                "_and": [
                    {"_eq": 1},
                    {"_eq": 2},
                    {"_eq": 3},
                ]
            }
        },
        Q(field1=1) & Q(field1=2) & Q(field1=3),
    ),
    (
        {
            "field1": {
                "_not": [
                    {"_eq": 1},
                    {"_eq": 2},
                    {"_eq": 3},
                ]
            }
        },
        ~(Q(field1=1) & Q(field1=2) & Q(field1=3)),
    ),
    # Nested queries
    (
        {
            "a": {
                "_not": [{"b": {"_eq": 7}}, {"c": {"_eq": 2}}],
            }
        },
        ~Q(a__b=7, a__c=2),
    ),
    (
        {
            "field1": {
                "_or": [
                    {"field2": {"_eq": 1}},
                    {"field2": {"_eq": 2}},
                    {"field2": {"_eq": 3}},
                ]
            }
        },
        Q(field1__field2=1) | Q(field1__field2=2) | Q(field1__field2=3),
    ),
    (
        {
            "a": {
                "_not": [{"b": {"_eq": 7}}, {"c": {"_neq": 2}}],
            }
        },
        ~(Q(a__b=7) & ~Q(a__c=2)),
    ),
]


# Test function for makeQuery
@pytest.mark.parametrize("query,expected", test_cases)
def test_make_query(query, expected):
    assert makeQuery(query) == expected
