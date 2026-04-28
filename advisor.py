"""
Core logic for Garden App
Handles:
- Seasonal advice
- Plant advice
- Q&A system
- User configuration
- CLI interface
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
    def __init__(self, data_file="data.json", config_file="user_config.json"):
        self.data_file = data_file
        self.config_file = config_file

        self.data = self._load_json(self.data_file)
        self.config = self._load_config()
        self.month_to_season = self._map_month_to_season()

    def _load_json(self, file_name):
        path = Path(file_name)
        if not path.exists():
            raise FileNotFoundError(f"{file_name} not found.")

        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"{file_name} contains invalid JSON.")

    def _load_config(self):
        path = Path(self.config_file)
        if path.exists():
            return self._load_json(self.config_file)
        return {"hemisphere": "southern"}

    def save_user_config(self):
        with open(self.config_file, "w") as f:
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
        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12.")

        season = self.month_to_season.get(month)
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
            for keyword in topic["keywords"]:
                if keyword in question:
                    return topic["answer"]

        return "Sorry, I don’t have an answer for that yet."


class GardenCLI:
    def __init__(self):
        self.advisor = GardenAdvisor()

    def show_menu(self):
        print("""
🌱 Garden App Menu
-----------------------------------
1. Get current advice
2. Get monthly advice
3. Get plant advice
4. Ask gardening question
5. Set hemisphere
6. Help
7. Exit
-----------------------------------
""")

    def show_help(self):
        print("""
💡 Usage Tips:
- Option 2: enter month (1–12)
- Option 3: plant <name>
- Option 4: ask <question>
- Option 5: set hemisphere
""")

    def run(self):
        print("🌿 Welcome to the Garden App 🌿")
        self.show_menu()

        while True:
            choice = input("Select option >> ").strip().lower()

            if choice in ["7", "exit"]:
                print("Goodbye! 🌱")
                break

            elif choice in ["6", "help"]:
                self.show_help()

            elif choice == "1":
                print(self.advisor.get_current_advice())

            elif choice == "2":
                month = input("Enter month (1–12): ").strip()
                if month.isdigit():
                    try:
                        print(self.advisor.get_advice_by_month(int(month)))
                    except ValueError as e:
                        print(e)
                else:
                    print("Invalid month input.")

            elif choice == "3":
                plant = input("Plant name: ").strip()
                print(self.advisor.get_plant_advice(plant))

            elif choice == "4":
                question = input("Ask question: ").strip()
                print(self.advisor.answer_question(question))

            elif choice == "5":
                hemi = input("northern/southern: ").strip().lower()
                if hemi in ["northern", "southern"]:
                    self.advisor.config["hemisphere"] = hemi
                    self.advisor.save_user_config()
                    print(f"Hemisphere set to {hemi}")
                else:
                    print("Invalid hemisphere.")

            else:
                print("Invalid option. Type 6 for help.")