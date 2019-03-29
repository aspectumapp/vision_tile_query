# Utils functions for database
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import UUID

# EOS static dataset Columns
GEOMETRY_COL_NAME = 'geometry'
ID_COL_NAME = 'eos_id'
IS_EDITABLE_COL = 'eos_is_editable'
CATEGORY_COL_NAME = 'eos_category'


def get_table_name(model):
    return '{}.{}'.format(model.__table_args__['schema'], model.__tablename__)


GET_GEOM_COL_TYPE_QUERY = """
    SELECT
        type
    FROM
        geometry_columns
    WHERE
        f_table_name = '{table}'
        AND f_table_schema = '{schema}';
"""

GET_COLUMNS_QUERY = """
    SELECT
        column_name, data_type
    FROM
        information_schema.columns
    WHERE
        table_name = '{table}'
        AND table_schema = '{schema}'
"""

TYPES_MAPPING = {
    'abstime': sa.Time,
    'ARRAY': sa.ARRAY,
    'bigint': sa.BigInteger,
    'boolean': sa.Boolean,
    '"char"': sa.CHAR,
    'character': sa.CHAR,
    'character varying': sa.NVARCHAR,
    'double precision': sa.DECIMAL,
    'integer': sa.Integer,
    'json': sa.JSON,
    'numeric': sa.Numeric,
    'real': sa.REAL,
    'smallint': sa.SmallInteger,
    'text': sa.Text,
    'timestamp without time zone': sa.TIMESTAMP,
    'timestamp with time zone': sa.TIMESTAMP,
    'USER-DEFINED': None,
    'uuid': UUID,
}
