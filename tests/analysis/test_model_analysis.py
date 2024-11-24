
from numpy import array, inf
from numpy.testing import assert_array_equal
from pandas import DataFrame, Timestamp
from pytest import fixture, mark

from analysis.abroca import (
    Abroca,
    RocCurve,
)
from analysis.results import (
    ModelResult,
    Results,
    format_clf_params,
    get_num,
    try_array_float_list,
)


# Fixtures for sample data used across multiple tests
@fixture
def sample_arrays():
    return {
        "float_array": array([1.0, 2.0, 3.0]),
        "int_array": array([1, 2, 3]),
        "str_num_array": array(["1", "2", "3"]),
        "str_alpha_array": array(["a", "b", "c"]),
        "bool_array": array([True, False, True]),
        "zero_one_array": array([0, 1, 0]),
    }


@fixture
def sample_series():
    data = {
        "param1": [1, 2, 3],
        "param2": [0.1, 0.2, 0.3],
        "param3_id": [100, 101, 102],
        "n_jobs": [1, 2, 3],
        "warm_start": [1, 0, 1],
    }
    return DataFrame(data)


@fixture
def sample_y_true():
    return [0, 0, 1, 1]


@fixture
def sample_y_prob():
    return [0.1, 0.4, 0.35, 0.8]


@fixture
def sample_y_true_2():
    return [0, 1, 0, 1]


@fixture
def sample_y_prob_2():
    return [0.2, 0.3, 0.6, 0.7]


@fixture
def sample_X_test():
    return DataFrame({"test_split": [0, 0, 1, 1]})


# Parameterized tests for get_num function
@mark.parametrize(
    "input_str, expected_output",
    [
        ("123", 123),
        ("123.456", 123.456),
        ("abc", "abc"),
        (None, None),
        ("1e3", 1000.0),
        ("inf", inf),
        ("-inf", -inf),
    ],
)
def test_get_num(input_str, expected_output):
    """Test the get_num function with various inputs."""
    assert get_num(input_str) == expected_output


# Parameterized tests for try_array_float_list function
@mark.parametrize(
    "array_name, key, expected_result",
    [
        ("float_array", "param", [1.0, 2.0, 3.0]),
        ("str_num_array", "param", [1, 2, 3]),
        ("str_alpha_array", "param", ["a", "b", "c"]),
        ("bool_array", "param", [True, False, True]),
        ("zero_one_array", "warm_start", [False, True, False]),
        ("int_array", "n_jobs", [1, 2, 3]),
    ],
)
def test_try_array_float_list(sample_arrays, array_name, key, expected_result):
    """Test the try_array_float_list function with various arrays and keys."""
    array_ = sample_arrays[array_name]
    result = try_array_float_list(array_, key)
    assert result == expected_result


def test_format_clf_params(sample_series):
    """Test the format_clf_params function."""
    series = sample_series
    result = format_clf_params(series)

    expected_keys = ["clf__param1", "clf__param2", "clf__n_jobs", "clf__warm_start"]
    assert sorted(result.keys()) == sorted(expected_keys)
    assert result["clf__param1"] == [1, 2, 3]
    assert result["clf__param2"] == [0.1, 0.2, 0.3]
    assert result["clf__n_jobs"] == [1, 2, 3]
    assert result["clf__warm_start"] == [True, False, True]


def test_roccurve_initialization(sample_y_true, sample_y_prob):
    """Test that RocCurve can be initialized properly."""
    roc_curve = RocCurve(sample_y_true, sample_y_prob, X_test=None)

    assert roc_curve is not None
    assert isinstance(roc_curve, RocCurve)
    assert hasattr(roc_curve, "fpr")
    assert hasattr(roc_curve, "tpr")
    assert hasattr(roc_curve, "auc")
    assert roc_curve.auc >= 0


def test_abroca_initialization(
    sample_y_true,
    sample_y_prob,
    sample_y_true_2,
    sample_y_prob_2,
):
    """Test that Abroca can be initialized properly."""
    roc1 = RocCurve(sample_y_true, sample_y_prob, X_test=None)
    roc2 = RocCurve(sample_y_true_2, sample_y_prob_2, X_test=None)
    curve_dict = {"slice0": roc1, "slice1": roc2}

    abroca = Abroca(split_col="test_split", curve_dict=curve_dict)

    assert abroca is not None
    assert isinstance(abroca, Abroca)
    assert hasattr(abroca, "abroca")


def test_abroca_computation(
    sample_y_true,
    sample_y_prob,
    sample_y_true_2,
    sample_y_prob_2,
):
    """Test that Abroca computes the correct abroca value."""
    roc1 = RocCurve(sample_y_true, sample_y_prob, X_test=None)
    roc2 = RocCurve(sample_y_true_2, sample_y_prob_2, X_test=None)
    curve_dict = {"slice0": roc1, "slice1": roc2}

    abroca = Abroca(split_col="test_split", curve_dict=curve_dict)
    abroca_value = abroca.abroca

    assert abroca_value >= 0
    assert isinstance(abroca_value, float)


def test_modelresult_initialization():
    """Test that ModelResult can be initialized properly."""
    model_result = ModelResult(
        model_type="test_model",
        run_id=1,
        iter_id=1,
        mean_fit_time=0.1,
        std_fit_time=0.01,
        mean_score_time=0.05,
        std_score_time=0.005,
        mean_test_roc_auc=0.9,
        std_test_roc_auc=0.02,
        rank_test_roc_auc=1,
        timestamp=Timestamp("2023-01-01"),
        inc_aca=True,
        inc_dem=False,
        inc_eng=True,
        inc_all=False,
        splits_test_roc_auc=[0.88, 0.92],
        name="",
        params=[],
    )

    assert model_result is not None
    assert isinstance(model_result, ModelResult)
    expected_name = "test_model_1_1"
    assert model_result.name == expected_name


def test_results_initialization():
    """Test that Results can be initialized properly."""
    model_result = ModelResult(
        model_type="test_model",
        run_id=1,
        iter_id=1,
        mean_fit_time=0.1,
        std_fit_time=0.01,
        mean_score_time=0.05,
        std_score_time=0.005,
        mean_test_roc_auc=0.9,
        std_test_roc_auc=0.02,
        rank_test_roc_auc=1,
        timestamp=Timestamp("2023-01-01"),
        inc_aca=True,
        inc_dem=False,
        inc_eng=True,
        inc_all=False,
        splits_test_roc_auc=[0.88, 0.92],
        name="test_model",
        params=[],
    )

    results = Results(obj_list=[model_result])

    assert results is not None
    assert isinstance(results, Results)
    assert len(results) == 1


def test_results_get_splits():
    """Test the get_splits method of Results."""
    model_result1 = ModelResult(
        model_type="model1",
        run_id=1,
        iter_id=1,
        mean_fit_time=0.1,
        std_fit_time=0.01,
        mean_score_time=0.05,
        std_score_time=0.005,
        mean_test_roc_auc=0.9,
        std_test_roc_auc=0.02,
        rank_test_roc_auc=1,
        timestamp=Timestamp("2023-01-01"),
        inc_aca=True,
        inc_dem=False,
        inc_eng=True,
        inc_all=False,
        splits_test_roc_auc=[0.88, 0.92],
        name="model1",
        params=[],
    )

    model_result2 = ModelResult(
        model_type="model2",
        run_id=2,
        iter_id=2,
        mean_fit_time=0.2,
        std_fit_time=0.02,
        mean_score_time=0.06,
        std_score_time=0.006,
        mean_test_roc_auc=0.85,
        std_test_roc_auc=0.03,
        rank_test_roc_auc=2,
        timestamp=Timestamp("2023-01-02"),
        inc_aca=False,
        inc_dem=True,
        inc_eng=False,
        inc_all=True,
        splits_test_roc_auc=[0.83, 0.87],
        name="model2",
        params=[],
    )

    results = Results(obj_list=[model_result1, model_result2])
    splits = results.get_splits()

    assert len(splits) == 2
    assert_array_equal(splits[0], array([0.88, 0.92]))
    assert_array_equal(splits[1], array([0.83, 0.87]))


def test_results_do_friedman():
    """Test the do_friedman method of Results."""
    model_result1 = ModelResult(
        model_type="model1",
        run_id=1,
        iter_id=1,
        mean_fit_time=0.1,
        std_fit_time=0.01,
        mean_score_time=0.05,
        std_score_time=0.005,
        mean_test_roc_auc=0.95,
        std_test_roc_auc=0.01,
        rank_test_roc_auc=1,
        timestamp=Timestamp("2023-01-01"),
        inc_aca=True,
        inc_dem=False,
        inc_eng=True,
        inc_all=False,
        splits_test_roc_auc=[0.94, 0.96],
        name="model1",
        params=[],
    )

    model_result2 = ModelResult(
        model_type="model2",
        run_id=2,
        iter_id=2,
        mean_fit_time=0.2,
        std_fit_time=0.02,
        mean_score_time=0.06,
        std_score_time=0.006,
        mean_test_roc_auc=0.90,
        std_test_roc_auc=0.02,
        rank_test_roc_auc=2,
        timestamp=Timestamp("2023-01-02"),
        inc_aca=False,
        inc_dem=True,
        inc_eng=False,
        inc_all=True,
        splits_test_roc_auc=[0.89, 0.91],
        name="model2",
        params=[],
    )

    model_result3 = ModelResult(
        model_type="model3",
        run_id=3,
        iter_id=3,
        mean_fit_time=0.15,
        std_fit_time=0.015,
        mean_score_time=0.055,
        std_score_time=0.0055,
        mean_test_roc_auc=0.88,
        std_test_roc_auc=0.015,
        rank_test_roc_auc=3,
        timestamp=Timestamp("2023-01-03"),
        inc_aca=True,
        inc_dem=True,
        inc_eng=True,
        inc_all=False,
        splits_test_roc_auc=[0.87, 0.89],
        name="model3",
        params=[],
    )

    results = Results(obj_list=[model_result1, model_result2, model_result3])
    friedman_stat, p_value = results.do_friedman()

    assert friedman_stat >= 0
    assert 0 <= p_value <= 1


# Parameterized tests for ModelResult initialization with various inputs
@mark.parametrize(
    "model_type, run_id, iter_id, expected_name",
    [
        ("test_model", 1, 1, "test_model_1_1"),
        ("model_x", 2, 3, "model_x_2_3"),
    ],
)
def test_modelresult_name_generation(model_type, run_id, iter_id, expected_name):
    """Test that ModelResult generates the correct name."""
    model_result = ModelResult(
        model_type=model_type,
        run_id=run_id,
        iter_id=iter_id,
        mean_fit_time=0.1,
        std_fit_time=0.01,
        mean_score_time=0.05,
        std_score_time=0.005,
        mean_test_roc_auc=0.9,
        std_test_roc_auc=0.02,
        rank_test_roc_auc=1,
        timestamp=Timestamp("2023-01-01"),
        inc_aca=True,
        inc_dem=False,
        inc_eng=True,
        inc_all=False,
        splits_test_roc_auc=[],
        name="",
        params=[],
    )

    assert model_result.name == expected_name
