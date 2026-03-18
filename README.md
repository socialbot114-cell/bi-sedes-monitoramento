# BI Monitoramento SEDES (Distrito Federal) 📊

Portal de monitoramento estratégico para análise de atendimentos socioassistenciais, força de trabalho e KPIs operacionais.

## 📋 Visão Geral
Este projeto foi desenvolvido para permitir a comparação histórica de atendimentos (Year-over-Year) entre os anos de 2024, 2025 e 2026, com foco na recuperação operacional pós-paralisação de 2023.

## 🚀 Funcionalidades
- **Dashboard Comparativo (YoY):** Gráficos dinâmicos comparando o volume mensal de atendimentos por ano.
- **KPIs em Tempo Real:** Visualização de totais, médias diárias e indicadores de eficiência.
- **Top 10 Unidades:** Ranking das unidades com maior carga de trabalho (Força de Trabalho).
- **Processamento de Big Data:** Script otimizado para lidar com bases de dados superiores a 1.7 milhão de registros.

## 🛠️ Tecnologias Utilizadas
- **Frontend:** HTML5, Tailwind CSS, Chart.js.
- **Backend/Processamento:** Python 3 (Processamento nativo de CSV).
- **Deploy:** GitHub Pages (Compatível com hospedagem estática).

## 📂 Estrutura de Pastas
- `/data`: Arquivos JSON agregados para o dashboard.
- `/scripts`: Script de limpeza e agregação de dados.
- `/public`: Portal web estático.

## ⚙️ Como Atualizar os Dados
1. Coloque o arquivo CSV atualizado na pasta raiz.
2. Execute o script de processamento:
   ```bash
   python3 scripts/process_data.py
   ```
3. O portal será atualizado automaticamente com os novos JSONs.

---
*Desenvolvido pelo Orquestrador Antigravity | 2026*
