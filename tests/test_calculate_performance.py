import pytest

from app.services.frankfurter import calculate_performance


class TestCalculatePerformance:

    def test_positive_change(self):
        result = calculate_performance(
            [5.00, 5.10, 5.25], "USD", "BRL", "2024-01-01", "2024-01-05"
        )

        assert result["initial_rate"] == 5.00
        assert result["final_rate"] == 5.25
        assert result["percentage_change"] == 5.0
        assert result["absolute_change"] == 0.25

    def test_negative_change(self):
        result = calculate_performance(
            [5.50, 5.20, 5.00], "USD", "BRL", "2024-01-01", "2024-01-05"
        )

        assert result["initial_rate"] == 5.50
        assert result["final_rate"] == 5.00
        assert result["percentage_change"] < 0
        assert result["absolute_change"] < 0

    def test_zero_change_constant_rate(self):
        result = calculate_performance(
            [1.00, 1.00, 1.00], "USD", "EUR", "2024-01-01", "2024-01-03"
        )

        assert result["percentage_change"] == 0.0
        assert result["absolute_change"] == 0.0

    def test_highest_and_lowest_rate(self):
        result = calculate_performance(
            [5.00, 5.50, 4.80, 5.25], "USD", "BRL", "2024-01-01", "2024-01-05"
        )

        assert result["highest_rate"] == 5.50
        assert result["lowest_rate"] == 4.80

    def test_rounding_to_4_decimal_places(self):
        result = calculate_performance(
            [3.123456789, 3.987654321], "USD", "EUR", "2024-01-01", "2024-01-02"
        )

        assert result["initial_rate"] == 3.1235
        assert result["final_rate"] == 3.9877

    def test_empty_rates_raises_exception(self):
        with pytest.raises(ValueError, match="Insufficient"):
            calculate_performance([], "USD", "BRL", "2024-01-01", "2024-01-05")

    def test_return_contains_all_expected_fields(self):
        result = calculate_performance(
            [5.00, 5.25], "USD", "BRL", "2024-01-01", "2024-01-05"
        )

        expected_fields = [
            "base_currency",
            "target_currency",
            "start_date",
            "end_date",
            "initial_rate",
            "final_rate",
            "percentage_change",
            "absolute_change",
            "highest_rate",
            "lowest_rate",
        ]
        for field in expected_fields:
            assert field in result, f"Missing field: {field}"

    def test_metadata_propagated_correctly(self):
        result = calculate_performance(
            [5.00, 5.25], "USD", "BRL", "2024-01-01", "2024-01-05"
        )

        assert result["base_currency"] == "USD"
        assert result["target_currency"] == "BRL"
        assert result["start_date"] == "2024-01-01"
        assert result["end_date"] == "2024-01-05"
