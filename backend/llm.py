def generate_travel_plan(city_info, budget):
    # Extract city name and attractions
    city_name = city_info.get("city", "the destination")
    attractions = city_info.get("attractions", [])
    
    # Generate a simple text plan based on city info
    plan = f"Welcome to {city_name}!\n\n"
    plan += f"Budget for your trip: ${budget}\n\n"
    plan += "Here is a suggested itinerary:\n"
    
    for idx, attraction in enumerate(attractions[:3], start=1):
        plan += f"Day {idx}: Visit {attraction}.\n"
    
    plan += "\nEnjoy your trip!"
    return plan
