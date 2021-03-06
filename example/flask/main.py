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
