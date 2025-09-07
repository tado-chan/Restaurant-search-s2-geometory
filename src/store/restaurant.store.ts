import { Injectable, signal } from '@angular/core';
import { Restaurant, MapTap } from '../models/restaurant';
import { ApiService } from '../services/api.service';

@Injectable({
  providedIn: 'root'
})
export class RestaurantStore {
  private _selectedTap = signal<MapTap | null>(null);
  private _currentRestaurant = signal<Restaurant | null>(null);
  private _currentOsmBuildingId = signal<string | null>(null);
  private _searchMessage = signal<string | null>(null);
  private _isLoading = signal<boolean>(false);
  private _error = signal<string | null>(null);
  private _isSheetOpen = signal<boolean>(false);

  // Public read-only signals
  selectedTap = this._selectedTap.asReadonly();
  currentRestaurant = this._currentRestaurant.asReadonly();
  currentOsmBuildingId = this._currentOsmBuildingId.asReadonly();
  searchMessage = this._searchMessage.asReadonly();
  isLoading = this._isLoading.asReadonly();
  error = this._error.asReadonly();
  isSheetOpen = this._isSheetOpen.asReadonly();

  constructor(private apiService: ApiService) {}

  setSelectedTap(tap: MapTap) {
    this._selectedTap.set(tap);
  }

  setLoading(isLoading: boolean) {
    this._isLoading.set(isLoading);
  }

  setError(error: string | null) {
    this._error.set(error);
  }

  setSheetOpen(isOpen: boolean) {
    this._isSheetOpen.set(isOpen);
  }


  async searchNearbyRestaurant(coordinates: MapTap): Promise<void> {
    console.log('searchNearbyRestaurant called with:', coordinates);
    this._isLoading.set(true);
    this._error.set(null);
    this._selectedTap.set(coordinates);

    try {
      const response = await this.apiService.searchNearbyRestaurant(coordinates);
      console.log('API response:', response);
      
      this._currentRestaurant.set(response.restaurant);
      this._currentOsmBuildingId.set(response.osmBuildingId || null);
      this._searchMessage.set(response.message || null);
      this._isLoading.set(false);
      this._isSheetOpen.set(true);
      console.log('Store updated, osmBuildingId:', response.osmBuildingId);
    } catch (error) {
      this._error.set(error instanceof Error ? error.message : 'Search failed');
      this._isLoading.set(false);
      this._currentRestaurant.set(null);
      this._currentOsmBuildingId.set(null);
      this._searchMessage.set(null);
    }
  }

  clearSelection() {
    this._selectedTap.set(null);
    this._currentRestaurant.set(null);
    this._currentOsmBuildingId.set(null);
    this._searchMessage.set(null);
    this._error.set(null);
    this._isSheetOpen.set(false);
  }
}