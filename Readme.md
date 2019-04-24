## EOS vision tile query library 

vision_tile_query is a library for creating SQL with PostGIS As_MVT by XYZ.
It can be used for constructing vector servers
## Architecture
Vision tile query library provides PostGIS MVT SQL query with special 
abilities. Polygon simplification and geometries count simplification 
according to zoom level are the main features. Read more about postgis+MVT 
https://postgis.net/docs/ST_AsMVT.html
### Installing
Simple run
```text
pip install vision-tile-query

``` 
### Usage examples
Tile query library requires SQLalchemy table model for constructing SQL query 
#### Flask
Example for flask framework with sqlalchemy DB engine
```python
from flask import Flask, render_template
from sqlalchemy import create_engine
from vision_tile_query import VisionBaseTileProcessor
from vision_tile_query import TableManager

app = Flask(__name__)
# Connect to DB
app.engine = create_engine('postgresql://postgres@localhost:5432/vision_db')
table_manager = TableManager(app.engine)


@app.route('/')
def map_page():
    return render_template('main.html')


@app.route('/tile/<table>/<zoom>/<x_tile>/<y_tile>.pbf')
def get_tile(table, x_tile, y_tile, zoom):
    tile = {'x': x_tile, 'y': y_tile, 'z': zoom}

    # Define model
    model = table_manager.get_table_model(
            table, 'public')

    tile_query = VisionBaseTileProcessor().get_tile(
        tile, model=model.__table__)

    # Exec query and get data
    conn = app.engine.connect()
    query = conn.execute(tile_query)
    tile = query.fetchone()
    conn.close()

    # Make response object
    response = app.make_response(bytes(tile[0]))
    response.headers['Content-Type'] = 'application/x-protobuf'
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


if __name__ == '__main__':
    app.run()
```

#### Aiohttp
Simple aiohttp example for MVT tile server with async table manager
```python
import asyncio
import aiohttp_jinja2
import jinja2
import aiopg.sa
from sqlalchemy.engine.url import URL
from aiohttp import web

from vision_tile_query import VisionBaseTileProcessor, AsyncTableManager

DNS = str(URL(
    database='vision_db',
    host='localhost',
    username='postgres',
    drivername='postgres',
))


async def init_pg(app):
    app['db'] = await aiopg.sa.create_engine(DNS)
    app['table_manager'] = AsyncTableManager(app['db'])


async def close_pg_connection(app):
    app['db'].close()
    await app['db'].wait_closed()


async def get_tile(request):
    params = dict(request.match_info)

    tile = {'x': int(params.get('x')),
            'y': int(params.get('y')),
            'z': int(params.get('z'))}

    # Define model
    model = await app['table_manager'].get_table_model(
        params.get('table'), 'public')

    tile_query = VisionBaseTileProcessor().get_tile(
        tile, model=model.__table__)

    async with app['db'].acquire() as conn:
        data = await conn.scalar(tile_query)

    response = web.Response(
            body=bytes(data),
            headers={
                'Content-Type': "application/x-protobuf",
            }
        )
    return response


@aiohttp_jinja2.template('main.html')
async def handle(request):
    return {'KEY': 'YOUR MAPBOX TOKEN'}


loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
app.add_routes([web.get("/", handle),
                web.get("/tile/{table}/{z}/{x}/{y}.pbf", get_tile)
                ])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

app.update(name='vision-tile-query')

# signal on app start
app.on_startup.append(init_pg)
# signal on app end
app.on_cleanup.append(close_pg_connection)

web.run_app(app)
```

### Settings
Main module settings are:
  - use_simplification - simplify geometry of polygons and lines. 
  By default False
  - use_lod - use LOD for points objects, don't select all object on 
  world(1-7) zoom levels. By default False
  - use_clip_by_tile - usefull for multipolygons, this attribute enables 
  postgis `ST_ClipByBox2D`. By default True
Also you can configure additional settings such as:
  - percentage - number value from 0 to 100. How much percent library have 
  to use in postgres TABLESAMPLE function
  - simplify - library uses postgis function ST_Simplify. Simplify provide 
  square size depending to you coordinate system

### Tests
  For run test on your machine use `python pytest -v`

### Requirements
 - mercantile>=0.10.0
 - SQLAlchemy>=1.1.11
 - geoalchemy2>=0.4.0