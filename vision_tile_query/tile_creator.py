from abc import ABCMeta, abstractmethod

import mercantile
import sqlalchemy as sa
from sqlalchemy.sql.schema import Table


from .utils.logger import log
from .config import (
    MERCATOR_SRID, WEB_MERCATOR_SRID, RELATIVE_BUFFER_WIDTH,
    GEOMETRY_COL_NAME, ID_COL_NAME, POINT_TYPES, SIMPLIFICATION_TYPES,
    SIMPLIFY_COEFFICIENT, DEFAULT_EXTENT
)


class AbstractTileProcessor(metaclass=ABCMeta):
    """
    Abstract class for tile processor with call method
    """
    use_simplification = False
    use_lod = False
    use_clip_by_tile = True

    @abstractmethod
    def get_tile(self, tile: dict, model: sa.table, params: dict) -> sa.sql:
        raise NotImplementedError()

    @abstractmethod
    def construct_selection_columns(self, model, envelope, envelope_extended,
                                    tile_area, zoom):
        raise NotImplementedError()

    @abstractmethod
    def get_geometry_as_mvt(self, model, tile, tile_bounds, params):
        raise NotImplementedError()

    @abstractmethod
    def get_mvt_subquery(self, model, tile, tile_bounds, params):
        raise NotImplementedError()

    @staticmethod
    def coordinates_to_bbox(tile: dict) -> mercantile.Tile:
        """Creating Bbox from x, y, z coordinates"""

        tile_bounds = mercantile.bounds(
            int(tile.get('x')),
            int(tile.get('y')),
            int(tile.get('z')),
        )

        return tile_bounds

    @staticmethod
    def get_extended_bounds(bounds: (list, tuple)) -> tuple:
        """
        Returns coordinates for bounds wider by `buffer_width`
        in each direction
        """

        buffer_width = abs(bounds[2] - bounds[0]) * RELATIVE_BUFFER_WIDTH

        return (
            max(bounds[0] - buffer_width, -180),
            max(bounds[1] - buffer_width, -89),
            min(bounds[2] + buffer_width, 180),
            min(bounds[3] + buffer_width, 89)
        )

    @staticmethod
    def get_bounds_area(bounds):
        """ Returns area in square degrees for bounding box """

        width = abs(bounds[2] - bounds[0])
        height = abs(bounds[3] - bounds[1])

        return width * height

    @staticmethod
    def get_mercator_envelope(bounds):
        return sa.func.ST_MakeEnvelope(*tuple(bounds), MERCATOR_SRID)

    @staticmethod
    def get_simplify_coefficient(zoom):
        multiplier = 99 * ((7 / 10) ** zoom) + 1
        return SIMPLIFY_COEFFICIENT / multiplier


class VisionBaseTileProcessor(AbstractTileProcessor):
    """
    Base class for processing tiles from database,
    calculate bbox, convert them to pbf
    """
    log = log

    def get_mvt_subquery(self, model, tile, tile_bounds, params):
        # Tile bounds with buffer. Use in filter for objects
        bounds_extended = self.get_extended_bounds(tile_bounds)

        tile_area = self.get_bounds_area(tile_bounds)

        envelope = self.get_mercator_envelope(tile_bounds)
        envelope_extended = self.get_mercator_envelope(bounds_extended)

        columns_to_select = self.construct_selection_columns(
            model=model,
            envelope=envelope,
            envelope_extended=envelope_extended,
            tile_area=tile_area,
            zoom=int(tile.get('z')),
        )

        where_clause = sa.and_(
            sa.func.ST_IsEmpty(model.columns[GEOMETRY_COL_NAME]).is_(False),
            model.columns[GEOMETRY_COL_NAME].op('&&')(envelope),
        )

        sub_query = (
            sa.select(columns_to_select).where(where_clause)
        )

        return sub_query

    def geom_simplify(self, geom_column, tile_area, zoom):

        simplify = self.get_simplify_coefficient(zoom)
        return sa.func.ST_SimplifyVW(
            geom_column, simplify * tile_area
        )

    def select_geom_col(self, model, envelope_extended, tile_area, zoom):
        geom_column = model.columns[GEOMETRY_COL_NAME]
        geometry_type = geom_column.type.geometry_type

        if self.use_clip_by_tile:
            geom_column = sa.func.ST_ClipByBox2D(
                geom_column, envelope_extended)

        if self.use_simplification and geometry_type in SIMPLIFICATION_TYPES:
            geom_column = self.geom_simplify(geom_column, tile_area, zoom)

        return geom_column

    def construct_selection_columns(self, model, envelope, envelope_extended,
                                    tile_area, zoom):

        geom_sel_column = self.select_geom_col(
            model, envelope_extended, tile_area, zoom
        )

        columns_to_select = [
            model.columns[ID_COL_NAME],
            sa.func.ST_AsMVTGeom(
                sa.func.ST_Transform(geom_sel_column, WEB_MERCATOR_SRID),
                sa.func.ST_Transform(envelope, WEB_MERCATOR_SRID),
                DEFAULT_EXTENT, 256, False
            ).label('geom')
        ]

        return columns_to_select

    def get_geometry_as_mvt(self, model, tile, tile_bounds, params):
        """
        Method that performs getting geometry as MVT.
        All geometries get by random using TABLESAMPLE with limitation by
        points per tile.
        """
        geometry_type = model.columns[GEOMETRY_COL_NAME].type.geometry_type

        # Bt default don't use TABLESAMPLE for polygons and lines
        table = model
        if self.use_lod and geometry_type in POINT_TYPES:
            if params.get('percentage'):
                percentage = params['percentage']
            else:
                percentage = 100
            # Use TABLESAMPLE for getting exact same random data from table
            table = model.tablesample(
                sa.func.bernoulli(percentage),
                seed=sa.cast(0, sa.Integer)
            )

        # Don't use TABLESAMPLE for polygons and lines

        sub_query = self.get_mvt_subquery(
            table, tile, tile_bounds, params
        )

        return sa.select([
            sa.func.ST_AsMVT(sa.column('q'), 'layer', DEFAULT_EXTENT, 'geom')
        ]).select_from(
            sub_query.alias('q')
        )

    def get_tile(self, tile: dict, model: Table,
                 params: dict = None) -> sa.sql:
        """
        Main method for get tile in MVT format
        :param tile: query path params including x, y, z
        :param model: sqlalchemy table model
        :param params: additional request settings
        :return:
        """
        tile_bounds = self.coordinates_to_bbox(tile)

        return self.get_geometry_as_mvt(
             model, tile, tile_bounds, params
        )
