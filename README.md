# Classificação Supervisionada — Dry Bean Dataset (UCI)

Trabalho da disciplina **INTELIGÊNCIA ARTIFICIAL E COMPUTACIONAL** — comparativo entre Árvore de Decisão, Random Forest e KNN.

**Dataset:** [Dry Bean Dataset — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/602/dry+bean+dataset)
(13.611 instâncias, 16 atributos numéricos, 7 classes; target: `Class`)

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `dados/` | Arquivo original (`Dry_Bean_Dataset.xlsx` / `dry_bean_original.csv`) e pré-processados (`dry_bean_preproc1.csv`: sem Bean ID; `dry_bean_preproc2.csv`: + padronização) |
| `scripts/` | `01_exploracao.py` (caracterização e gráficos), `02_experimentos.py` (validação cruzada 10-fold e modelos finais), `03_relatorio.py` (gera o PDF) |
| `modelos/` | Modelos finais treinados (`.joblib`) e o `StandardScaler` |
| `figuras/` | Gráficos gerados (distribuição da classe, histogramas, boxplot, matrizes de confusão) |
| `logs/` | Logs de execução, caracterização dos atributos, resultados da validação cruzada e métricas por classe |
| `Relatorio_Dry_Bean.pdf` | Relatório final |

## Reprodução

```bash
pip install pandas scikit-learn matplotlib joblib openpyxl reportlab
python3 scripts/01_exploracao.py
python3 scripts/02_experimentos.py   # aceita etapas: cv:dt:P1 ... | final
python3 scripts/03_relatorio.py
```

## Resultados (validação cruzada estratificada 10-fold, seed 42)

| Algoritmo | Pré-proc. | Acurácia | Precisão | Recall | F-Measure | Tempo de treino (s) |
|---|---|---|---|---|---|---|
| Árvore de Decisão | P1/P2 | 89,58% | 0,911 | 0,910 | 0,910 | 0,20 |
| Random Forest | P2 | **92,60%** | 0,939 | 0,935 | 0,937 | 3,32 |
| KNN (k=5) | P1 | 73,43% | 0,744 | 0,730 | 0,734 | 0,005 |
| KNN (k=5) | P2 | 92,33% | 0,937 | 0,934 | 0,936 | 0,005 |

Melhor algoritmo: **Random Forest (P2)**. Melhor classe: **BOMBAY** (F1 = 1,000); pior classe: **SIRA** (F1 = 0,860), confundida com DERMASON.
