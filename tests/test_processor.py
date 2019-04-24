import pytest
import sqlalchemy as sa

TILES_SET = (
    {'z': 4, 'x': 10, 'y': 4},
    {'z': 5, 'x': 22, 'y': 10},
    {'z': 5, 'x': 0, 'y': 10},
    {'z': 6, 'x': 21, 'y': 37},
    {'z': 6, 'x': 13, 'y': 26},
    {'z': 7, 'x': 77, 'y': 67},
    {'z': 7, 'x': 62, 'y': 60},
    {'z': 8, 'x': 140, 'y': 104},
    {'z': 8, 'x': 145, 'y': 100},
    {'z': 9, 'x': 256, 'y': 170},
    {'z': 9, 'x': 291, 'y': 188},
    {'z': 10, 'x': 823, 'y': 438},
    {'z': 10, 'x': 887, 'y': 606},
    {'z': 11, 'x': 1283, 'y': 1164},
    {'z': 11, 'x': 576, 'y': 681},
)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_points_data(tileprocessor, vectortable, tile):
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_poly_data(tileprocessor, polytable, tile):
    tile_query = tileprocessor.get_tile(
        tile, model=polytable)

    assert isinstance(tile_query, sa.sql.selectable.Select)