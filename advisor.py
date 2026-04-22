"""
Core logic for Garden App
Handles:
- Seasonal advice
- Plant advice
- Q&A system
- User configuration
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class GardenAdvisor:
    def __init__(self):
        self.data = self._load_json("data.json")
        self.config = self._load_user_config()
        self.month_to_season = self._map_month_to_season()

    def _load_json(self, file_name):
        path = Path(file_name)
        if not path.exists():
            raise FileNotFoundError(f"{file_name} not found.")
        with open(path, "r") as f:
            return json.load(f)

    def _load_user_config(self):
        path = Path("user_config.json")
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
        return {"hemisphere": "southern"}

    def save_user_config(self):
        with open("user_config.json", "w") as f:
            json.dump(self.config, f, indent=4)

    def _map_month_to_season(self):
        hemi = self.config.get("hemisphere", "southern")

        if hemi == "northern":
            return {
                12: "winter", 1: "winter", 2: "winter",
                3: "spring", 4: "spring", 5: "spring",
                6: "summer", 7: "summer", 8: "summer",
                9: "autumn", 10: "autumn", 11: "autumn"
            }

        return {
            12: "summer", 1: "summer", 2: "summer",
            3: "autumn", 4: "autumn", 5: "autumn",
            6: "winter", 7: "winter", 8: "winter",
            9: "spring", 10: "spring", 11: "spring"
        }

    def get_advice_by_month(self, month: int) -> str:
        if month not in self.month_to_season:
            raise ValueError("Month must be between 1 and 12.")

        season = self.month_to_season[month]
        return self.data["seasons"].get(season, "No advice available.")

    def get_current_advice(self) -> str:
        return self.get_advice_by_month(datetime.now().month)

    def get_plant_advice(self, plant: str) -> str:
        return self.data["plants"].get(
            plant.lower(),
            "No advice available for this plant."
        )

    def answer_question(self, question: str) -> str:
        question = question.lower()

        for topic in self.data["qa"].values():
            if any(keyword in question for keyword in topic["keywords"]):
                return topic["answer"]

        return "Sorry, I don’t have an answer for that yet."


class GardenCLI:
    def __init__(self):
        self.advisor = GardenAdvisor()

    def show_help(self):
        print("""
🌱 Available Commands:
------------------------------------------------
1-12                 → Get monthly advice
current              → Get current advice
plant <name>         → Get plant advice
ask <question>       → Ask gardening question
set hemisphere <h>   → Set hemisphere (northern/southern)
help                 → Show this menu
exit                 → Quit application
------------------------------------------------
""")

    def run(self):
        print("🌿 Welcome to the Garden App Pro 🌿")
        self.show_help()

        while True:
            command = input(">> ").strip().lower()

            if command == "exit":
                print("Goodbye! 🌱")
                break

            elif command == "help":
                self.show_help()

            elif command == "current":
                print(self.advisor.get_current_advice())

            elif command.startswith("plant "):
                plant = command.split(" ", 1)[1]
                print(self.advisor.get_plant_advice(plant))

            elif command.startswith("ask "):
                question = command.split(" ", 1)[1]
                print(self.advisor.answer_question(question))

            elif command.startswith("set hemisphere "):
                hemi = command.split(" ")[-1]
                if hemi in ["northern", "southern"]:
                    self.advisor.config["hemisphere"] = hemi
                    self.advisor.save_user_config()
                    print(f"Hemisphere set to {hemi}")
                else:
                    print("Invalid hemisphere.")

            elif command.isdigit():
                try:
                    print(self.advisor.get_advice_by_month(int(command)))
                except ValueError as e:
                    print(e)

            else:
                print("Invalid command. Type 'help'.")