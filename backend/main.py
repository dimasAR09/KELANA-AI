#session 1 
def print_trip_summary(destination, days, budget, travel_style):
    print("========================")
    print("KelanaAI")
    print("========================")
    print(f"Destination : {destination}")
    print(f"Days        : {days}")
    print(f"Budget      : {budget}")
    print(f"Style       : {travel_style}")

print_trip_summary("Japan", 5, 1500, "Family")
print_trip_summary("Bali", 3, 800, "Backpacker")
print_trip_summary("Australia", 5, 5000, "Vacation")

# Homework session 1 (Tugas 1)

def print_trip_summary(destination, Japan, days, budget, USD, December):
    print("========================")
    print("KelanaAI")
    print("========================")
    print(f"Destination : {destination}")
    print(f"Country     : {Japan}")
    print(f"Days        : {days}")
    print(f"Budget      : {budget}")
    print(f"Currency    : {USD}")
    print(f"Month       : {December}")

print_trip_summary("Japan","Japan", 5, 1500, "USD", "December")

def print_trip_summary(destination, Bali, days, budget, USD, March):
    print("========================")
    print("KelanaAI")
    print("========================")
    print(f"Destination : {destination}")
    print(f"Country     : {Bali}")
    print(f"Days        : {days}")
    print(f"Budget      : {budget}")
    print(f"Currency    : {USD}")
    print(f"Month       : {March}")

print_trip_summary("Bali","Bali", 3, 800, "USD", "March")

def print_trip_summary(destination, Australia, days, budget, USD, June):
    print("========================")
    print("KelanaAI")
    print("========================")
    print(f"Destination : {destination}")
    print(f"Country     : {Australia}")
    print(f"Days        : {days}")
    print(f"Budget      : {budget}")
    print(f"Currency    : {USD}")
    print(f"Month       : {June}")

print_trip_summary("Australia","Australia", 5, 5000, "USD", "June")

# challenge session 1
def print_trip_summary(
    destination,
    days,
    budget,
    travel_style,
    hotel_cost,
    food_cost,
    transportation_cost,
    miscellaneous_cost,
):
    total_estimated_cost = (
        hotel_cost
        + food_cost
        + transportation_cost
        + miscellaneous_cost
    )

    print("=========================")
    print("KELANA-AI")
    print("=========================")
    print(f"Destination : {destination}")
    print(f"Days        : {days}")
    print(f"Budget      : {budget}")
    print(f"Style       : {travel_style}")
    print(f"Hotel Cost  : {hotel_cost}")
    print(f"Transport   : {transportation_cost}")
    print(f"Misc Cost   : {miscellaneous_cost}")
    print(f"Total Cost  : {total_estimated_cost}")

    if total_estimated_cost > budget:
        print("Budget exceeded.")

    print()


    
print_trip_summary("Japan", 5, 1500, "Family", 900, 300, 250, 100)
print_trip_summary("Bali", 3, 800, "Backpacker", 300, 150, 100, 75) 
print_trip_summary("Australia", 5, 5000, "vacation", 400, 200, 150, 80)

#session 2 ( function logic business sevices)
from services.trip_service import calculate_daily_budget, get_trip_category, get_transportation, rekomendasi_tempat, get_travel_season