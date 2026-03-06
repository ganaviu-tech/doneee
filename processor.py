import pandas as pd


# Weather based crop recommendation
def recommend_crop_by_weather(temperature, humidity, rainfall):

    if temperature > 30 and rainfall > 100:
        return ["Rice 🌾", "Sugarcane 🌱"]

    elif temperature > 25:
        return ["Maize 🌽", "Cotton 🌿"]

    elif temperature > 20:
        return ["Wheat 🌾", "Barley 🌱"]

    else:
        return ["Potato 🥔", "Peas 🌿"]


# AI explanation generator
def generate_ai_explanation(crop, deficiencies):

    if not deficiencies:
        return f"The soil nutrients are balanced and suitable for growing {crop.lower()}."

    nutrients = ", ".join(deficiencies)

    return f"The soil is lacking {nutrients}. Adding the recommended fertilizer will help the {crop.lower()} crop grow healthier and increase yield."


# Main CSV processor
def process_csv(file, crop):

    df = pd.read_csv(file)

    results = []

    for _, row in df.iterrows():

        nitrogen = row["nitrogen"]
        phosphorus = row["phosphorus"]
        potassium = row["potassium"]
        ph = row["ph_level"]

        score = 100
        deficiencies = []
        fertilizer_plan = []

        # Universal deficiency rules
        if nitrogen < 20:
            deficiencies.append("Nitrogen")
            fertilizer_plan.append("Apply Urea Fertilizer")
            score -= 15

        if phosphorus < 15:
            deficiencies.append("Phosphorus")
            fertilizer_plan.append("Apply DAP (Diammonium Phosphate)")
            score -= 15

        if potassium < 150:
            deficiencies.append("Potassium")
            fertilizer_plan.append("Apply MOP (Muriate of Potash)")
            score -= 15

        # Crop specific pH range
        crop_ranges = {
            "TOMATO": (6.0, 7.0),
            "WHEAT": (6.0, 7.5),
            "RICE": (5.0, 6.5),
            "MAIZE": (5.8, 7.0)
        }

        min_ph, max_ph = crop_ranges[crop]

        if ph < min_ph or ph > max_ph:
            score -= 20

        # Critical nutrient penalties
        if crop == "TOMATO" and potassium < 200:
            score -= 10
            deficiencies.append("High Potassium Demand")

        if crop == "WHEAT" and nitrogen < 30:
            score -= 10
            deficiencies.append("High Nitrogen Demand")

        if crop == "RICE" and phosphorus < 25:
            score -= 10
            deficiencies.append("High Phosphorus Demand")

        if crop == "MAIZE" and nitrogen < 35:
            score -= 10
            deficiencies.append("High Nitrogen Demand")

        score = max(score, 0)

        # Health status
        if score >= 80:
            health = "Optimal"
        elif score >= 50:
            health = "Deficient"
        else:
            health = "Critical"

        # Weather recommendation
        temperature = 28
        humidity = 65
        rainfall = 120

        weather_crops = recommend_crop_by_weather(
            temperature,
            humidity,
            rainfall
        )

        result = {

            "soil_id": row["soil_id"],
            "target_crop": crop,

            "health_metrics": {
                "overall_health": health,
                "critical_deficiencies": deficiencies
            },

            "recommendation": {
                "fertilizer_plan": ", ".join(fertilizer_plan),
                "suitability_score": score
            },

            "weather_based_recommendation": weather_crops,

            "ai_explanation": generate_ai_explanation(crop, deficiencies)

        }

        results.append(result)

    return results