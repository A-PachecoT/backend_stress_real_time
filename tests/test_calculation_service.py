import pytest
from app.services.calculation_service import CalculationService


def test_normalize():
    """Test value normalization"""
    assert CalculationService.normalize(85, 50, 120) == 0.5  # Middle value
    assert CalculationService.normalize(50, 50, 120) == 0.0  # Min value
    assert CalculationService.normalize(120, 50, 120) == 1.0  # Max value
    assert round(CalculationService.normalize(85, 50, 100), 2) == 0.70  # Custom range


def test_calculate_pss10():
    """Test PSS-10 score calculation"""
    # Test case with all zeros (minimum stress)
    assert CalculationService.calculate_pss10([0] * 10) == 0

    # Test case with all fours (maximum stress)
    assert CalculationService.calculate_pss10([4] * 10) == 40

    # Test case with inverse questions
    responses = [2] * 10  # All answers are 2
    score = CalculationService.calculate_pss10(responses)
    assert score == 20  # Should be 20 as inverse questions balance out


def test_calculate_stress_level():
    """Test stress level interpretation"""
    assert CalculationService.calculate_stress_level(0) == "Bajo"
    assert CalculationService.calculate_stress_level(13) == "Bajo"
    assert CalculationService.calculate_stress_level(14) == "Moderado"
    assert CalculationService.calculate_stress_level(26) == "Moderado"
    assert CalculationService.calculate_stress_level(27) == "Alto"
    assert CalculationService.calculate_stress_level(40) == "Alto"


def test_calculate_partial_index():
    """Test partial stress index calculation"""
    # Test with only required parameters
    ip = CalculationService.calculate_partial_index(
        heart_rate=85,  # Middle of range (50-120)
        temperature=36.5,  # Middle of range (35-38)
    )
    assert 0 <= ip <= 1  # Should be normalized between 0 and 1

    # Test with all parameters
    ip_full = CalculationService.calculate_partial_index(
        heart_rate=85,
        temperature=36.5,
        angular_velocity=0.1,  # Middle of range (0-0.2)
        facial_result=0.5,  # Already normalized
        pss10_response=20,  # Middle of range (0-40)
    )
    assert 0 <= ip_full <= 1


def test_calculate_total_stress_index():
    """Test total stress index calculation"""
    # Test with empty list
    assert CalculationService.calculate_total_stress_index([]) == 0.0

    # Test with single value
    assert CalculationService.calculate_total_stress_index([0.5]) == 0.5

    # Test with multiple values
    indices = [0.2, 0.4, 0.6, 0.8]
    assert CalculationService.calculate_total_stress_index(indices) == 0.5


@pytest.mark.asyncio
async def test_get_stress_analysis():
    """Test complete stress analysis"""
    # Test data
    sensor_data = [
        {"ritmo_cardiaco": 85, "temperatura": 36.5},
        {"ritmo_cardiaco": 90, "temperatura": 36.8},
    ]
    pss10_responses = [2] * 10  # All answers are 2

    # Get analysis
    analysis = await CalculationService.get_stress_analysis(
        sensor_data=sensor_data, pss10_responses=pss10_responses
    )

    # Verify response structure
    assert "timestamp" in analysis
    assert "total_stress_index" in analysis
    assert "pss10_score" in analysis
    assert "stress_level" in analysis
    assert "partial_indices" in analysis

    # Verify values
    assert 0 <= analysis["total_stress_index"] <= 1
    assert analysis["pss10_score"] == 20
    assert analysis["stress_level"] == "Moderado"
    assert len(analysis["partial_indices"]) == len(sensor_data)
