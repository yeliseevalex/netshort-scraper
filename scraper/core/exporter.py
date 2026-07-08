import csv
from pathlib import Path


OUTPUT_DIR = Path("output")


def save_csv(data, filename="series.csv"):
    if not data:
        raise ValueError("No data to save")

    OUTPUT_DIR.mkdir(exist_ok=True)

    file_path = OUTPUT_DIR / filename

    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Series title",
                "Series URL",
                "Cover image URL",
                "Description",
                "Genre",
                "Number of episodes",
                "Status",
                "Tags / ranking"
            ]
        )

        writer.writeheader()

        rows = []

        for item in data:
            rows.append({
                "Series title": item.title,
                "Series URL": item.url,
                "Cover image URL": item.cover_image,
                "Description": item.description,
                "Genre": item.genre,
                "Number of episodes": item.episodes,
                "Status": item.status,
                "Tags / ranking": item.tags
            })

        writer.writerows(rows)

    print(f"CSV saved: {file_path}")