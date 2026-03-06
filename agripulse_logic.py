def calculate_agripulse_score(crop, n, p, k, ph):

    base_score = 100
    penalties = 0
    deficiencies = []
    actions = []

    crop = crop.upper()

    ph_ranges = {
        "TOMATO": (6.0, 7.0),
        "WHEAT": (6.0, 7.5),
        "RICE": (5.0, 6.5),
        "MAIZE": (5.8, 7.0)
    }

    low, high = ph_ranges[crop]

    if not (low <= ph <= high):
        penalties += 20

    if n < 20:
        penalties += 15
        deficiencies.append("Nitrogen")
        actions.append("Apply Urea Fertilizer")

    if p < 15:
        penalties += 15
        deficiencies.append("Phosphorus")
        actions.append("Apply DAP (Diammonium Phosphate)")

    if k < 150:
        penalties += 15
        deficiencies.append("Potassium")
        actions.append("Apply MOP (Muriate of Potash)")

    critical = {
        "TOMATO": ("k", 200),
        "WHEAT": ("n", 30),
        "RICE": ("p", 25),
        "MAIZE": ("n", 35)
    }

    nutrient, threshold = critical[crop]

    values = {"n": n, "p": p, "k": k}

    if values[nutrient] < threshold:
        penalties += 10

    score = max(0, base_score - penalties)

    if score >= 80:
        health = "Optimal"
    elif score >= 50:
        health = "Deficient"
    else:
        health = "Critical"

    fertilizer = "No fertilizer required"
    if actions:
        fertilizer = ", ".join(actions)

    return score, health, deficiencies, fertilizer