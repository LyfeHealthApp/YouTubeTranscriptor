import pandas as pd
import os

# Ruta del archivo original
INPUT_FILE = "videos.csv"
CHUNK_SIZE = 1000
OUTPUT_FOLDER = "chunks"

# Crear carpeta si no existe
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Leer CSV original
df = pd.read_csv(INPUT_FILE, sep=';', encoding='ISO-8859-1')

# Dividir en bloques de 1000
for i, start in enumerate(range(0, len(df), CHUNK_SIZE)):
    chunk = df.iloc[start:start + CHUNK_SIZE]
    output_name = f"{OUTPUT_FOLDER}/videos_{i+1:04}.csv"
    chunk.to_csv(output_name, sep=';', index=False, encoding='utf-8')
    print(f"✅ Guardado: {output_name} ({len(chunk)} videos)")
