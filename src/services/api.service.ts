import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { environment } from '../environments/environment';
import { BuildingSearchResponse, SearchRequest, OptimizedBuildingResponse } from '../models/restaurant';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly baseUrl = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  async searchNearbyRestaurant(coordinates: SearchRequest): Promise<BuildingSearchResponse> {
    const url = `${this.baseUrl}/api/restaurants/search`;
    
    // Use actual backend API call
    try {
      return firstValueFrom(
        this.http.post<BuildingSearchResponse>(url, coordinates)
      );
    } catch (error) {
      // Fallback to mock if backend is not available
      console.warn('Backend not available, using mock data:', error);
      return this.getMockResponse();
    }
  }

  async searchNearbyRestaurantOptimized(coordinates: SearchRequest): Promise<OptimizedBuildingResponse> {
    const url = `${this.baseUrl}/api/restaurants/search-optimized`;
    
    try {
      return firstValueFrom(
        this.http.post<OptimizedBuildingResponse>(url, coordinates)
      );
    } catch (error) {
      console.warn('Backend not available, using optimized mock data:', error);
      return this.getMockOptimizedResponse();
    }
  }

  private getMockResponse(): Promise<BuildingSearchResponse> {
    // Mock GeoJSON building polygon for development
    const mockBuildingPolygon = {
      type: "Feature" as const,
      properties: {
        building: "residential",
        osm_id: 123456,
        name: "Mock Building"
      },
      geometry: {
        type: "Polygon" as const,
        coordinates: [
          [
            [139.6503, 35.6762], // SW corner
            [139.6505, 35.6762], // SE corner
            [139.6505, 35.6764], // NE corner
            [139.6503, 35.6764], // NW corner
            [139.6503, 35.6762]  // Close polygon
          ]
        ]
      }
    };

    // Mock data for development
    const mockResponses: BuildingSearchResponse[] = [
      {
        restaurant: {
          id: "rest_001",
          name: "東京ラーメン横丁",
          address: "東京都渋谷区1-2-3",
          openingHours: "11:00 - 22:00",
          rating: 4.2,
          lat: 35.6762,
          lng: 139.6503,
          osmBuildingId: 123456
        },
        buildingPolygon: mockBuildingPolygon,
        message: "建物が見つかりました"
      },
      {
        restaurant: {
          id: "rest_002", 
          name: "築地寿司 禅",
          address: "東京都中央区銀座4-5-6",
          openingHours: "17:00 - 24:00",
          rating: 4.7,
          lat: 35.6765,
          lng: 139.6510,
          osmBuildingId: 789012
        },
        buildingPolygon: {
          ...mockBuildingPolygon,
          geometry: {
            ...mockBuildingPolygon.geometry,
            coordinates: [
              [
                [139.6510, 35.6765],
                [139.6512, 35.6765],
                [139.6512, 35.6767],
                [139.6510, 35.6767],
                [139.6510, 35.6765]
              ]
            ]
          }
        },
        message: "建物が見つかりました"
      },
      {
        restaurant: {
          id: "rest_003",
          name: "アジアンパーム渋谷本町",
          address: "東京都渋谷区本町2-14-4", 
          openingHours: "11:30 - 14:30, 17:00 - 23:00",
          rating: 4.0,
          lat: 35.6713,
          lng: 139.6845,
          osmBuildingId: 456789
        },
        buildingPolygon: {
          ...mockBuildingPolygon,
          properties: {
            building: "commercial",
            osm_id: 456789,
            name: "Asian Palm Building"
          },
          geometry: {
            ...mockBuildingPolygon.geometry,
            coordinates: [
              [
                [139.6843, 35.6711],
                [139.6847, 35.6711],
                [139.6847, 35.6715],
                [139.6843, 35.6715],
                [139.6843, 35.6711]
              ]
            ]
          }
        },
        message: "建物が見つかりました"
      }
    ];

    const randomResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)];
    
    // Simulate API delay
    return new Promise(resolve => {
      setTimeout(() => resolve(randomResponse), 500);
    });
  }

  private getMockOptimizedResponse(): Promise<OptimizedBuildingResponse> {
    const mockOptimizedResponses: OptimizedBuildingResponse[] = [
      {
        restaurant: {
          id: "rest_001",
          name: "東京ラーメン横丁",
          address: "東京都渋谷区1-2-3",
          openingHours: "11:00 - 22:00",
          rating: 4.2,
          lat: 35.6762,
          lng: 139.6503,
          osmBuildingId: 123456
        },
        osmBuildingId: 123456,
        message: "建物が見つかりました"
      },
      {
        restaurant: {
          id: "rest_002", 
          name: "築地寿司 禅",
          address: "東京都中央区銀座4-5-6",
          openingHours: "17:00 - 24:00",
          rating: 4.7,
          lat: 35.6765,
          lng: 139.6510,
          osmBuildingId: 789012
        },
        osmBuildingId: 789012,
        message: "建物が見つかりました"
      },
      {
        restaurant: {
          id: "rest_003",
          name: "アジアンパーム渋谷本町",
          address: "東京都渋谷区本町2-14-4", 
          openingHours: "11:30 - 14:30, 17:00 - 23:00",
          rating: 4.0,
          lat: 35.6713,
          lng: 139.6845,
          osmBuildingId: 456789
        },
        osmBuildingId: 456789,
        message: "建物が見つかりました"
      }
    ];

    const randomResponse = mockOptimizedResponses[Math.floor(Math.random() * mockOptimizedResponses.length)];
    
    // Faster response for optimized version
    return new Promise(resolve => {
      setTimeout(() => resolve(randomResponse), 100);
    });
  }
}