#session 2 
def calculate_daily_budget(budget, days):
 return budget/days

def get_trip_category(budget):
 if budget < 1000:
   return "Backpacker"
 elif budget < 3000:
   return "Standard"
 else:
   return "Luxury"

rekomendasi_tempat = {
  "Standard": "Japan: Tokyo Tower, Shibuya, Month Fuji",
  "Backpacker": "Bali: Ubud, Kuta Beach, Pandawa Beach",
  "Luxury": "Australia: Sydney, Melbourne, Queensland"
}

#Homework session 2 (Tugas 2)
def get_travel_season(month):
    if month == "December":
        return "Peak Season"
    elif month == "June":
        return "Holiday Season"
    else:
        return "Regular Season"

# challenge session 2
def get_transportation(destination):
    if category == "Backpacker":
        return "Bus"
    elif category == "Standard":
        return "Train"
    elif category == "Luxury":
        return "Flight"
    else:
        return "Unknown"

destination = "Japan"
days = 5
budget = 1500
travel_month = "December"

daily = calculate_daily_budget(1500,5)
category = get_trip_category(1500)
transport = get_transportation(category)
season = get_travel_season(travel_month)

print(f"Destination  : {destination}")
print(f"Days         : {days}")
print(f"Budget       : {budget} USD")
print(f"Travel Month : {travel_month}")
print(f"Season       : {season}")

print(f"{category} · {daily} USD/day")
print(f"Recommended Transportation: {transport}")
print(f"Recommended Places: {rekomendasi_tempat[category]}\n")

destination = "Bali"
days = 3
budget = 800
travel_month = "March"

daily = calculate_daily_budget(800,3)
category = get_trip_category(800)
transport = get_transportation(category)
season = get_travel_season(travel_month)

print(f"Destination  : {destination}")
print(f"Days         : {days}")
print(f"Budget       : {budget} USD")
print(f"Travel Month : {travel_month}")
print(f"Season       : {season}")

print(f"{category} · {daily} USD/day")
print(f"Recommended Transportation: {transport}")
print(f"Recommended places: {rekomendasi_tempat[category]}\n")

destination = "Australia"
days = 5
budget = 5000
travel_month = "June"

daily = calculate_daily_budget(5000,5)
category = get_trip_category(5000)
transport = get_transportation(category)
season = get_travel_season(travel_month)

print(f"Destination  : {destination}")
print(f"Days         : {days}")
print(f"Budget       : {budget} USD")
print(f"Travel Month : {travel_month}")
print(f"Season       : {season}")

print(f"{category} · {daily} USD/day")
print(f"Recommended Transportation: {transport}")
print(f"Recommended places: {rekomendasi_tempat[category]}\n")