from unittest.mock import Mock, patch

import pytest
import requests

from app.services.frankfurter import (
    calculate_performance,
    get_exchange_rate,
    validate_dates,
)


class TestCalculatePerformance:

    # CÉNÁRIOS DE TESTE - FLUXO NORMAL

    def test_calculate_performance_positive_change(self):
        result = calculate_performance(
            [5.00, 5.10, 5.25], "USD", "BRL", "2024-01-01", "2024-01-05"
        )
        assert result["initial_rate"] == 5.00
        assert result["final_rate"] == 5.25
        assert result["percentage_change"] == 5.0
        assert result["absolute_change"] == 0.25

    def test_calculate_performance_negative_change(self):
        result = calculate_performance(
            [5.50, 5.20, 5.00], "USD", "BRL", "2024-01-01", "2024-01-05"
        )
        assert result["initial_rate"] == 5.50
        assert result["final_rate"] == 5.00
        assert result["percentage_change"] < 0
        assert result["absolute_change"] < 0

    def test_calculate_performance_zero_change_constant_rate(self):
        result = calculate_performance(
            [1.00, 1.00, 1.00], "USD", "EUR", "2024-01-01", "2024-01-03"
        )
        assert result["percentage_change"] == 0.0
        assert result["absolute_change"] == 0.0

    def test_calculate_performance_highest_and_lowest_rate(self):
        result = calculate_performance(
            [5.00, 5.50, 4.80, 5.25], "USD", "BRL", "2024-01-01", "2024-01-05"
        )
        assert result["highest_rate"] == 5.50
        assert result["lowest_rate"] == 4.80

    def test_calculate_performance_rounding_to_4_decimal_places(self):
        result = calculate_performance(
            [3.123456789, 3.987654321], "USD", "EUR", "2024-01-01", "2024-01-02"
        )
        assert result["initial_rate"] == 3.1235
        assert result["final_rate"] == 3.9877

    def test_calculate_performance_return_contains_all_expected_fields(self):
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

    def test_calculate_performance_metadata_propagated_correctly(self):
        result = calculate_performance(
            [5.00, 5.25], "USD", "BRL", "2024-01-01", "2024-01-05"
        )
        assert result["base_currency"] == "USD"
        assert result["target_currency"] == "BRL"
        assert result["start_date"] == "2024-01-01"
        assert result["end_date"] == "2024-01-05"

    def test_validate_dates_with_valid_range(self):
        assert validate_dates("2024-01-01", "2024-01-05") is None

    def test_validate_dates_with_same_day(self):
        assert validate_dates("2024-01-01", "2024-01-01") is None

    @patch("app.services.frankfurter.requests.get")
    def test_get_exchange_rate_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "amount": 1.0,
            "base": "EUR",
            "date": "2024-01-01",
            "rates": {"BRL": 5.35},
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        resultado = get_exchange_rate("EUR", "BRL")

        assert resultado == 5.35
        mock_get.assert_called_once()

    # CÉNÁRIOS DE TESTE - FLUXOS DE EXTENSÃO

    def test_calculate_performance_empty_rates_raises_exception(self):
        with pytest.raises(ValueError, match="Insufficient"):
            calculate_performance([], "USD", "BRL", "2024-01-01", "2024-01-05")

    def test_validate_dates_invalid_start_format_raises_error(self):
        with pytest.raises(ValueError, match="Dates must be in YYYY-MM-DD format"):
            validate_dates("01-01-2024", "2024-01-05")

    def test_validate_dates_invalid_end_format_raises_error(self):
        with pytest.raises(ValueError, match="Dates must be in YYYY-MM-DD format"):
            validate_dates("2024-01-01", "amanha")

    def test_validate_dates_reversed_range_raises_error(self):
        with pytest.raises(
            ValueError, match="Start date cannot be later than end date"
        ):
            validate_dates("2024-01-05", "2024-01-01")

    def test_calculate_performance_zero_initial_rate_prevents_division_error(self):
        result = calculate_performance(
            [0.00, 5.00], "USD", "BRL", "2024-01-01", "2024-01-02"
        )
        assert result["percentage_change"] == 0
        assert result["absolute_change"] == 5.0

    @patch("app.services.frankfurter.requests.get")
    def test_get_exchange_rate_raises_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error: Not Found"
        )
        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            get_exchange_rate("EUR", "MOEDA_FALSA")

    @patch("app.services.frankfurter.requests.get")
    def test_get_exchange_rate_raises_timeout_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        with pytest.raises(requests.exceptions.Timeout):
            get_exchange_rate("EUR", "BRL")

    @patch("app.services.frankfurter.requests.get")
    def test_get_exchange_rate_raises_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Failed to establish a new connection"
        )

        with pytest.raises(requests.exceptions.ConnectionError):
            get_exchange_rate("EUR", "BRL")

    @patch("app.services.frankfurter.requests.get")
    def test_get_exchange_rate_missing_rates_raises_key_error(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"error": "Algum erro da API"}
        mock_get.return_value = mock_response

        with pytest.raises(KeyError):
            get_exchange_rate("EUR", "BRL")

    @patch("app.services.frankfurter.requests.get")
    def test_get_exchange_rate_missing_currency_raises_key_error(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"USD": 1.15}}
        mock_get.return_value = mock_response

        with pytest.raises(KeyError):
            get_exchange_rate("EUR", "BRL")
