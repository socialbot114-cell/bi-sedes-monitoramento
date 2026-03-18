import csv
import json
import os
from collections import defaultdict
from datetime import datetime

# Configurações
CSV_PATH = (
    "/home/richard/Documentos/monitoramento /mt_vw_mpdft_atendimentos_202603181027.csv"
)
OUTPUT_DIR = "/home/richard/Documentos/monitoramento /bi-sedes-monitoramento/data"


def process_data():
    print("Iniciando processamento nativo de 1.7M de registros...")

    daily_stats = defaultdict(int)
    unit_stats = defaultdict(int)

    try:
        with open(CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_str = row["DATA ATENDIMENTO"]
                unidade = row["unidade"]

                # Agregação Diária
                daily_stats[data_str] += 1

                # Agregação por Unidade
                unit_stats[unidade] += 1

        # Formatar estatísticas diárias para o JSON
        daily_json = []
        for data_str, total in daily_stats.items():
            dt = datetime.strptime(data_str, "%Y-%m-%d")
            daily_json.append(
                {
                    "DATA ATENDIMENTO": data_str,
                    "ano": dt.year,
                    "mes": dt.month,
                    "dia": dt.day,
                    "total": total,
                }
            )

        # Formatar unidades (Top 20)
        unit_json = sorted(
            [{"unidade": u, "total": t} for u, t in unit_stats.items()],
            key=lambda x: x["total"],
            reverse=True,
        )[:20]

        # Salvar
        with open(os.path.join(OUTPUT_DIR, "daily_stats.json"), "w") as f:
            json.dump(daily_json, f)

        with open(os.path.join(OUTPUT_DIR, "unit_stats.json"), "w") as f:
            json.dump(unit_json, f)

        print(f"Sucesso! Dados salvos em {OUTPUT_DIR}")

    except Exception as e:
        print(f"Erro no processamento: {e}")


if __name__ == "__main__":
    process_data()
