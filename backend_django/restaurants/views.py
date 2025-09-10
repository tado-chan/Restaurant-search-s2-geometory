"""
API Views for Restaurant Search
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import get_db_session
from .services import RestaurantSearchService, OSMBuildingService, ValidationService, SpatialSearchService
import json
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
def search_restaurant(request):
    """
    最寄りレストラン検索API（OSM ID使用）
    POST /api/search
    """
    try:
        # リクエストデータ取得
        data = request.data
        lat = data.get('lat')
        lng = data.get('lng')
        
        # 必須パラメータチェック
        if lat is None or lng is None:
            return Response({
                'error': '緯度(lat)と経度(lng)は必須です'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 型変換
        try:
            lat = float(lat)
            lng = float(lng)
        except (ValueError, TypeError):
            return Response({
                'error': '緯度・経度は数値で入力してください'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 座標検証
        validation = ValidationService.validate_coordinates(lat, lng)
        if not validation['is_valid']:
            return Response({
                'error': ', '.join(validation['errors'])
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # データベースセッション取得
        db = next(get_db_session())
        
        try:
            # サービス実行
            service = RestaurantSearchService(db)
            result = service.search_nearest_restaurant_optimized(lat, lng)
            
            if not result:
                return Response({
                    'error': '近くにレストランが見つかりませんでした'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response(result, status=status.HTTP_200_OK)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Restaurant search error: {str(e)}")
        return Response({
            'error': 'サーバー内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_restaurants(request):
    """
    全レストラン一覧取得API
    GET /api/restaurants
    """
    try:
        # データベースセッション取得
        db = next(get_db_session())
        
        try:
            # サービス実行
            service = RestaurantSearchService(db)
            restaurants = service.get_all_restaurants()
            
            return Response({
                'restaurants': restaurants,
                'count': len(restaurants)
            }, status=status.HTTP_200_OK)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Get restaurants error: {str(e)}")
        return Response({
            'error': 'サーバー内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_restaurant_detail(request, restaurant_id):
    """
    レストラン詳細情報取得API
    GET /api/restaurants/{restaurant_id}
    """
    try:
        # データベースセッション取得
        db = next(get_db_session())
        
        try:
            # サービス実行
            service = RestaurantSearchService(db)
            result = service.get_restaurant_detail(restaurant_id)
            
            if not result:
                return Response({
                    'error': 'レストランが見つかりませんでした'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response(result, status=status.HTTP_200_OK)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Get restaurant detail error: {str(e)}")
        return Response({
            'error': 'サーバー内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_osm_building(request, osm_id):
    """
    OSM建物データ取得API
    GET /api/buildings/{osm_id}
    """
    try:
        # データベースセッション取得
        db = next(get_db_session())
        
        try:
            # サービス実行
            service = OSMBuildingService(db)
            building = service.get_building_by_osm_id(osm_id)
            
            if not building:
                return Response({
                    'error': 'OSM建物データが見つかりませんでした'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response(building, status=status.HTTP_200_OK)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Get OSM building error: {str(e)}")
        return Response({
            'error': 'サーバー内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_buildings(request):
    """
    全OSM建物一覧取得API
    GET /api/buildings
    """
    try:
        # データベースセッション取得
        db = next(get_db_session())
        
        try:
            # サービス実行
            service = OSMBuildingService(db)
            buildings = service.get_all_buildings()
            
            return Response({
                'buildings': buildings,
                'count': len(buildings)
            }, status=status.HTTP_200_OK)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Get buildings error: {str(e)}")
        return Response({
            'error': 'サーバー内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def search_restaurants_by_location(request):
    """
    位置ベースレストラン検索API（範囲指定）
    POST /api/search/location
    """
    try:
        # リクエストデータ取得
        data = request.data
        lat = data.get('lat')
        lng = data.get('lng')
        radius = data.get('radius', 1.0)  # デフォルト1km
        
        # 必須パラメータチェック
        if lat is None or lng is None:
            return Response({
                'error': '緯度(lat)と経度(lng)は必須です'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 型変換
        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
        except (ValueError, TypeError):
            return Response({
                'error': '緯度・経度・半径は数値で入力してください'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 座標検証
        coord_validation = ValidationService.validate_coordinates(lat, lng)
        if not coord_validation['is_valid']:
            return Response({
                'error': ', '.join(coord_validation['errors'])
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 半径検証
        radius_validation = ValidationService.validate_search_radius(radius)
        if not radius_validation['is_valid']:
            return Response({
                'error': ', '.join(radius_validation['errors'])
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # データベースセッション取得
        db = next(get_db_session())
        
        try:
            # サービス実行
            service = RestaurantSearchService(db)
            results = service.search_restaurants_by_location(lat, lng, radius)
            
            return Response({
                'restaurants': results,
                'count': len(results),
                'search_params': {
                    'lat': lat,
                    'lng': lng,
                    'radius_km': radius
                }
            }, status=status.HTTP_200_OK)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Location-based search error: {str(e)}")
        return Response({
            'error': 'サーバー内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def health_check(request):
    """
    ヘルスチェックAPI
    GET /api/health
    """
    try:
        # データベース接続テスト
        db = next(get_db_session())
        db.close()
        
        return Response({
            'status': 'OK',
            'message': 'Restaurant Search API Server is running',
            'version': '1.0.0'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return Response({
            'status': 'ERROR',
            'message': 'Database connection failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def search_building_by_location(request):
    """
    PostGIS空間検索API（新機能）
    POST /api/search/spatial
    指定座標を含む建物のOSM IDを返す
    """
    try:
        # リクエストデータ取得
        data = request.data
        lat = data.get('lat')
        lng = data.get('lng')
        
        # 必須パラメータチェック
        if lat is None or lng is None:
            return Response({
                'error': '緯度(lat)と経度(lng)は必須です'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 型変換
        try:
            lat = float(lat)
            lng = float(lng)
        except (ValueError, TypeError):
            return Response({
                'error': '緯度・経度は数値で入力してください'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 座標検証
        validation = ValidationService.validate_coordinates(lat, lng)
        if not validation['is_valid']:
            return Response({
                'error': ', '.join(validation['errors'])
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # データベースセッション取得
        db = next(get_db_session())
        
        try:
            # 空間検索サービス実行
            service = SpatialSearchService(db)
            result = service.find_building_at_location(lat, lng)
            
            if not result:
                return Response({
                    'error': 'この座標には建物が見つかりませんでした',
                    'coordinates': {'lat': lat, 'lng': lng}
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response(result, status=status.HTTP_200_OK)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Spatial search error: {str(e)}")
        return Response({
            'error': 'サーバー内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def search_buildings_near_location(request):
    """
    PostGIS周辺建物検索API
    POST /api/search/spatial/nearby
    指定座標周辺の建物を検索
    """
    try:
        # リクエストデータ取得
        data = request.data
        lat = data.get('lat')
        lng = data.get('lng')
        radius = data.get('radius', 100)  # デフォルト100メートル
        
        # 必須パラメータチェック
        if lat is None or lng is None:
            return Response({
                'error': '緯度(lat)と経度(lng)は必須です'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 型変換
        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
        except (ValueError, TypeError):
            return Response({
                'error': '緯度・経度・半径は数値で入力してください'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 座標検証
        validation = ValidationService.validate_coordinates(lat, lng)
        if not validation['is_valid']:
            return Response({
                'error': ', '.join(validation['errors'])
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 半径検証
        if radius <= 0 or radius > 1000:
            return Response({
                'error': '半径は1～1000メートルの範囲で指定してください'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # データベースセッション取得
        db = next(get_db_session())
        
        try:
            # 空間検索サービス実行
            service = SpatialSearchService(db)
            results = service.find_buildings_near_location(lat, lng, radius)
            
            return Response({
                'buildings': results,
                'count': len(results),
                'search_params': {
                    'lat': lat,
                    'lng': lng,
                    'radius_meters': radius
                }
            }, status=status.HTTP_200_OK)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Nearby spatial search error: {str(e)}")
        return Response({
            'error': 'サーバー内部エラーが発生しました'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)