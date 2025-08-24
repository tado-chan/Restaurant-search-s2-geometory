import { Component, OnInit, ViewChild, ElementRef, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonContent, IonHeader, IonTitle, IonToolbar, IonSpinner, IonToast, IonModal, IonButton, IonItem, IonLabel, IonText } from '@ionic/angular/standalone';
import { MapService } from '../../services/map.service';
import { RestaurantStore } from '../../store/restaurant.store';

@Component({
  selector: 'app-map',
  templateUrl: './map.page.html',
  styleUrls: ['./map.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    IonContent,
    IonHeader, 
    IonTitle,
    IonToolbar,
    IonSpinner,
    IonToast,
    IonModal,
    IonButton,
    IonItem,
    IonLabel,
    IonText
  ]
})
export class MapPage implements OnInit {
  @ViewChild('mapContainer', { static: true }) mapContainer!: ElementRef;
  
  private mapService = inject(MapService);
  protected store = inject(RestaurantStore);

  constructor() {
    // Effect to render building polygon when buildingPolygon or osmBuildingId changes
    effect(() => {
      const buildingPolygon = this.store.currentBuildingPolygon();
      const osmBuildingId = this.store.currentOsmBuildingId();
      
      if (this.store.useOptimizedMode() && osmBuildingId) {
        // Use OSM ID for optimized rendering
        this.mapService.renderBuildingPolygonByOsmId(osmBuildingId);
      } else if (!this.store.useOptimizedMode() && buildingPolygon) {
        // Use traditional polygon rendering
        this.mapService.renderBuildingPolygon(buildingPolygon);
      }
    });
  }

  async ngOnInit() {
    await this.initializeMap();
  }

  private async initializeMap() {
    try {
      const map = await this.mapService.initializeMap(this.mapContainer.nativeElement);
      
      this.mapService.addClickListener((event) => {
        if (event.latLng) {
          const coordinates = {
            lat: event.latLng.lat(),
            lng: event.latLng.lng()
          };
          
          this.store.searchNearbyRestaurant(coordinates);
        }
      });
    } catch (error) {
      this.store.setError('Failed to initialize map');
    }
  }

  protected onSheetDismiss() {
    this.store.setSheetOpen(false);
    this.mapService.clearOverlays();
    this.store.clearSelection();
  }

  protected formatRating(rating: number): string {
    return rating.toFixed(1);
  }

  protected getStars(rating: number): string {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    return '★'.repeat(fullStars) + (hasHalfStar ? '☆' : '') + '☆'.repeat(5 - Math.ceil(rating));
  }

  protected toggleOptimizedMode() {
    const currentMode = this.store.useOptimizedMode();
    this.store.setOptimizedMode(!currentMode);
  }
}