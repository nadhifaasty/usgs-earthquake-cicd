import argparse
import csv
from pathlib import Path
from urllib.request import urlopen

FEED_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.csv"
REQUIRED_COLUMNS = ("id", "time", "latitude", "longitude", "depth", "mag")


def validate_and_save(source, output):
    reader = csv.DictReader(source)
    columns = reader.fieldnames or []
    missing = [column for column in REQUIRED_COLUMNS if column not in columns]

    if missing:
        raise ValueError(f"Kolom wajib tidak ada: {', '.join(missing)}")

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with output.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            writer.writerow(row)
            count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description="Ambil data gempa USGS")
    parser.add_argument("--output", default="out/earthquakes.csv")
    args = parser.parse_args()

    with urlopen(FEED_URL, timeout=30) as response:
        lines = (line.decode("utf-8-sig") for line in response)
        count = validate_and_save(lines, args.output)

    print(f"Berhasil menyimpan {count} kejadian ke {args.output}")


if __name__ == "__main__":
    main()