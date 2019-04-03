# Default SRID numbers
MERCATOR_SRID = 4326
WEB_MERCATOR_SRID = 3857

# MVT query settings
# 1% of tile width
RELATIVE_BUFFER_WIDTH = 0.01
# default tile extent value. See details https://postgis.net/docs/ST_AsMVT.html
DEFAULT_EXTENT = 4096
# 0.5% of tile area fow VM polygons simplification
SIMPLIFY_COEFFICIENT = 0.000005

# Default columns names
GEOMETRY_COL_NAME = 'geometry'
ID_COL_NAME = 'id'

# Vector objects types
POINT_TYPES = ['POINT', 'MULTIPOINT']
POLYGON_TYPES = ['POLYGON', 'MULTIPOLYGON']
LINE_TYPES = ['LINESTRING', 'MULTILINESTRING']
SIMPLIFICATION_TYPES = LINE_TYPES + POLYGON_TYPES
