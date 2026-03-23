import csv
import json
import os
from collections import defaultdict
from datetime import datetime

# Configurações
CSV_PATH = "/home/richard/Documentos/monitoramento /novos dados 23 03 2026.csv"
OUTPUT_DIR = "/home/richard/Documentos/monitoramento /bi-sedes-monitoramento/data"


def get_strategic_group(unit_name):
    name = unit_name.upper().strip()

    # GRUPO A: CRAS & CREAS & CENTRO POP
    if any(k in name for k in ["CRAS", "CREAS", "CENTRO POP"]):
        return "CRAS / CREAS / CENTRO POP"

    # GRUPO B: UNIDADE ACOLHIMENTO
    if any(
        k in name
        for k in [
            "ACOLHIMENTO",
            "UAI",
            "SAIAFA",
            "CASA SOCIAL",
            "GERÊNCIA - DE SERVIÇOS DE ACOLHIMENTO",
        ]
    ):
        return "UNIDADE ACOLHIMENTO"

    # GRUPO C: OSC & POSTO
    if any(
        k in name
        for k in [
            "OSC",
            "POSTO",
            "MÃOS SOLIDÁRIAS",
            "MAOS SOLIDARIAS",
            "APAE",
            "PESTALOZZI",
            "ASSOCIAÇÃO",
            "SOCIEDADE",
        ]
    ):
        return "OSC & POSTO"

    # RESTANTE (CECON, COORDENACAO, ETC)
    if "CECON" in name:
        return "CECON / CONVIVÊNCIA"
    return "OUTROS / GESTÃO"


def process_data():
    print("Iniciando processamento com Grupos Estratégicos e Volume Anual...")

    # Estrutura: [ano][mes][dia][grupo][unidade] = total
    data_tree = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        )
    )
    annual_totals = defaultdict(int)
    unit_map = defaultdict(set)

    try:
        with open(CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_str = row["DATA ATENDIMENTO"]
                unidade = row["unidade"]
                if not unidade:
                    continue

                grupo = get_strategic_group(unidade)

                try:
                    dt = datetime.strptime(data_str, "%Y-%m-%d")
                    data_tree[dt.year][dt.month][dt.day][grupo][unidade] += 1
                    annual_totals[dt.year] += 1
                    unit_map[grupo].add(unidade)
                except:
                    continue

        # Formatar para JSON BI (V3)
        final_data = []
        for ano, meses in data_tree.items():
            for mes, dias in meses.items():
                for dia, grupos in dias.items():
                    for gp, unidades in grupos.items():
                        gp_total = sum(unidades.values())
                        final_data.append(
                            {
                                "y": ano,
                                "m": mes,
                                "d": dia,
                                "g": gp,
                                "t": gp_total,
                                "u": [{"n": u, "t": t} for u, t in unidades.items()],
                            }
                        )

        # Mapeamento de unidades por grupo
        unit_mapping_json = {gp: sorted(list(units)) for gp, units in unit_map.items()}

        # Salvar resultados
        with open(os.path.join(OUTPUT_DIR, "bi_data_v3.json"), "w") as f:
            json.dump(final_data, f)

        with open(os.path.join(OUTPUT_DIR, "annual_stats.json"), "w") as f:
            json.dump(annual_totals, f)

        with open(os.path.join(OUTPUT_DIR, "unit_mapping_v3.json"), "w") as f:
            json.dump(unit_mapping_json, f)

        print(f"Sucesso! Volumes Anuais: {json.dumps(annual_totals, indent=2)}")

    except Exception as e:
        print(f"Erro no processamento: {e}")


if __name__ == "__main__":
    process_data()
