import { Injectable } from '@angular/core';
import { Loader } from '@googlemaps/js-api-loader';
import { environment } from '../environments/environment';
import { GeoJSONFeature, GeoJSONGeometry } from '../models/restaurant';

@Injectable({
  providedIn: 'root'
})
export class MapService {
  private map?: google.maps.Map;
  private loader: Loader;
  private currentBuildingPolygon?: google.maps.Polygon;
  private osmBuildingCache = new Map<string, GeoJSONFeature>();

  constructor() {
    this.loader = new Loader({
      apiKey: environment.googleMapsApiKey,
      version: 'weekly',
      libraries: ['geometry']
    });
  }

  async initializeMap(element: HTMLElement): Promise<google.maps.Map> {
    const google = await this.loader.load();
    
    this.map = new google.maps.Map(element, {
      center: { lat: 35.6762, lng: 139.6503 }, // Tokyo default
      zoom: 15,
      mapId: 'restaurant-search-map'
    });

    return this.map;
  }

  addClickListener(callback: (event: google.maps.MapMouseEvent) => void): void {
    if (!this.map) throw new Error('Map not initialized');
    
    this.map.addListener('click', callback);
  }

  renderBuildingPolygon(geoJsonFeature?: GeoJSONFeature): void {
    if (!this.map) throw new Error('Map not initialized');
    
    this.clearOverlays();

    if (!geoJsonFeature) {
      console.warn('No building polygon to render');
      return;
    }

    // Convert GeoJSON coordinates to Google Maps LatLng (optimized)
    const coordinates = geoJsonFeature.geometry.coordinates[0];
    const path = this.convertCoordinatesOptimized(coordinates);

    // Create building polygon with optimized settings
    this.currentBuildingPolygon = new google.maps.Polygon({
      paths: path,
      fillColor: '#4285F4',
      fillOpacity: 0.3,
      strokeColor: '#1976D2', 
      strokeOpacity: 0.6,
      strokeWeight: 1,
      map: this.map
    });

    // Only adjust view if building is not visible in current viewport
    this.adjustViewportIfNeeded(path);
  }

  private convertCoordinatesOptimized(coordinates: number[][]): google.maps.LatLng[] {
    // Pre-allocate array for better performance
    const path = new Array(coordinates.length);
    for (let i = 0; i < coordinates.length; i++) {
      path[i] = new google.maps.LatLng(coordinates[i][1], coordinates[i][0]);
    }
    return path;
  }

  private adjustViewportIfNeeded(path: google.maps.LatLng[]): void {
    if (!this.map) return;
    
    const currentBounds = this.map.getBounds();
    if (!currentBounds) return;

    // Check if building is already visible
    const buildingBounds = new google.maps.LatLngBounds();
    path.forEach(point => buildingBounds.extend(point));
    
    // Only adjust if building is not visible or very small in current view
    if (!currentBounds.contains(buildingBounds.getCenter()) || 
        !this.isBuildingSufficientlyVisible(buildingBounds, currentBounds)) {
      
      this.map.fitBounds(buildingBounds);
      
      // Set zoom limit without event listener for better performance
      const currentZoom = this.map.getZoom();
      if (currentZoom && currentZoom > 19) {
        this.map.setZoom(19);
      }
    }
  }

  private isBuildingSufficientlyVisible(buildingBounds: google.maps.LatLngBounds, currentBounds: google.maps.LatLngBounds): boolean {
    const buildingNE = buildingBounds.getNorthEast();
    const buildingSW = buildingBounds.getSouthWest();
    const currentNE = currentBounds.getNorthEast();
    const currentSW = currentBounds.getSouthWest();
    
    // Building should occupy at least 10% of viewport to be considered sufficiently visible
    const buildingWidth = buildingNE.lng() - buildingSW.lng();
    const buildingHeight = buildingNE.lat() - buildingSW.lat();
    const viewWidth = currentNE.lng() - currentSW.lng();
    const viewHeight = currentNE.lat() - currentSW.lat();
    
    return (buildingWidth / viewWidth > 0.1) && (buildingHeight / viewHeight > 0.1);
  }

  clearOverlays(): void {
    if (this.currentBuildingPolygon) {
      this.currentBuildingPolygon.setMap(null);
      this.currentBuildingPolygon = undefined;
    }
  }

  async renderBuildingPolygonByOsmId(osmBuildingId: string): Promise<void> {
    console.log('renderBuildingPolygonByOsmId called with:', osmBuildingId);
    
    if (!this.map) throw new Error('Map not initialized');
    
    this.clearOverlays();

    // Check cache first
    let geoJsonFeature = this.osmBuildingCache.get(osmBuildingId);
    console.log('Cache lookup result:', geoJsonFeature ? 'found' : 'not found');
    
    if (!geoJsonFeature) {
      // Fetch building data from OSM API or use mock data
      geoJsonFeature = await this.fetchBuildingFromOsm(osmBuildingId);
      console.log('Fetched from OSM:', geoJsonFeature ? 'success' : 'failed');
      if (geoJsonFeature) {
        this.osmBuildingCache.set(osmBuildingId, geoJsonFeature);
      }
    }

    if (geoJsonFeature) {
      console.log('Rendering polygon with coordinates:', geoJsonFeature.geometry.coordinates);
      this.renderBuildingPolygon(geoJsonFeature);
    } else {
      console.warn(`Building with OSM ID ${osmBuildingId} not found`);
    }
  }

  private async fetchBuildingFromOsm(osmBuildingId: string): Promise<GeoJSONFeature | undefined> {
    try {
      const response = await fetch(`/api/buildings/${osmBuildingId}`);
      if (!response.ok) {
        console.warn(`Failed to fetch building ${osmBuildingId}: ${response.status}`);
        return undefined;
      }
      return await response.json();
    } catch (error) {
      console.error(`Error fetching building ${osmBuildingId}:`, error);
      return undefined;
    }
  }

  getMap(): google.maps.Map | undefined {
    return this.map;
  }
}