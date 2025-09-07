export interface Restaurant {
  id: string;
  name: string;
  address: string;
  openingHours: string;
  rating: number;
  lat: number;
  lng: number;
  osmBuildingId?: string;
}

export interface GeoJSONGeometry {
  type: 'Polygon';
  coordinates: number[][][]; // [[[lng, lat], [lng, lat], ...]]
}

export interface GeoJSONFeature {
  type: 'Feature';
  properties: {
    building?: string;
    osm_id?: string;
    name?: string;
    'building:levels'?: string;
    'building:material'?: string;
    'building:colour'?: string;
    'building:use'?: string;
    'roof:shape'?: string;
  };
  geometry: GeoJSONGeometry;
}

export interface BuildingSearchResponse {
  restaurant: Restaurant;
  osmBuildingId?: string;
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