from uc.converter import ConversionGraph, Quantity
import pytest


@pytest.fixture(scope="session", params=["bfs", "dfs"])
def unit_registry(request) -> ConversionGraph:
    graph = ConversionGraph(search_algo=request.param)

    graph.add_unit("m", "length")
    graph.add_unit("cm", "length")
    graph.add_unit("mm", "length")
    graph.add_unit("mi", "length")
    graph.add_unit("km", "length")

    graph.add_linear("m", "cm", scale=100.0)
    graph.add_linear("cm", "mm", scale=10.0)
    graph.add_linear("mi", "km", scale=1.60934)
    return graph


def pytest_generate_tests(metafunc):
    if "test_conversions_with_metafunc" == metafunc.function.__name__:
        # expected_fixtures = ["from_value, from_unit, expected_value, to_unit"]
        # is_relevant_test = all(fixture in metafunc.fixturenames for fixture in expected_fixtures)
        # if is_relevant_test:
        metafunc.parametrize(
            "from_value, from_unit, expected_value, to_unit",
            [(0.5, "m", 500.0, "mm"), (1, "m", 1000.0, "mm"), (2.5, "m", 2500, "mm")],
        )


def test_conversions_with_metafunc(unit_registry, from_value, from_unit, expected_value, to_unit):
    from_quantity = Quantity(value=from_value, unit=from_unit)
    to_quantity = unit_registry.convert(from_quantity, to_unit)
    assert to_quantity.value == pytest.approx(expected_value)


@pytest.fixture(params=[(0.5, "m", 500.0, "mm"), (1, "m", 1000.0, "mm")], ids=lambda p: f"{p[0]}_{p[1]}_{p[2]}_{p[3]}")
def conversion_case(request):
    return request.param


def test_conversions_with_fixture_parametrization(unit_registry, conversion_case):
    from_value, from_unit, expected_value, to_unit = conversion_case
    from_quantity = Quantity(value=from_value, unit=from_unit)
    to_quantity = unit_registry.convert(from_quantity, to_unit)
    assert to_quantity.value == pytest.approx(expected_value)


@pytest.mark.parametrize(
    "from_value, from_unit, expected_value, to_unit", [(0.5, "m", 500.0, "mm"), (1, "m", 1000.0, "mm")]
)
def test_conversions_with_decorator_parametrization(unit_registry, from_value, from_unit, expected_value, to_unit):
    from_quantity = Quantity(value=from_value, unit=from_unit)
    to_quantity = unit_registry.convert(from_quantity, to_unit)
    assert to_quantity.value == pytest.approx(expected_value)


def test_conversion_unknow_units_fails(unit_registry):
    from_value = 1
    from_unit = "unknow_unit"
    to_unit = "mm"

    with pytest.raises(KeyError):
        from_quantity = Quantity(value=from_value, unit=from_unit)
        to_quantity = unit_registry.convert(from_quantity, to_unit)


def test_conversion_no_conv_path_fails(unit_registry):
    from_value = 1
    from_unit = "mi"
    to_unit = "mm"

    with pytest.raises(ValueError):
        from_quantity = Quantity(value=from_value, unit=from_unit)
        to_quantity = unit_registry.convert(from_quantity, to_unit)
