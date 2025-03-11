import unittest

import pandas as pd
import pytest

from ak_sap.Database.tables import (
    _array_to_list_of_dicts,
    _array_to_pandas,
    flatten_dataframe,
)


# Test case with a valid input
def test_array_to_pandas_valid():
    headers = ("Name", "Age", "City")
    data = ("John", 25, "New York", "Alice", 30, "San Francisco")
    expected_df = pd.DataFrame(
        {
            "Name": ["John", "Alice"],
            "Age": [25, 30],
            "City": ["New York", "San Francisco"],
        }
    )
    result_df = _array_to_pandas(headers, data)
    pd.testing.assert_frame_equal(result_df, expected_df)


# Test case with an invalid input (array length is not divisible by header length)
def test_array_to_pandas_invalid_length():
    headers = ("Name", "Age", "City")
    data = ("John", 25, "New York", "Alice", 30)  # Missing City for Alice
    with pytest.raises(
        AssertionError,
        match=r"Array length \(\d+\) is not divisible by header length \(\d+\)",
    ):
        _array_to_pandas(headers, data)


# Test case with a valid input
def test_array_to_list_of_dicts_valid():
    headers = ("Name", "Age", "City")
    data = ("John", 25, "New York", "Alice", 30, "San Francisco")
    expected_list_of_dicts = [
        {"Name": "John", "Age": 25, "City": "New York"},
        {"Name": "Alice", "Age": 30, "City": "San Francisco"},
    ]
    result_list_of_dicts = _array_to_list_of_dicts(headers, data)
    assert result_list_of_dicts == expected_list_of_dicts


# Test case with an invalid input (array length is not divisible by header length)
def test_array_to_list_of_dicts_invalid_length():
    headers = ("Name", "Age", "City")
    data = ("John", 25, "New York", "Alice", 30)  # Missing City for Alice
    with pytest.raises(
        AssertionError,
        match=r"Array length \(\d+\) is not divisible by header length \(\d+\)",
    ):
        _array_to_list_of_dicts(headers, data)


class TestFlattenDataFrame(unittest.TestCase):
    def test_flatten_empty_dataframe(self):
        df = pd.DataFrame()
        result = flatten_dataframe(df)
        self.assertEqual(
            result,
            tuple(),
            "Flattening an empty dataframe should return an empty tuple",
        )

    def test_flatten_dataframe_with_values(self):
        data = {"A": [1, 2, 3], "B": ["a", "b", "c"], "C": [4.5, 6.7, 8.9]}
        df = pd.DataFrame(data)
        result = flatten_dataframe(df)
        expected = ("1", "a", "4.5", "2", "b", "6.7", "3", "c", "8.9")
        self.assertEqual(
            result,
            expected,
            "Flattening a dataframe with values should produce the correct tuple",
        )

    def test_flatten_dataframe_with_nan_values(self):
        data = {"A": [1, 2, None], "B": ["a", None, "c"], "C": [4.5, 6.7, 8.9]}
        df = pd.DataFrame(data)
        result = flatten_dataframe(df)
        expected = ("1.0", "a", "4.5", "2.0", None, "6.7", None, "c", "8.9")
        self.assertEqual(
            result,
            expected,
            "Flattening a dataframe with NaN values should produce the correct tuple",
        )

    def test_flatten_dataframe_with_empty_strings(self):
        data = {"A": [1, 2, ""], "B": ["a", "", "c"], "C": [4.5, 6.7, 8.9]}
        df = pd.DataFrame(data)
        result = flatten_dataframe(df)
        expected = ("1", "a", "4.5", "2", None, "6.7", None, "c", "8.9")
        self.assertEqual(
            result,
            expected,
            "Flattening a dataframe with empty strings should produce the correct tuple",
        )


if __name__ == "__main__":
    unittest.main()
