# -*- coding: utf-8 -*-
"""
Exploração / caracterização do dataset Dry Bean (UCI).
Gera: tabela de caracterização (CSV), gráficos (PNG) e log.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = "."
df = pd.read_csv(f"{BASE}/dados/dry_bean_original.csv")

log = []
log.append(f"Instancias: {len(df)}")
log.append(f"Atributos (com classe): {df.shape[1]}")
log.append(f"Valores faltantes (total): {df.isnull().sum().sum()}")
log.append(f"Duplicatas: {df.duplicated().sum()}")

# Tabela de caracterização: nome, tipo, intervalo/conjunto de valores, faltantes
linhas = []
for col in df.columns:
    s = df[col]
    if s.dtype == object:
        tipo = "Nominal (categórico)"
        intervalo = "{" + ", ".join(sorted(s.unique())) + "}"
    elif s.dtype == "int64":
        tipo = "Numérico (inteiro)"
        intervalo = f"[{s.min()} – {s.max()}]"
    else:
        tipo = "Numérico (real)"
        intervalo = f"[{s.min():.4f} – {s.max():.4f}]"
    linhas.append({"Atributo": col, "Tipo": tipo, "Intervalo / Valores": intervalo,
                   "Faltantes": int(s.isnull().sum())})
carac = pd.DataFrame(linhas)
carac.to_csv(f"{BASE}/logs/caracterizacao_atributos.csv", index=False)
log.append("\nTabela de caracterização salva em logs/caracterizacao_atributos.csv")

# Distribuição da classe (desbalanceamento)
dist = df["Class"].value_counts().sort_values(ascending=False)
log.append("\nDistribuição do atributo classe (Class):")
for k, v in dist.items():
    log.append(f"  {k}: {v} ({100*v/len(df):.2f}%)")
log.append(f"Razão de desbalanceamento (maior/menor): {dist.max()/dist.min():.2f}")

# Gráfico 1: distribuição da classe
fig, ax = plt.subplots(figsize=(8, 4.5))
cores = plt.cm.viridis([i/len(dist) for i in range(len(dist))])
ax.bar(dist.index, dist.values, color=cores)
for i, v in enumerate(dist.values):
    ax.text(i, v + 40, str(v), ha="center", fontsize=9)
ax.set_title("Distribuição do atributo classe (Class) — Dry Bean Dataset")
ax.set_ylabel("Quantidade de instâncias")
ax.set_xlabel("Classe (variedade de feijão)")
plt.tight_layout()
plt.savefig(f"{BASE}/figuras/distribuicao_classe.png", dpi=150)
plt.close()

# Gráfico 2: histogramas dos atributos numéricos
num = df.drop(columns=["Bean ID", "Class"])
axes = num.hist(figsize=(14, 10), bins=30, color="#3a7ca5", edgecolor="white")
plt.suptitle("Histogramas dos 16 atributos numéricos", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig(f"{BASE}/figuras/histogramas_atributos.png", dpi=130)
plt.close()

# Gráfico 3: boxplot de um atributo discriminativo por classe
fig, ax = plt.subplots(figsize=(8, 4.5))
df.boxplot(column="Area", by="Class", ax=ax)
ax.set_title("Atributo Area por classe")
plt.suptitle("")
ax.set_ylabel("Area (pixels)")
plt.tight_layout()
plt.savefig(f"{BASE}/figuras/boxplot_area_por_classe.png", dpi=150)
plt.close()

with open(f"{BASE}/logs/01_exploracao.log", "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("\n".join(log))
