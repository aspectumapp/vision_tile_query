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


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_params_use_lod(tileprocessor, vectortable, tile):
    tileprocessor.use_lod = True
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_params_lod_percentages_0(tileprocessor, vectortable, tile):
    params = {'percentage': 0}
    tileprocessor.use_lod = True
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable, params=params)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_params_lod_percentages_50(
        tileprocessor, vectortable, tile):
    tileprocessor.use_lod = True
    params = {'percentage': 50}
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable, params=params)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_params_lod_percentages_100(
        tileprocessor, vectortable, tile):
    tileprocessor.use_lod = True
    params = {'percentage': 100}
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable, params=params)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_params_enable_simplificastion(
        tileprocessor, vectortable, tile):
    tileprocessor.use_simplification = True
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_params_enable_simplificastion(
        tileprocessor, vectortable, tile):
    tileprocessor.use_simplification = True
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_params_enable_simplificastion_0(
        tileprocessor, vectortable, tile):
    tileprocessor.use_simplification = True
    params = {'simplify': 0.00001}
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable, params=params)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_params_enable_simplificastion_50(
        tileprocessor, vectortable, tile):
    tileprocessor.use_simplification = True
    params = {'simplify': 0.00005}
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable, params=params)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_with_params_enable_simplificastion_100(
        tileprocessor, vectortable, tile):
    tileprocessor.use_simplification = True
    params = {'simplify': 0.0001}
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable, params=params)

    assert isinstance(tile_query, sa.sql.selectable.Select)


@pytest.mark.parametrize("tile", TILES_SET)
def test_query_disable_clip_to_tile(
        tileprocessor, vectortable, tile):
    tileprocessor.use_clip_by_tile = False
    tile_query = tileprocessor.get_tile(
        tile, model=vectortable)

    assert isinstance(tile_query, sa.sql.selectable.Select)
