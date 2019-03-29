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