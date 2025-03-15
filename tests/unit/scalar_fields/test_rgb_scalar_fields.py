import pytest

from pyntcloud.scalar_fields.rgb import (
    HueSaturationValue,
    RelativeLuminance,
    RGBIntensity,
)


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_HueSaturationValue_bounds(pyntcloud_with_rgb_and_normals):
    scalar_field = HueSaturationValue(pyntcloud=pyntcloud_with_rgb_and_normals)
    scalar_field.extract_info()
    scalar_field.compute()
    assert min(scalar_field.to_be_added["H"]) >= 0
    assert max(scalar_field.to_be_added["H"]) <= 360
    assert min(scalar_field.to_be_added["S"]) >= 0
    assert max(scalar_field.to_be_added["S"]) <= 1
    assert min(scalar_field.to_be_added["V"]) >= 0
    assert max(scalar_field.to_be_added["V"]) <= 100


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_RelativeLuminance_bounds(pyntcloud_with_rgb_and_normals):
    scalar_field = RelativeLuminance(pyntcloud=pyntcloud_with_rgb_and_normals)
    scalar_field.extract_info()
    scalar_field.compute()
    assert min(scalar_field.to_be_added["relative_luminance"]) >= 0
    assert max(scalar_field.to_be_added["relative_luminance"]) <= 255


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_RGBIntensity_bounds(pyntcloud_with_rgb_and_normals):
    scalar_field = RGBIntensity(pyntcloud=pyntcloud_with_rgb_and_normals)
    scalar_field.extract_info()
    scalar_field.compute()
    assert min(scalar_field.to_be_added["Ri"]) >= 0
    assert max(scalar_field.to_be_added["Ri"]) <= 1
    assert min(scalar_field.to_be_added["Gi"]) >= 0
    assert max(scalar_field.to_be_added["Gi"]) <= 1
    assert min(scalar_field.to_be_added["Bi"]) >= 0
    assert max(scalar_field.to_be_added["Bi"]) <= 1
