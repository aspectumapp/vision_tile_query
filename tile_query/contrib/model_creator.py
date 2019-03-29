import geoalchemy2.types as geotypes
import sqlalchemy as sa
from sqlalchemy.exc import NoSuchColumnError

from opensource.tile_query.config import GEOMETRY_COL_NAME
from opensource.tile_query.utils.logger import log
from opensource.tile_query.utils import Base
from opensource.tile_query.utils.database import (
    GET_GEOM_COL_TYPE_QUERY, GET_COLUMNS_QUERY, TYPES_MAPPING
)


class TableManager:

    logger = log

    def __init__(self, engine):
        self.models = {}
        self.s = engine

    def _get_headers(self, table_name: str, schema: str) -> dict:
        cursor = self.s.cursor()
        geom_type_query = GET_GEOM_COL_TYPE_QUERY.format(
            table=table_name, schema=schema
        )

        columns_query = GET_COLUMNS_QUERY.format(
            table=table_name, schema=schema
        )

        cursor.execute(geom_type_query)

        geometry_type = cursor.fetchone()

        if not geometry_type:
            geometry_type = 'GEOMETRY'

        cursor.execute(columns_query)
        columns = cursor.fetchall()

        cursor.close()

        if not columns:
            raise NoSuchColumnError

        headers = {
            column['column_name']: sa.Column(
                column['column_name'],
                TYPES_MAPPING.get(column['data_type'])
            )
            for column in columns
            if column['data_type'] in TYPES_MAPPING
        }

        headers.update({
            '__tablename__': table_name,
            '__table_args__': {
                'schema': schema,
                'extend_existing': True,
            },
            GEOMETRY_COL_NAME: sa.Column(
                geotypes.Geometry(geometry_type=geometry_type, srid=4326),
            ),
        })

        return headers

    async def get_table_model(self, table_name: str, schema: str):
        # Check if model already exists
        model_name = schema + ':' + table_name
        if model_name in self.models:
            return self.models[model_name]

        headers = self._get_headers(table_name, schema)
        new_model = type(table_name, (Base,), headers)

        # Store a new table model
        self.models[model_name] = new_model

        return new_model

    def uncache_table_model(self, table_name, schema):
        model_name = schema + ':' + table_name
        table_model = self.models.get(model_name)
        if table_model:
            Base.metadata.remove(table_model.__table__)
            self.models.pop(model_name)
