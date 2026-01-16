import httpx
from app.core.config import settings

OVERPASS_QUERY = """
[out:json];
(
  node(around:{radius},{lat},{lon})["amenity"];
  node(around:{radius},{lat},{lon})["tourism"];
  node(around:{radius},{lat},{lon})["historic"];
);
out body;
>;
out skel qt;
"""

class OSMClient:
    async def fetch_pois(self, lat: float, lon: float, radius: int = 500):
        query = OVERPASS_QUERY.format(lat=lat, lon=lon, radius=radius)
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(settings.OSM_API_URL, data={"data": query}, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                return self._parse_osm_response(data)
            except Exception as e:
                # Log error in production
                print(f"OSM Fetch Error: {e}")
                return []

    def _parse_osm_response(self, data: dict):
        pois = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name")
            if not name:
                continue
                
            category = "unknown"
            if "amenity" in tags:
                category = tags["amenity"]
            elif "tourism" in tags:
                category = tags["tourism"]
            elif "historic" in tags:
                category = tags["historic"]
                
            pois.append({
                "osm_id": str(element["id"]),
                "lat": element["lat"],
                "lon": element["lon"],
                "name": name,
                "category": category,
                "description": tags.get("description", "")
            })
        return pois
