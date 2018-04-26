import pytest


@pytest.mark.parametrize("scalar_field", [
    "hsv", "relative_luminance", "rgb_intensity"
])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_KeyError_is_raised_when_rgb_is_missing(simple_pyntcloud, scalar_field):
    with pytest.raises(KeyError):
        simple_pyntcloud.add_scalar_field(
            scalar_field)


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_hsv_bounds(pyntcloud_with_rgb_and_normals):
    pyntcloud_with_rgb_and_normals.add_scalar_field(
        "hsv")
    assert min(pyntcloud_with_rgb_and_normals.points["H"]) >= 0
    assert max(pyntcloud_with_rgb_and_normals.points["H"]) <= 360
    assert min(pyntcloud_with_rgb_and_normals.points["S"]) >= 0
    assert max(pyntcloud_with_rgb_and_normals.points["S"]) <= 1
    assert min(pyntcloud_with_rgb_and_normals.points["V"]) >= 0
    assert max(pyntcloud_with_rgb_and_normals.points["V"]) <= 100


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_relative_luminance_bounds(pyntcloud_with_rgb_and_normals):
    pyntcloud_with_rgb_and_normals.add_scalar_field(
        "relative_luminance")
    assert min(pyntcloud_with_rgb_and_normals.points["relative_luminance"]) >= 0
    assert max(pyntcloud_with_rgb_and_normals.points["relative_luminance"]) <= 255


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_rgb_intensity_bounds(pyntcloud_with_rgb_and_normals):
    pyntcloud_with_rgb_and_normals.add_scalar_field(
        "rgb_intensity")
    assert min(pyntcloud_with_rgb_and_normals.points["Ri"]) >= 0
    assert max(pyntcloud_with_rgb_and_normals.points["Ri"]) <= 1
    assert min(pyntcloud_with_rgb_and_normals.points["Gi"]) >= 0
    assert max(pyntcloud_with_rgb_and_normals.points["Gi"]) <= 1
    assert min(pyntcloud_with_rgb_and_normals.points["Bi"]) >= 0
    assert max(pyntcloud_with_rgb_and_normals.points["Bi"]) <= 1
