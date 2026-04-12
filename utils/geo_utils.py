from shapely.geometry import Point, shape


def is_point_in_geojson(lat, lon, geojson):
    try:
        geom = shape(geojson["features"][0]["geometry"])
        point = Point(lon, lat)
        return geom.intersects(point)
    except Exception:
        return False