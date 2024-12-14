import pytest

from app.services.calculation_service import CalculationService


def test_normalize():
    """Test value normalization"""
    assert CalculationService.normalize(80, 60, 100) == 0.5  # Middle value
    assert CalculationService.normalize(60, 60, 100) == 0.0  # Min value
    assert CalculationService.normalize(100, 60, 100) == 1.0  # Max value
    assert round(CalculationService.normalize(38.5, 35, 42), 2) == 0.50  # Temperature
    assert CalculationService.normalize(80, 80, 80) == 0  # Same min and max


def test_calculate_weighted_average():
    """Test weighted average calculation"""
    # Test case with middle values
    values = [38.5, 80, 0.5, 20]  # temp, heart_rate, facial, questions
    result = CalculationService.calculate_weighted_average(values)
    assert 0 <= result <= 100  # Result should be a percentage

    # Test with minimum values
    min_values = [35, 60, 0, 0]
    min_result = CalculationService.calculate_weighted_average(min_values)
    assert min_result == 0

    # Test with maximum values
    max_values = [42, 100, 1, 40]
    max_result = CalculationService.calculate_weighted_average(max_values)
    assert max_result == 100

    # Test invalid input
    with pytest.raises(ValueError):
        CalculationService.calculate_weighted_average([38.5, 80, 0.5])  # Missing value


def test_calculate_pss10():
    """Test PSS-10 score calculation"""
    # Test with all zeros
    assert CalculationService.calculate_pss10([0] * 10) == 0

    # Test with all fours
    assert CalculationService.calculate_pss10([4] * 10) == 40

    # Test with mixed values
    assert CalculationService.calculate_pss10([2] * 10) == 20

    # Test invalid input
    with pytest.raises(ValueError):
        CalculationService.calculate_pss10([1, 2, 3])  # Not enough responses


def test_calculate_stress_level():
    """Test stress level interpretation"""
    assert CalculationService.calculate_stress_level(0) == "Bajo"
    assert CalculationService.calculate_stress_level(33) == "Bajo"
    assert CalculationService.calculate_stress_level(34) == "Moderado"
    assert CalculationService.calculate_stress_level(66) == "Moderado"
    assert CalculationService.calculate_stress_level(67) == "Alto"
    assert CalculationService.calculate_stress_level(100) == "Alto"


@pytest.mark.asyncio
async def test_get_stress_analysis():
    """Test complete stress analysis"""
    # Test data
    sensor_data = [{"temperatura": 38.5, "ritmo_cardiaco": 80, "indice_facial": 0.5}]
    pss10_responses = [2] * 10  # All answers are 2 (total 20)

    # Get analysis
    analysis = await CalculationService.get_stress_analysis(
        sensor_data=sensor_data, pss10_responses=pss10_responses
    )

    # Verify response structure
    assert "timestamp" in analysis
    assert "stress_percentage" in analysis
    assert "stress_level" in analysis
    assert "normalized_values" in analysis

    # Verify values
    assert 0 <= analysis["stress_percentage"] <= 100
    assert analysis["stress_level"] in ["Bajo", "Moderado", "Alto"]
    assert len(analysis["normalized_values"]) == 4

    # Test with missing sensor data
    with pytest.raises(ValueError):
        await CalculationService.get_stress_analysis([], None)
