import pytest
from vision_tile_query import VisionBaseTileProcessor
import geoalchemy2.types as geotypes
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VectorTable(Base):
    __tablename__ = 'points_data_test'

    id = sa.Column(sa.Interval, primary_key=True)

    rackid = sa.Column(sa.BigInteger)
    address = sa.Column(sa.Text)
    ward = sa.Column(sa.BigInteger)
    community_area = sa.Column(sa.BigInteger)
    community_name = sa.Column(sa.Text)
    geometry = sa.Column(geotypes.Geometry(geometry_type='POINT', srid=4326))


class VectorPolyTable(Base):
    __tablename__ = 'poly_data_test'

    id = sa.Column(sa.Interval, primary_key=True)
    name = sa.Column(sa.Text)
    description= sa.Column(sa.Text)
    geometry = sa.Column(geotypes.Geometry(geometry_type='POLYGON', srid=4326))


@pytest.fixture
def polytable():
    return VectorPolyTable.__table__


@pytest.fixture
def vectortable():
    return VectorTable.__table__


@pytest.fixture
def tileprocessor():
    return VisionBaseTileProcessor()
