export interface Restaurant {
  id: string;
  name: string;
  address: string;
  openingHours: string;
  rating: number;
  lat: number;
  lng: number;
  osmBuildingId?: number;
}

export interface GeoJSONGeometry {
  type: 'Polygon';
  coordinates: number[][][]; // [[[lng, lat], [lng, lat], ...]]
}

export interface GeoJSONFeature {
  type: 'Feature';
  properties: {
    building?: string;
    osm_id?: number;
    name?: string;
  };
  geometry: GeoJSONGeometry;
}

export interface BuildingSearchResponse {
  restaurant: Restaurant;
  buildingPolygon?: GeoJSONFeature;
  message?: string;
}

export interface OptimizedBuildingResponse {
  restaurant: Restaurant;
  osmBuildingId?: number;
  message?: string;
}

export interface SearchRequest {
  lat: number;
  lng: number;
}

export interface MapTap {
  lat: number;
  lng: number;
}