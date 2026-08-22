# Session 2 - Core calculation functions
def calculate_daily_budget(budget, days):
    """Calculate daily budget from total budget and number of days"""
    if days <= 0:
        return 0.0
    return budget / days

def get_trip_category(budget):
    """Categorize trip based on budget"""
    if budget < 1000:
        return "Backpacker"
    elif budget < 3000:
        return "Standard"
    else:
        return "Luxury"

# Recommendation data
rekomendasi_tempat = {
    "Standard": "Japan: Tokyo Tower, Shibuya, Mount Fuji",
    "Backpacker": "Bali: Ubud, Kuta Beach, Pandawa Beach",
    "Luxury": "Australia: Sydney, Melbourne, Queensland"
}

# Homework session 2 (Tugas 2)
def get_travel_season(month):
    """Determine travel season based on month"""
    if month == "December":
        return "Peak Season"
    elif month == "June":
        return "Holiday Season"
    else:
        return "Regular Season"

# Challenge session 2
def get_transportation(category):
    """Get recommended transportation based on trip category"""
    if category == "Backpacker":
        return "Bus"
    elif category == "Standard":
        return "Train"
    elif category == "Luxury":
        return "Flight"
    else:
        return "Bus"

# Example usage (only runs when script is executed directly)
if __name__ == "__main__":
    # Example 1: Japan trip
    destination = "Japan"
    days = 5
    budget = 1500
    travel_month = "December"

    daily = calculate_daily_budget(budget, days)
    category = get_trip_category(budget)
    transport = get_transportation(category)
    season = get_travel_season(travel_month)

    print(f"Destination  : {destination}")
    print(f"Days         : {days}")
    print(f"Budget       : {budget} USD")
    print(f"Travel Month : {travel_month}")
    print(f"Season       : {season}")
    print(f"{category} · {daily:.2f} USD/day")
    print(f"Recommended Transportation: {transport}")
    print(f"Recommended Places: {rekomendasi_tempat[category]}\n")

    # Example 2: Bali trip
    destination = "Bali"
    days = 3
    budget = 800
    travel_month = "March"

    daily = calculate_daily_budget(budget, days)
    category = get_trip_category(budget)
    transport = get_transportation(category)
    season = get_travel_season(travel_month)

    print(f"Destination  : {destination}")
    print(f"Days         : {days}")
    print(f"Budget       : {budget} USD")
    print(f"Travel Month : {travel_month}")
    print(f"Season       : {season}")
    print(f"{category} · {daily:.2f} USD/day")
    print(f"Recommended Transportation: {transport}")
    print(f"Recommended places: {rekomendasi_tempat[category]}\n")

    # Example 3: Australia trip
    destination = "Australia"
    days = 5
    budget = 5000
    travel_month = "June"

    daily = calculate_daily_budget(budget, days)
    category = get_trip_category(budget)
    transport = get_transportation(category)
    season = get_travel_season(travel_month)

    print(f"Destination  : {destination}")
    print(f"Days         : {days}")
    print(f"Budget       : {budget} USD")
    print(f"Travel Month : {travel_month}")
    print(f"Season       : {season}")
    print(f"{category} · {daily:.2f} USD/day")
    print(f"Recommended Transportation: {transport}")
    print(f"Recommended places: {rekomendasi_tempat[category]}\n")
