from weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    """Formats weather data in string"""
    return (
        f'{weather.weather_type.value}\n'
        f'Температура: {weather.temperature} °C, по ощущениям: {weather.feels_like} °C\n'
        f"Восход: {weather.sunrise.strftime('%H:%M')}\n"
        f"Закат: {weather.sunset.strftime('%H:%M')}"
    )
