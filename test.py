"""
Basic unit tests for Garden App
"""

from advisor import GardenAdvisor


def test_season_mapping():
    advisor = GardenAdvisor()
    assert advisor.get_advice_by_month(1) is not None


def test_plant_advice():
    advisor = GardenAdvisor()
    assert "sun" in advisor.get_plant_advice("tomatoes").lower()


def test_question_answering():
    advisor = GardenAdvisor()
    response = advisor.answer_question("How often should I water plants?")
    assert "water" in response.lower()