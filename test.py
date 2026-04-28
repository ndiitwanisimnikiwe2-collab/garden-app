"""
Basic unit tests for Garden App
"""

from advisor import GardenAdvisor


def test_season_mapping():
    advisor = GardenAdvisor()
    result = advisor.get_advice_by_month(1)
    assert isinstance(result, str)
    assert len(result) > 0


def test_plant_advice():
    advisor = GardenAdvisor()
    result = advisor.get_plant_advice("tomatoes")
    assert "sun" in result.lower()


def test_question_answering():
    advisor = GardenAdvisor()
    response = advisor.answer_question("How often should I water plants?")
    assert "water" in response.lower()