import pytest

from pyntcloud import PyntCloud

from test_from_file import assert_points_xyz, assert_points_color, assert_mesh


@pytest.mark.parametrize("extension,color,mesh,comments", [
    (".ply", True, True, False),
    ("_ascii.ply", True, True, True),
    (".npz", True, True, False),
    (".obj", False, True, False),
    (".bin", False, False, False)
])
def test_to_file(tmpdir, diamond, extension, color, mesh, comments):
    extra_write_args = {}
    if mesh:
        extra_write_args["also_save"] = ["mesh"]
    if comments:
        extra_write_args["comments"] = ["PyntCloud is cool"]
    if extension == ".ply":
        extra_write_args["as_text"] = False
    if extension == "_ascii.ply":
        extra_write_args["as_text"] = True

    diamond.to_file(str(tmpdir.join("written{}".format(extension))), **extra_write_args)

    written_file = PyntCloud.from_file(str(tmpdir.join("written{}".format(extension))))

    assert_points_xyz(written_file)
    if color:
        assert_points_color(written_file)
    if mesh:
        assert_mesh(written_file)
    if comments:
        assert written_file.comments == ["PyntCloud is cool"]


def test_to_bin_raises_ValueError_if_invalid_kwargs(tmpdir, diamond):
    with pytest.raises(ValueError):
        diamond.to_file(str(tmpdir.join("written.bin")), also_save=["mesh"])


def test_write_ply_with_bool(plane_pyntcloud, tmp_path):
    """Expectation: a PyntCloud class holding Boolean column within `points` can be written and re-read as a PLY file.

    After adding the new column, we have the following DataFrame under plane_pyntcloud.points:

        x    y    z  bool_col
    0  0.0  0.0  0.0      True
    1  1.0  1.0  0.0      True
    2  2.0  2.0  0.0     False
    3  1.0  2.0  0.0      True
    4  0.1  0.2  0.3      True
    """
    # Insert the additional column of dtype: bool.
    plane_pyntcloud.points["bool_col"] = plane_pyntcloud.points.x < 2

    # Write the DataFrame containing Boolean data.
    ply_out = (tmp_path / "test_file.ply").as_posix()
    plane_pyntcloud.to_file(ply_out)

    # Reload the test file and compare it is exactly as it was before writing.
    new_pyntcloud = PyntCloud.from_file(ply_out, allow_bool=True)
    assert new_pyntcloud.points.equals(plane_pyntcloud.points), "Re-read pyntcloud is not identical to before writing"
