import os
from io import StringIO
import pandas as pd

VHI_FOLDER = "vhi_data"
OUTPUT_FILE = "final_vhi.csv"

region_map = {
    1: "Cherkasy",
    2: "Chernihiv",
    3: "Chernivtsi",
    4: "Crimea",
    5: "Dnipropetrovsk",
    6: "Donetsk",
    7: "Ivano-Frankivsk",
    8: "Kharkiv",
    9: "Kherson",
    10: "Khmelnytskyi",
    11: "Kirovohrad",
    12: "Kyiv",
    13: "Luhansk",
    14: "Lviv",
    15: "Mykolaiv",
    16: "Odesa",
    17: "Poltava",
    18: "Rivne",
    19: "Sumy",
    20: "Ternopil",
    21: "Zakarpattia",
    22: "Vinnytsia",
    23: "Volyn",
    24: "Zaporizhzhia",
    25: "Zhytomyr",
    26: "Kyiv City",
    27: "Sevastopol"
}

all_data = []

for filename in os.listdir(VHI_FOLDER):
    if filename.endswith(".csv"):
        file_path = os.path.join(VHI_FOLDER, filename)

        region_id = int(filename.split("_")[2])

        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        cleaned_lines = []

        for line in lines[1:]:
            line = line.replace("<br>", "")
            line = line.replace("<tt><pre>", "")
            line = line.strip()

            if not line:
                continue

            if line.endswith(","):
                line = line[:-1]

            cleaned_lines.append(line)

        csv_text = "\n".join(cleaned_lines)
        df = pd.read_csv(StringIO(csv_text), skipinitialspace=True)

        df.columns = [col.strip() for col in df.columns]

        df["region_id"] = region_id
        df["region"] = region_map.get(region_id, f"Region {region_id}")

        all_data.append(df)

final_df = pd.concat(all_data, ignore_index=True)

for col in ["year", "week", "SMN", "SMT", "VCI", "TCI", "VHI"]:
    final_df[col] = pd.to_numeric(final_df[col], errors="coerce")

final_df = final_df.dropna(subset=["year", "week", "VCI", "TCI", "VHI"])
final_df["year"] = final_df["year"].astype(int)
final_df["week"] = final_df["week"].astype(int)

final_df = final_df.sort_values(by=["region_id", "year", "week"]).reset_index(drop=True)

final_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print("Готово. Створено файл:", OUTPUT_FILE)
print(final_df.head())
print(final_df.shape)