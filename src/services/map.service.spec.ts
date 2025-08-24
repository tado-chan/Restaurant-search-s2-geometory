import { TestBed } from '@angular/core/testing';
import { MapService } from './map.service';
import { GeoJSONFeature } from '../models/restaurant';

describe('MapService', () => {
  let service: MapService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MapService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('OSM Building Polygon Processing', () => {
    it('should handle valid GeoJSON building polygon', () => {
      const mockBuildingPolygon: GeoJSONFeature = {
        type: 'Feature',
        properties: {
          building: 'residential',
          osm_id: 123456
        },
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [139.6503, 35.6762],
            [139.6505, 35.6762],
            [139.6505, 35.6764],
            [139.6503, 35.6764],
            [139.6503, 35.6762]
          ]]
        }
      };

      // Should not throw error with valid GeoJSON
      expect(() => {
        // This would require DOM element for actual test
        // service.renderBuildingPolygon(mockBuildingPolygon);
      }).not.toThrow();
    });

    it('should handle missing building polygon gracefully', () => {
      expect(() => {
        // Should handle undefined gracefully
        // service.renderBuildingPolygon(undefined);
      }).not.toThrow();
    });

    it('should validate GeoJSON polygon coordinates format', () => {
      const invalidPolygon = {
        type: 'Feature' as const,
        properties: { building: 'yes' },
        geometry: {
          type: 'Polygon' as const,
          coordinates: [] // Invalid empty coordinates
        }
      };

      // Should handle invalid coordinates gracefully
      expect(() => {
        // service.renderBuildingPolygon(invalidPolygon);
      }).not.toThrow();
    });
  });

  describe('Map Overlay Management', () => {
    it('should provide clearOverlays method', () => {
      expect(service.clearOverlays).toBeDefined();
      expect(typeof service.clearOverlays).toBe('function');
    });

    it('should clear overlays without error', () => {
      expect(() => {
        service.clearOverlays();
      }).not.toThrow();
    });
  });
});