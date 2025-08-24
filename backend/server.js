const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// ミドルウェア設定
app.use(cors());
app.use(express.json());

// データベース接続設定
const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 3306,
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'restaurant_search_app'
};

// データベース接続プール作成
const pool = mysql.createPool(dbConfig);

// ヘルスチェック
app.get('/health', (req, res) => {
  res.json({ status: 'OK', message: 'Restaurant Search API Server is running' });
});

// 近くのレストラン検索API
app.post('/api/search', async (req, res) => {
  try {
    const { lat, lng } = req.body;
    
    if (!lat || !lng) {
      return res.status(400).json({ error: 'Latitude and longitude are required' });
    }

    // 最も近いレストランを検索（距離計算）
    const query = `
      SELECT 
        r.id,
        r.name,
        r.address,
        r.opening_hours,
        r.rating,
        r.lat,
        r.lng,
        r.osm_building_id,
        SQRT(POW(r.lat - ?, 2) + POW(r.lng - ?, 2)) as distance
      FROM restaurants r
      ORDER BY distance
      LIMIT 1
    `;
    
    const [rows] = await pool.execute(query, [lat, lng]);
    
    if (rows.length === 0) {
      return res.status(404).json({ error: 'No restaurants found' });
    }

    const restaurant = rows[0];
    
    // OSM建物データを取得
    let buildingPolygon = null;
    if (restaurant.osm_building_id) {
      const buildingQuery = `
        SELECT osm_id, name, building_type, geometry_coordinates
        FROM osm_buildings 
        WHERE osm_id = ?
      `;
      const [buildingRows] = await pool.execute(buildingQuery, [restaurant.osm_building_id]);
      
      if (buildingRows.length > 0) {
        const building = buildingRows[0];
        buildingPolygon = {
          type: 'Feature',
          properties: {
            building: building.building_type || 'yes',
            osm_id: building.osm_id,
            name: building.name
          },
          geometry: {
            type: 'Polygon',
            coordinates: JSON.parse(building.geometry_coordinates)
          }
        };
      }
    }

    // レスポンス作成
    const response = {
      restaurant: {
        id: restaurant.id,
        name: restaurant.name,
        address: restaurant.address,
        openingHours: restaurant.opening_hours,
        rating: parseFloat(restaurant.rating),
        lat: parseFloat(restaurant.lat),
        lng: parseFloat(restaurant.lng),
        osmBuildingId: restaurant.osm_building_id
      },
      buildingPolygon,
      message: `${restaurant.name}が見つかりました`
    };

    res.json(response);
    
  } catch (error) {
    console.error('Database error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 最適化版レストラン検索API
app.post('/api/search/optimized', async (req, res) => {
  try {
    const { lat, lng } = req.body;
    
    if (!lat || !lng) {
      return res.status(400).json({ error: 'Latitude and longitude are required' });
    }

    // 最も近いレストランを検索
    const query = `
      SELECT 
        id,
        name,
        address,
        opening_hours,
        rating,
        lat,
        lng,
        osm_building_id,
        SQRT(POW(lat - ?, 2) + POW(lng - ?, 2)) as distance
      FROM restaurants
      ORDER BY distance
      LIMIT 1
    `;
    
    const [rows] = await pool.execute(query, [lat, lng]);
    
    if (rows.length === 0) {
      return res.status(404).json({ error: 'No restaurants found' });
    }

    const restaurant = rows[0];
    
    const response = {
      restaurant: {
        id: restaurant.id,
        name: restaurant.name,
        address: restaurant.address,
        openingHours: restaurant.opening_hours,
        rating: parseFloat(restaurant.rating),
        lat: parseFloat(restaurant.lat),
        lng: parseFloat(restaurant.lng),
        osmBuildingId: restaurant.osm_building_id
      },
      osmBuildingId: restaurant.osm_building_id,
      message: `${restaurant.name}が見つかりました (データベース検索)`
    };

    res.json(response);
    
  } catch (error) {
    console.error('Database error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 全レストラン取得API
app.get('/api/restaurants', async (req, res) => {
  try {
    const query = 'SELECT * FROM restaurants ORDER BY rating DESC';
    const [rows] = await pool.execute(query);
    res.json(rows);
  } catch (error) {
    console.error('Database error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// サーバー起動
app.listen(PORT, () => {
  console.log(`🚀 Restaurant Search API Server running on port ${PORT}`);
  console.log(`📍 Health check: http://localhost:${PORT}/health`);
});

// graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, closing database pool...');
  await pool.end();
  process.exit(0);
});