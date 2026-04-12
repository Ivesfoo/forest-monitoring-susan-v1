from services.area_service import get_active_monitored_areas

areas = get_active_monitored_areas()

print("Active monitored areas count:", len(areas))

if areas:
    print("First area name:", areas[0]["area_name"])
    print("First area geojson:", areas[0]["geojson"])
else:
    print("No active monitored areas found.")