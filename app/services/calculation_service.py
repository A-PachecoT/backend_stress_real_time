from typing import List, Dict
from datetime import datetime


class CalculationService:
    # Updated weights and ranges based on new requirements
    WEIGHTS = {
        "temperatura": 0.1,
        "ritmo_cardiaco": 0.1,
        "indice_facial": 0.4,
        "indice_preguntas": 0.4,
    }

    RANGES = {
        "temperatura": (35, 42),
        "ritmo_cardiaco": (60, 100),
        "indice_facial": (0, 1),  # Already normalized
        "indice_preguntas": (0, 40),
    }

    @staticmethod
    def normalize(value: float, min_val: float, max_val: float) -> float:
        """Normalize a value between 0 and 1"""
        if min_val == max_val:  # To avoid division by zero
            return 0
        return (value - min_val) / (max_val - min_val)

    @classmethod
    def calculate_weighted_average(cls, values: List[float]) -> float:
        """
        Calculate the weighted average of normalized values.

        :param values: List of values in order [temperature, heart_rate, facial_index, questions_index]
        :return: Weighted average as a percentage
        """
        if len(values) != 4:
            raise ValueError(
                "Expected 4 values: temperature, heart_rate, facial_index, questions_index"
            )

        # Normalize values
        normalized_values = []
        for value, (param_name, (min_val, max_val)) in zip(values, cls.RANGES.items()):
            normalized_value = cls.normalize(value, min_val, max_val)
            normalized_values.append(normalized_value)

        # Calculate weighted average
        weighted_sum = sum(
            normalized_value * weight
            for normalized_value, weight in zip(normalized_values, cls.WEIGHTS.values())
        )

        # Convert to percentage
        return weighted_sum * 100

    @classmethod
    def calculate_pss10(cls, responses: List[int]) -> int:
        """Calculate PSS-10 score from responses"""
        if len(responses) != 10:
            raise ValueError("PSS-10 requires exactly 10 responses")
        return sum(responses)  # Simple sum as per new requirements

    @classmethod
    def calculate_stress_level(cls, stress_percentage: float) -> str:
        """Interpret stress level based on percentage"""
        if stress_percentage <= 33:
            return "Bajo"
        elif stress_percentage <= 66:
            return "Moderado"
        else:
            return "Alto"

    @classmethod
    async def get_stress_analysis(
        cls, sensor_data: List[Dict], pss10_responses: List[int] = None
    ) -> Dict:
        """Get complete stress analysis including PSS-10 and sensor data"""
        # Calculate PSS-10 score if responses provided
        questions_index = cls.calculate_pss10(pss10_responses) if pss10_responses else 0

        # Process latest sensor reading
        latest_reading = sensor_data[-1] if sensor_data else None
        if not latest_reading:
            raise ValueError("No sensor data available")

        # Prepare values for weighted average
        values = [
            latest_reading["temperatura"],
            latest_reading["ritmo_cardiaco"],
            latest_reading.get("indice_facial", 0),  # Default to 0 if not present
            questions_index,
        ]

        # Calculate stress percentage
        stress_percentage = cls.calculate_weighted_average(values)
        stress_level = cls.calculate_stress_level(stress_percentage)

        return {
            "timestamp": datetime.now(),
            "stress_percentage": stress_percentage,
            "stress_level": stress_level,
            "normalized_values": {
                "temperatura": cls.normalize(values[0], *cls.RANGES["temperatura"]),
                "ritmo_cardiaco": cls.normalize(
                    values[1], *cls.RANGES["ritmo_cardiaco"]
                ),
                "indice_facial": values[2],  # Already normalized
                "indice_preguntas": cls.normalize(
                    values[3], *cls.RANGES["indice_preguntas"]
                ),
            },
        }
