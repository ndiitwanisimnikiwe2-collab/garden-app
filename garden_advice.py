# Get user input
season = input("Enter the season (summer/winter): ").lower().strip()
plant_type = input("Enter the plant type (flower/vegetable): ").lower().strip()

# Function to handle season advice
def get_season_advice(season):
    if season == "summer":
        return "Water your plants regularly and provide some shade.\n"
    elif season == "winter":
        return "Protect your plants from frost with covers.\n"
    else:
        return "No advice for this season.\n"

# Function to handle plant advice
def get_plant_advice(plant_type):
    if plant_type == "flower":
        return "Use fertilisers to encourage blooms."
    elif plant_type == "vegetable":
        return "Keep an eye out for pests!"
    else:
        return "No advice for this type of plant."

# Combine results
advice = get_season_advice(season) + get_plant_advice(plant_type)

print(advice)
