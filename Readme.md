## EOS vision tile query library

Vector tile query library create MVT tiles SQL query by XYZ.

## Architecture
Vision tile query library provide postgis MVT SQL query with special 
abilities. Polygon simplification and geometries count simplification 
according zoom level are main features. Reade more about postgis+MVT
https://postgis.net/docs/ST_AsMVT.html

### Installing
Use pip with project url
```text
pip install git+ssh://github.com/eos-vision/eos-vision-tile-query

``` 
### Usage examples
Tile query library requires SQLalchemy table model for constructing SQL query 
#### Flask
```text
import os
from flask import Flask
from models import VectorTable
from sqlalchmey import create_engine
from eos-vision.tile_query import VisionBaseTileProcessor

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')
# Connect to DB


@app.route('tile/<table_name>/<z>/<x>/<y>.pbf')
def hello_name(name):
    tile = {'x': x, 'y': y, 'z': z}
    tile_query = VisionBaseTileProcessor.get_tile(tile, VectorTable)
    conn = app.engine.connect()
    tile = conn.execute(tile_query)
    conn.close()
    return bytes(tile)

if __name__ == '__main__':
    app.run()
```

#### Aiohttp
Will be soon

### Requirements
 - mercantile==0.10.0
 - SQLAlchemy==1.1.11
 - geoalchemy2==0.4.0