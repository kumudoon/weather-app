import pytest
from unittest.mock import patch
from requests.exceptions import HTTPError, Timeout
from weather.apis import get_coordinates, get_current_weather

def test_get_coordinates_success():
    """    Test successful retrieval of coordinates for a valid city.
    """
    mock_response = {
        "results": [
            {"latitude": 12.34, "longitude": 56.78}
        ]
    }
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None
        lat, lon = get_coordinates("TestCity")
        assert lat == 12.34
        assert lon == 56.78

def test_get_coordinates_not_found():
    """ Test handling of a city not found error. """
    mock_response = {"results": []}
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None
        with pytest.raises(ValueError, match="City 'UnknownCity' not found."):
            get_coordinates("UnknownCity")

def test_get_temperature_success():
    """ Test successful retrieval of temperature in current weather data. """
    mock_response = {
        "current_weather": {
            "temperature": 21.5
        }
    }
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None
        temp = get_current_weather(12.34, 56.78)
        assert temp["temperature"] == 21.5


def test_get_weather_no_data():
    """ Test handling of no weather data found for given coordinates. """
    mock_response = {}
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None
        with pytest.raises(ValueError, match="Weather data not found."):
            get_current_weather(12.34, 56.78)

def test_get_coordinates_empty_city():
    """ Test handling of an empty city name. """
    with pytest.raises(ValueError):
        get_coordinates("")

def test_get_coordinates_rate_limit():
    """ Test handling of rate limit error when fetching coordinates. """
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = HTTPError("429 Client Error: Too Many Requests")
        with pytest.raises(HTTPError, match="429 Client Error"):
            get_coordinates("TestCity")

def test_get_weather_rate_limit():
    """ Test handling of rate limit error when fetching weather data. """
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = HTTPError("429 Client Error: Too Many Requests")
        with pytest.raises(HTTPError, match="429 Client Error"):
            get_current_weather(12.34, 56.78)

def test_get_coordinates_malformed_json():
    """ Test handling of malformed JSON response when fetching coordinates. """
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.return_value.json.side_effect = ValueError("No JSON object could be decoded")
        mock_get.return_value.raise_for_status = lambda: None
        with pytest.raises(ValueError, match="No JSON object could be decoded"):
            get_coordinates("TestCity")

def test_get_weather_malformed_json():
    """ Test handling of malformed JSON response when fetching weather data. """
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.return_value.json.side_effect = ValueError("No JSON object could be decoded")
        mock_get.return_value.raise_for_status = lambda: None
        with pytest.raises(ValueError, match="No JSON object could be decoded"):
            get_current_weather(12.34, 56.78)

def test_get_coordinates_timeout():
    """ Test handling of a timeout error when fetching coordinates. """
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.side_effect = Timeout("The request timed out")
        with pytest.raises(Timeout, match="timed out"):
            get_coordinates("TestCity")

def test_get_weather_timeout():
    """ Test handling of a timeout error when fetching current weather data. """
    with patch("weather.apis.requests.get") as mock_get:
        mock_get.side_effect = Timeout("The request timed out")
        with pytest.raises(Timeout, match="timed out"):
            get_current_weather(12.34, 56.78)

