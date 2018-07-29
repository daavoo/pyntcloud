import pytest

from pyntcloud import PyntCloud

from test_from_file import assert_points_xyz, assert_points_color, assert_mesh


@pytest.mark.parametrize("extension,color,mesh", [
    (".ply", True, True),
    ("_ascii.ply", True, True),
    (".npz", True, True),
    (".obj", False, False),
    (".bin", False, False)
])
def test_to_file(tmpdir, diamond, extension, color, mesh):
    extra_write_args = {}
    if mesh:
        extra_write_args["also_save"] = ["mesh"]
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


def test_to_bin_raises_ValueError_if_invalid_kwargs(tmpdir, diamond):
    with pytest.raises(ValueError):
        diamond.to_file(str(tmpdir.join("written.bin")), also_save=["mesh"])