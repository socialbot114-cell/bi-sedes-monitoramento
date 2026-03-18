import csv
import json
import os
from collections import defaultdict
from datetime import datetime
import re

# Configurações
CSV_PATH = (
    "/home/richard/Documentos/monitoramento /mt_vw_mpdft_atendimentos_202603181027.csv"
)
OUTPUT_DIR = "/home/richard/Documentos/monitoramento /bi-sedes-monitoramento/data"


def get_category(unit_name):
    name = unit_name.upper()
    if "CRAS" in name:
        return "CRAS"
    if "CREAS" in name:
        return "CREAS"
    if any(
        k in name
        for k in ["ACOLHIMENTO", "UAI", "SAIAFA", "CASA SOCIAL", "INCLUSÃO", "INCLUSAO"]
    ):
        return "ACOLHIMENTO"
    if "CENTRO POP" in name:
        return "CENTRO POP"
    if any(k in name for k in ["MÃOS SOLIDÁRIAS", "MAOS SOLIDARIAS"]):
        return "MÃOS SOLIDÁRIAS"
    if "CENTRO DIA" in name:
        return "CENTRO DIA"
    if "CECON" in name:
        return "CECON"
    return "OUTROS"


def process_data():
    print("Iniciando processamento com Categorização Estratégica...")

    # Estrutura: [ano][mes][dia][categoria][unidade] = total
    data_tree = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        )
    )
    unit_map = defaultdict(set)  # Para saber quais unidades pertencem a qual categoria

    try:
        with open(CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_str = row["DATA ATENDIMENTO"]
                unidade = row["unidade"]
                categoria = get_category(unidade)

                dt = datetime.strptime(data_str, "%Y-%m-%d")
                data_tree[dt.year][dt.month][dt.day][categoria][unidade] += 1
                unit_map[categoria].add(unidade)

        # Formatar para JSON leve (Agregado por Dia/Categoria/Unidade)
        final_data = []
        for ano, meses in data_tree.items():
            for mes, dias in meses.items():
                for dia, categorias in dias.items():
                    for cat, unidades in categorias.items():
                        cat_total = sum(unidades.values())
                        final_data.append(
                            {
                                "y": ano,
                                "m": mes,
                                "d": dia,
                                "c": cat,
                                "t": cat_total,
                                "u": [{"n": u, "t": t} for u, t in unidades.items()],
                            }
                        )

        # Salvar Mapeamento de Unidades por Categoria
        unit_mapping_json = {
            cat: sorted(list(units)) for cat, units in unit_map.items()
        }

        with open(os.path.join(OUTPUT_DIR, "bi_data_v2.json"), "w") as f:
            json.dump(final_data, f)

        with open(os.path.join(OUTPUT_DIR, "unit_mapping.json"), "w") as f:
            json.dump(unit_mapping_json, f)

        print(f"Sucesso! BI Data V2 salvo em {OUTPUT_DIR}")

    except Exception as e:
        print(f"Erro no processamento: {e}")


if __name__ == "__main__":
    process_data()
