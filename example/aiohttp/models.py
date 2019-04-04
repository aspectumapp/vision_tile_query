import geoalchemy2.types as geotypes
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VectorTable(Base):
    __tablename__ = 'flask_test'

    id = sa.Column(sa.Interval, primary_key=True)

    rackid = sa.Column(sa.BigInteger)
    address = sa.Column(sa.Text)
    ward = sa.Column(sa.BigInteger)
    community_area = sa.Column(sa.BigInteger)
    community_name = sa.Column(sa.Text)
    geometry = sa.Column(geotypes.Geometry(geometry_type='POINT', srid=4326))


class VectorPolyTable(Base):
    __tablename__ = 'flask_pol_test'

    id = sa.Column(sa.Interval, primary_key=True)
    name = sa.Column(sa.Text)
    description= sa.Column(sa.Text)
    geometry = sa.Column(geotypes.Geometry(geometry_type='POLYGON', srid=4326))


vectortable = VectorTable.__table__
polytable = VectorPolyTable.__table__
