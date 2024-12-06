from typing import List, Tuple, Dict
from datetime import datetime


class CalculationService:
    # Constants from the scripts
    PSS10_INVERSE_QUESTIONS = [3, 4, 6, 7, 9]  # 0-based indices
    WEIGHTS = {
        "pss10": 0.3,
        "heart_rate": 0.25,
        "temperature": 0.2,
        "angular_velocity": 0.15,
        "facial": 0.1,
    }
    LIMITS = {
        "heart_rate": (50, 120),
        "temperature": (35.0, 38.0),
        "angular_velocity": (0.0, 0.2),
    }

    @staticmethod
    def normalize(value: float, min_val: float, max_val: float) -> float:
        """Normalize a value between 0 and 1"""
        return (value - min_val) / (max_val - min_val)

    @classmethod
    def calculate_pss10(cls, responses: List[int]) -> int:
        """Calculate PSS-10 score from responses"""
        if len(responses) != 10:
            raise ValueError("PSS-10 requires exactly 10 responses")

        total = 0
        for i, response in enumerate(responses):
            if i in cls.PSS10_INVERSE_QUESTIONS:
                total += 4 - response  # Inverse scoring
            else:
                total += response
        return total

    @classmethod
    def calculate_stress_level(cls, pss10_score: int) -> str:
        """Interpret PSS-10 score"""
        if pss10_score <= 13:
            return "Bajo"
        elif pss10_score <= 26:
            return "Moderado"
        else:
            return "Alto"

    @classmethod
    def calculate_partial_index(
        cls,
        heart_rate: float,
        temperature: float,
        angular_velocity: float = 0.0,
        facial_result: float = 0.0,
        pss10_response: int = None,
    ) -> float:
        """Calculate partial stress index (IP)"""
        # Normalize physiological parameters
        hr_norm = cls.normalize(heart_rate, *cls.LIMITS["heart_rate"])
        temp_norm = cls.normalize(temperature, *cls.LIMITS["temperature"])

        # Base calculation with required parameters
        ip = (
            cls.WEIGHTS["heart_rate"] * hr_norm + cls.WEIGHTS["temperature"] * temp_norm
        )

        # Add optional parameters if provided
        if angular_velocity is not None:
            ang_norm = cls.normalize(angular_velocity, *cls.LIMITS["angular_velocity"])
            ip += cls.WEIGHTS["angular_velocity"] * ang_norm

        if facial_result is not None:
            ip += cls.WEIGHTS["facial"] * facial_result

        if pss10_response is not None:
            pss10_norm = pss10_response / 40  # Normalize PSS-10 score (max 40)
            ip += cls.WEIGHTS["pss10"] * pss10_norm

        return ip

    @classmethod
    def calculate_total_stress_index(cls, partial_indices: List[float]) -> float:
        """Calculate total stress index (ITE)"""
        if not partial_indices:
            return 0.0
        return sum(partial_indices) / len(partial_indices)

    @classmethod
    async def get_stress_analysis(
        cls, sensor_data: List[Dict], pss10_responses: List[int] = None
    ) -> Dict:
        """Get complete stress analysis including PSS-10 and sensor data"""

        # Calculate PSS-10 score if responses provided
        pss10_score = None
        stress_level = None
        if pss10_responses and len(pss10_responses) == 10:
            pss10_score = cls.calculate_pss10(pss10_responses)
            stress_level = cls.calculate_stress_level(pss10_score)

        # Calculate partial indices from sensor data
        partial_indices = []
        for data in sensor_data:
            ip = cls.calculate_partial_index(
                heart_rate=data["ritmo_cardiaco"],
                temperature=data["temperatura"],
                pss10_response=pss10_score if pss10_score else None,
            )
            partial_indices.append(ip)

        # Calculate total stress index
        ite = cls.calculate_total_stress_index(partial_indices)

        return {
            "timestamp": datetime.now(),
            "total_stress_index": ite,
            "pss10_score": pss10_score,
            "stress_level": stress_level,
            "partial_indices": partial_indices,
        }
