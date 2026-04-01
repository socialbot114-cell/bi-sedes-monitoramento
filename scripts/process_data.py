import csv
import json
import os
from collections import defaultdict
from datetime import datetime

CSV_PATH = "/home/richard/Documentos/monitoramento /NOVOS DADOS 01 ABRIL.csv"
OUTPUT_DIR = "/home/richard/Documentos/monitoramento /bi-sedes-monitoramento/data"


def get_strategic_group(unit_name):
    name = unit_name.upper().strip()
    if any(k in name for k in ["CRAS", "CREAS", "CENTRO POP"]):
        return "CRAS / CREAS / CENTRO POP"
    if any(k in name for k in ["ACOLHIMENTO", "UAI", "SAIAFA", "CASA SOCIAL"]):
        return "UNIDADE ACOLHIMENTO"
    if any(k in name for k in ["OSC", "POSTO", "MÃOS SOLIDÁRIAS", "MAOS SOLIDARIAS"]):
        return "OSC & POSTO"
    return "CECON / GESTÃO"


def process_data():
    print("Iniciando processamento v5 (2025-2026 + Perfil Servidor)...")

    # Estrutura principal: [ano][mes][dia][grupo]
    daily_tree = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    )
    # Detalhes: [ano][mes][grupo] -> { units: {}, profiles: {} }
    details_tree = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(
                lambda: {"units": defaultdict(int), "profiles": defaultdict(int)}
            )
        )
    )
    annual_totals = defaultdict(int)

    try:
        with open(CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_str = row["DATA ATENDIMENTO"]
                unidade = row["unidade"]
                perfil = row["perfil_servidor"]
                if not unidade:
                    continue

                try:
                    dt = datetime.strptime(data_str, "%Y-%m-%d")
                    if dt.year < 2025:
                        continue

                    gp = get_strategic_group(unidade)

                    # 1. Agregação Diária
                    daily_tree[dt.year][dt.month][dt.day][gp] += 1

                    # 2. Agregação de Detalhes (Mensal por Grupo)
                    node = details_tree[dt.year][dt.month][gp]
                    node["units"][unidade] += 1
                    node["profiles"][perfil] += 1

                    annual_totals[dt.year] += 1
                except:
                    continue

        # Formatar bi_data_v4.json (Diário)
        final_daily = []
        for y, meses in daily_tree.items():
            for m, dias in meses.items():
                for d, grupos in dias.items():
                    for gp, total in grupos.items():
                        final_daily.append(
                            {"y": y, "m": m, "d": d, "g": gp, "t": total}
                        )

        # Salvar Arquivos
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(os.path.join(OUTPUT_DIR, "bi_data_v4.json"), "w") as f:
            json.dump(final_daily, f)

        with open(os.path.join(OUTPUT_DIR, "bi_details_v4.json"), "w") as f:
            json.dump(details_tree, f)

        # GERAR MAPEAMENTO V4 CORRETAMENTE
        unit_map = defaultdict(set)
        for y, meses in details_tree.items():
            for m, grupos in meses.items():
                for gp, val in grupos.items():
                    for unit in val["units"].keys():
                        unit_map[gp].add(unit)

        with open(os.path.join(OUTPUT_DIR, "unit_mapping_v4.json"), "w") as f:
            json.dump({gp: sorted(list(u)) for gp, u in unit_map.items()}, f)

        print(f"Sucesso! Gerados v4: bi_data, bi_details e unit_mapping.")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    process_data()
