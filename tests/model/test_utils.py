from numpy import array
from numpy.testing import assert_array_equal
from pandas import DataFrame, Series
from pandas.testing import assert_frame_equal
from pytest import raises

from model.utils import (
    combine_domains,
    get_distinct_value_proportions,
    get_idx_val,
    get_list_difs,
    get_list_mids,
    get_rect_area,
    idx_list,
    lengthen_params_log,
    make_prop_dict,
    overwrite_std_params,
    percentiles,
    rm_pattern,
    unpack_clf_keys,
    unpack_clf_params,
    wo_ids,
)


def test_idx_list_zero():
    result = idx_list(0, 0)
    assert result == []


def test_idx_list_one_one():
    result = idx_list(1, 1)
    assert result == [(0, 0)]


def test_idx_list_two_three():
    result = idx_list(2, 3)
    expected = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    assert result == expected


def test_idx_list_negative():
    result = idx_list(-1, 2)
    assert result == []


def test_idx_list_zero_rows():
    result = idx_list(0, 5)
    assert result == []


def test_idx_list_zero_cols():
    result = idx_list(5, 0)
    assert result == []


# Test cases for unpack_clf_keys
def test_unpack_clf_keys_empty():
    params_dict = {}
    result = unpack_clf_keys(params_dict)
    assert result == []


def test_unpack_clf_keys_no_underscores():
    params_dict = {"param1": 10, "param2": 20}
    result = unpack_clf_keys(params_dict)
    assert result == ["param1", "param2"]


def test_unpack_clf_keys_single_underscore():
    params_dict = {"clf__param1": 10, "clf__param2": 20}
    result = unpack_clf_keys(params_dict)
    assert result == ["param1", "param2"]


def test_unpack_clf_keys_multiple_underscores():
    params_dict = {"step__clf__param1": 10, "step__clf__param2": 20}
    result = unpack_clf_keys(params_dict)
    assert result == ["param1", "param2"]


def test_unpack_clf_keys_mixed():
    params_dict = {"param1": 10, "clf__param2": 20, "step__clf__param3": 30}
    result = unpack_clf_keys(params_dict)
    assert result == ["param1", "param2", "param3"]


# Test cases for unpack_clf_params
def test_unpack_clf_params_empty():
    params_dict = {}
    result = unpack_clf_params(params_dict)
    assert result == {}


def test_unpack_clf_params_no_underscores():
    params_dict = {"param1": 10, "param2": 20}
    result = unpack_clf_params(params_dict)
    assert result == {"param1": 10, "param2": 20}


def test_unpack_clf_params_single_underscore():
    params_dict = {"clf__param1": 10, "clf__param2": 20}
    result = unpack_clf_params(params_dict)
    assert result == {"param1": 10, "param2": 20}


def test_unpack_clf_params_multiple_underscores():
    params_dict = {"step__clf__param1": 10, "step__clf__param2": 20}
    result = unpack_clf_params(params_dict)
    assert result == {"param1": 10, "param2": 20}


def test_unpack_clf_params_mixed():
    params_dict = {"param1": 10, "clf__param2": 20, "step__clf__param3": 30}
    result = unpack_clf_params(params_dict)
    assert result == {"param1": 10, "param2": 20, "param3": 30}


# Test cases for lengthen_params_log
def test_lengthen_params_log_basic():
    params_log = {"a": 1, "b": [2, 3], "c": None}
    result = lengthen_params_log(params_log)
    expected = {"a": [1, 1], "b": [2, 3], "c": [None, None]}
    assert result == expected


def test_lengthen_params_log_with_data_object():
    class DataObject:
        def __init__(self, data):
            self.data = array(data)

    params_log = {"a": 1, "b": [2, 3], "c": DataObject([4, 5, 6])}
    result = lengthen_params_log(params_log)
    expected = {"a": [1, 1, 1], "b": [2, 3], "c": [4, 5, 6]}
    assert result == expected


def test_lengthen_params_log_singletons():
    params_log = {"a": "test", "b": True, "c": 3.14}
    result = lengthen_params_log(params_log)
    expected = {"a": ["test"], "b": [True], "c": [3.14]}
    assert result == expected


def test_lengthen_params_log_mixed_lengths():
    params_log = {"a": [1], "b": [2, 3], "c": [4, 5, 6]}
    result = lengthen_params_log(params_log)
    expected = {"a": [1, 1, 1], "b": [2, 3], "c": [4, 5, 6]}
    assert result == expected


# Test cases for overwrite_std_params
def test_overwrite_std_params_all_true():
    clf_params = {"clf__param1": 10, "clf__param2": 20}
    std_params = {"param1": 1, "param2": 2, "param3": 3}
    result = overwrite_std_params(clf_params, std_params, all=True)
    expected = {"param1": [10], "param2": [20], "param3": [3]}
    assert result == expected


def test_overwrite_std_params_all_false():
    clf_params = {"clf__param1": 10, "clf__param2": 20}
    std_params = {"param1": 1, "param2": 2, "param3": 3}
    result = overwrite_std_params(clf_params, std_params, all=False)
    expected = {"param1": 10, "param2": 20, "param3": 3}
    assert result == expected


def test_overwrite_std_params_no_overlap():
    clf_params = {"clf__param4": 40}
    std_params = {"param1": 1, "param2": 2}
    result = overwrite_std_params(clf_params, std_params)
    expected = {"param1": [1], "param2": [2]}
    assert result == expected


def test_overwrite_std_params_extra_keys():
    clf_params = {"clf__param1": [10, 20], "clf__param2": [30, 40]}
    std_params = {"param1": 1, "param2": 2}
    result = overwrite_std_params(clf_params, std_params)
    expected = {"param1": [10, 20], "param2": [30, 40]}
    assert result == expected


# Test cases for get_props
def test_get_props_basic():
    series = Series([1, 2, 2, 3, 3, 3])
    result = get_distinct_value_proportions(series)
    expected = DataFrame({
        "value": [1, 2, 3],
        "frequency": [1, 2, 3],
        "proportion": [1 / 6, 2 / 6, 3 / 6],
    })
    assert_frame_equal(result.reset_index(drop=True), expected)


def test_get_props_empty_series():
    series = Series([], dtype=float)
    result = get_distinct_value_proportions(series)
    expected = DataFrame(columns=["value", "frequency", "proportion"])
    expected = expected.astype({
        "value": "float64",
        "frequency": "float64",
        "proportion": "float64",
    })
    assert_frame_equal(result, expected)


def test_get_props_single_value():
    series = Series([1, 1, 1, 1])
    result = get_distinct_value_proportions(series)
    expected = DataFrame({"value": [1], "frequency": [4], "proportion": [1.0]})
    assert_frame_equal(result.reset_index(drop=True), expected)


# Test cases for make_prop_dict
def test_make_prop_dict_basic():
    df = DataFrame({
        "col1": [1, 2, 2],
        "col2_id": [1, 2, 3],
        "col3": ["a", "b", "a"],
    })
    result = make_prop_dict(df)
    expected = {
        "col1": get_distinct_value_proportions(df["col1"]),
        "col3": get_distinct_value_proportions(df["col3"]),
    }
    assert "col2_id" not in result
    assert_frame_equal(result["col1"].reset_index(drop=True), expected["col1"])
    assert_frame_equal(result["col3"].reset_index(drop=True), expected["col3"])


# Test cases for rm_pattern
def test_rm_pattern_end():
    list_of_strs = ["test_id", "sample_id", "data", "id_test"]
    result = rm_pattern(list_of_strs, "_id", end=True)
    expected = ["data", "id_test"]
    assert result == expected


def test_rm_pattern_start():
    list_of_strs = ["id_test", "id_sample", "data", "test_id"]
    result = rm_pattern(list_of_strs, "id_", end=False)
    expected = ["data", "test_id"]
    assert result == expected


def test_rm_pattern_no_match():
    list_of_strs = ["test", "sample", "data"]
    result = rm_pattern(list_of_strs, "_id")
    assert result == list_of_strs


def test_rm_pattern_empty_list():
    list_of_strs = []
    result = rm_pattern(list_of_strs, "_id")
    assert result == []


def test_rm_pattern_short_strings():
    list_of_strs = ["a", "b", "_id"]
    result = rm_pattern(list_of_strs, "_id")
    expected = ["a", "b"]
    assert result == expected


# Test cases for wo_ids
def test_wo_ids():
    list_of_strs = ["test_id", "sample", "data_id"]
    result = wo_ids(list_of_strs)
    expected = ["sample"]
    assert result == expected


# Test cases for percentiles
def test_percentiles_quartiles():
    _list = [1, 2, 3, 4, 5, 6, 7, 8]
    result = percentiles(_list, tiles=4)
    expected = {"0": 1, 1: 2.75, 2: 4.5, 3: 6.25, 4: 8}
    assert result == expected


def test_percentiles_empty_list():
    _list = []
    with raises(IndexError):
        percentiles(_list)


def test_percentiles_non_integer_values():
    _list = [1.5, 2.5, 3.5, 4.5]
    result = percentiles(_list, tiles=2)
    expected = {"0": 1.5, 1: 3.0, 2: 4.5}
    assert result == expected


# Test cases for combine_domains
def test_combine_domains_basic():
    x1 = [1, 2, 3]
    x2 = [3, 4, 5]
    result = combine_domains(x1, x2)
    expected = array([1, 2, 3, 4, 5])
    assert_array_equal(result, expected)


def test_combine_domains_with_duplicates():
    x1 = [1, 2, 2, 3]
    x2 = [3, 3, 4, 5]
    result = combine_domains(x1, x2)
    expected = array([1, 2, 3, 4, 5])
    assert_array_equal(result, expected)


# Test cases for get_list_difs
def test_get_list_difs():
    _list = [5, 3, 2, 1]
    result = get_list_difs(_list)
    expected = [2, 1, 1]
    assert result == expected


def test_get_list_difs_single_element():
    _list = [1]
    result = get_list_difs(_list)
    expected = []
    assert result == expected


# Test cases for get_list_mids
def test_get_list_mids():
    _list = [1, 3, 5]
    result = get_list_mids(_list)
    expected = [2.0, 4.0]
    assert result == expected


def test_get_list_mids_single_element():
    _list = [1]
    result = get_list_mids(_list)
    expected = []
    assert result == expected


# Test cases for get_rect_area
def test_get_rect_area_positive():
    heights = [2, 3, 4]
    widths = [5, 6, 7]
    result = get_rect_area(heights, widths)
    expected = 2 * 5 + 3 * 6 + 4 * 7
    assert result == expected


def test_get_rect_area_negative_values():
    heights = [-2, -3, -4]
    widths = [5, 6, 7]
    result = get_rect_area(heights, widths)
    expected = abs(-2 * 5) + abs(-3 * 6) + abs(-4 * 7)
    assert result == expected


def test_get_rect_area_absolute_false():
    heights = [-2, -3, -4]
    widths = [5, 6, 7]
    result = get_rect_area(heights, widths, absolute=False)
    expected = -2 * 5 + -3 * 6 + -4 * 7
    assert result == expected


# Test cases for get_idx_val
def test_get_idx_val_basic():
    idx_counter = 0
    in_val = "b"
    in_list = ["a", "b", "c", "b"]
    out_list = [1, 2, 3, 4]
    result = get_idx_val(idx_counter, in_val, in_list, out_list)
    assert result == 2


def test_get_idx_val_with_counter():
    idx_counter = 2
    in_val = "b"
    in_list = ["a", "b", "c", "b"]
    out_list = [1, 2, 3, 4]
    result = get_idx_val(idx_counter, in_val, in_list, out_list)
    assert result == 4


def test_get_idx_val_value_error():
    idx_counter = 0
    in_val = "d"
    in_list = ["a", "b", "c"]
    out_list = [1, 2, 3]
    with raises(ValueError):
        get_idx_val(idx_counter, in_val, in_list, out_list)
