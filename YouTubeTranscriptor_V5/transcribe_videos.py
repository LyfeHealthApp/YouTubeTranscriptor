import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import csv

# Ruta de entrada y salida
input_file = "videos.csv"
output_file = "transcripts.csv"

# Leer el archivo CSV
df = pd.read_csv(input_file, sep=';', encoding='ISO-8859-1')
df.columns = df.columns.str.strip()
print("Columnas limpias:", list(df.columns))

# Lista para guardar transcripciones
transcripts = []

# Procesar cada fila
for index, row in df.iterrows():
    title = row['Title']
    link = row['Link']
    creator = row['Creator']

    try:
        video_id = link.split("v=")[1].split("&")[0]
    except IndexError:
        print(f"[❌] Error extrayendo el ID del video desde el link: {link}")
        continue

    print(f"Procesando video: {title} ({video_id})")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Buscar primero un transcript generado automáticamente en inglés
        transcript = None
        for t in transcript_list:
            if t.language_code == 'en' and t.is_generated:
                transcript = t
                break

        # Si no hay uno generado, buscar uno manual
        if transcript is None:
            for t in transcript_list:
                if t.language_code == 'en':
                    transcript = t
                    break

        # Si no se encontró ningún transcript
        if transcript is None:
            print(f"[❌] No se encontró ningún transcript en inglés para '{title}'")
            continue

        transcript_data = transcript.fetch()

        # Imprimir el tipo y algunos datos para depurar
        print(f"[🔍] Tipo de transcript_data: {type(transcript_data)}")
        print(f"[🔍] Contenido parcial: {transcript_data[:2] if isinstance(transcript_data, list) else transcript_data}")

        if isinstance(transcript_data, list) and isinstance(transcript_data[0], dict) and 'text' in transcript_data[0]:
            full_text = " ".join([item['text'] for item in transcript_data])
        else:
            print(f"[❌] Formato inesperado en '{title}'")
            continue


        transcripts.append({
            'Title': title,
            'Link': link,
            'Creator': creator,
            'Transcript': full_text
        })

    except (TranscriptsDisabled, NoTranscriptFound) as e:
        print(f"[❌] Sin transcripción para '{title}': {e}")
    except Exception as e:
        print(f"[❌] Error procesando el video '{title}': {e}")

# Guardar resultados
df_output = pd.DataFrame(transcripts)
df_output.to_csv(output_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
print(f"\n✅ Transcripciones guardadas en: {output_file}")
