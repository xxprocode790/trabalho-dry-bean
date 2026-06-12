# -*- coding: utf-8 -*-
"""
Experimentos: Arvore de Decisao, Random Forest e KNN no Dry Bean Dataset.
Validacao cruzada estratificada 10-fold, em duas variacoes de pre-processamento:
  P1: remocao do Bean ID (atributos originais, sem escala)
  P2: P1 + padronizacao (StandardScaler)
Metricas: acuracia, precisao (macro), recall (macro), F1 (macro) e tempo medio de treino.
Tambem treina modelos finais (holdout 75/25) e salva modelos + relatorios por classe.
Uso: python3 02_experimentos.py [cv:<dt|rf|knn>:<P1|P2> | final]   (sem argumento = tudo)
"""
import time, json, sys, os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = "."
SEED = 42

df = pd.read_csv(f"{BASE}/dados/dry_bean_original.csv")

# ---------- Pre-processamento 1: remocao do identificador ----------
df_p1 = df.drop(columns=["Bean ID"])
df_p1.to_csv(f"{BASE}/dados/dry_bean_preproc1.csv", index=False)
X1 = df_p1.drop(columns=["Class"]).values
y = df_p1["Class"].values

# ---------- Pre-processamento 2: P1 + padronizacao ----------
scaler = StandardScaler()
X2 = scaler.fit_transform(X1)
df_p2 = pd.DataFrame(X2, columns=df_p1.columns[:-1])
df_p2["Class"] = y
df_p2.to_csv(f"{BASE}/dados/dry_bean_preproc2.csv", index=False)
joblib.dump(scaler, f"{BASE}/modelos/scaler_padronizacao.joblib")

algoritmos = {
    "Arvore de Decisao": DecisionTreeClassifier(random_state=SEED),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=SEED),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
}
metricas = {"accuracy": "accuracy", "precision": "precision_macro",
            "recall": "recall_macro", "f1": "f1_macro"}
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=SEED)

etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
CSV_RES = f"{BASE}/logs/resultados_validacao_cruzada.csv"
LOG_CV = f"{BASE}/logs/02_experimentos.log"
chaves = {"dt": "Arvore de Decisao", "rf": "Random Forest", "knn": "KNN (k=5)"}
preps = {"P1": ("P1 - sem normalizacao", X1), "P2": ("P2 - com padronizacao", X2)}

def roda_cv(nome_prep, X, nome_alg, modelo):
    cvres = cross_validate(modelo, X, y, cv=cv, scoring=metricas, n_jobs=1)
    r = {
        "Pre-processamento": nome_prep,
        "Algoritmo": nome_alg,
        "Acuracia": cvres["test_accuracy"].mean(),
        "Acuracia_dp": cvres["test_accuracy"].std(),
        "Precisao": cvres["test_precision"].mean(),
        "Recall": cvres["test_recall"].mean(),
        "F-Measure": cvres["test_f1"].mean(),
        "Tempo de treino (s)": cvres["fit_time"].mean(),
    }
    linha = (f"[{nome_prep}] {nome_alg}: acc={r['Acuracia']:.4f}+-{r['Acuracia_dp']:.4f} "
             f"prec={r['Precisao']:.4f} rec={r['Recall']:.4f} f1={r['F-Measure']:.4f} "
             f"tempo_treino={r['Tempo de treino (s)']:.4f}s")
    pd.DataFrame([r]).to_csv(CSV_RES, mode="a", index=False,
                             header=not os.path.exists(CSV_RES))
    with open(LOG_CV, "a", encoding="utf-8") as f:
        f.write(linha + "\n")
    print(linha)

if etapa == "tudo":
    for kp in ["P1", "P2"]:
        for ka in ["dt", "rf", "knn"]:
            roda_cv(*preps[kp], chaves[ka], algoritmos[chaves[ka]])
elif etapa.startswith("cv:"):
    _, ka, kp = etapa.split(":")
    roda_cv(*preps[kp], chaves[ka], algoritmos[chaves[ka]])
    sys.exit(0)

# ---------- Modelos finais (holdout 75/25 estratificado, P2) ----------
log = []
X_tr, X_te, y_tr, y_te = train_test_split(X2, y, test_size=0.25,
                                          stratify=y, random_state=SEED)
relatorios = {}
log.append("Holdout 75/25 estratificado (P2 - com padronizacao):")
for nome_alg, modelo in algoritmos.items():
    t0 = time.perf_counter()
    modelo.fit(X_tr, y_tr)
    t_fit = time.perf_counter() - t0
    y_pred = modelo.predict(X_te)
    rep = classification_report(y_te, y_pred, output_dict=True, zero_division=0)
    relatorios[nome_alg] = rep
    slug = nome_alg.split()[0].lower()
    joblib.dump(modelo, f"{BASE}/modelos/modelo_{slug}.joblib")
    log.append(f"  {nome_alg}: acc_teste={rep['accuracy']:.4f} tempo_treino={t_fit:.4f}s")

    classes = sorted(np.unique(y))
    cm = confusion_matrix(y_te, y_pred, labels=classes)
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(classes)), classes, rotation=45, ha="right")
    ax.set_yticks(range(len(classes)), classes)
    for i in range(len(classes)):
        for j in range(len(classes)):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > cm.max()/2 else "black", fontsize=8)
    ax.set_title(f"Matriz de confusao - {nome_alg} (teste, P2)")
    ax.set_xlabel("Classe predita"); ax.set_ylabel("Classe real")
    plt.colorbar(im, fraction=0.046)
    plt.tight_layout()
    plt.savefig(f"{BASE}/figuras/matriz_confusao_{slug}.png", dpi=150)
    plt.close()

with open(f"{BASE}/logs/relatorios_por_classe.json", "w", encoding="utf-8") as f:
    json.dump(relatorios, f, ensure_ascii=False, indent=2)
with open(LOG_CV, "a", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print("\n".join(log))
print("OK - experimentos concluidos")
