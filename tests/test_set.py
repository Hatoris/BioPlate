import pytest

from BioPlate.core.set import plate_set



@pytest.mark.parametrize("elements,results", [
    (("A1", "Bob"), "2")
])
def test_plate_set(elements, results):
    assert plate_set == results


if __name__ == "__main__":
    pytest.main(".")