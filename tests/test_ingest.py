from io import StringIO
from pathlib import Path

import pytest

from ingest import validate_and_save


def test_csv_valid_disimpan(tmp_path):
    fixture = Path("fixtures/sample.csv")

    with fixture.open(encoding="utf-8") as source:
        count = validate_and_save(source, tmp_path / "hasil.csv")

    result = (tmp_path / "hasil.csv").read_text(encoding="utf-8")
    assert count == 2
    assert "contoh-001" in result
    assert "contoh-002" in result


def test_kolom_hilang_ditolak(tmp_path):
    csv_tanpa_mag = StringIO(
        "time,latitude,longitude,depth,id\n"
        "2026-01-01T00:00:00.000Z,-6.2,106.8,10,contoh-001\n"
    )

    with pytest.raises(ValueError, match="mag"):
        validate_and_save(csv_tanpa_mag, tmp_path / "hasil.csv")

    assert not (tmp_path / "hasil.csv").exists()