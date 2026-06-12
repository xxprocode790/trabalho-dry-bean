# -*- coding: utf-8 -*-
"""Gera o relatorio final em PDF a partir dos logs dos experimentos."""
import json
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, PageBreak)

BASE = "."
S = getSampleStyleSheet()
estilo_titulo = ParagraphStyle("T", parent=S["Title"], fontSize=16, spaceAfter=4)
estilo_sub = ParagraphStyle("Sub", parent=S["Heading1"], fontSize=13, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor("#1a4d6e"))
estilo_sub2 = ParagraphStyle("Sub2", parent=S["Heading2"], fontSize=11, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#2a6f97"))
estilo_n = ParagraphStyle("N", parent=S["Normal"], fontSize=10, leading=14, alignment=4)  # justificado
estilo_peq = ParagraphStyle("P", parent=S["Normal"], fontSize=8, leading=10)
estilo_centro = ParagraphStyle("C", parent=S["Normal"], fontSize=10, alignment=1)
estilo_leg = ParagraphStyle("L", parent=S["Normal"], fontSize=8.5, alignment=1, textColor=colors.HexColor("#555555"), spaceBefore=2, spaceAfter=10)

def tabela(dados, largs, fonte=8.5, header_bg="#1a4d6e"):
    t = Table(dados, colWidths=largs, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), fonte),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef3f7")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

# ---------- dados dos experimentos ----------
res = pd.read_csv(f"{BASE}/logs/resultados_validacao_cruzada.csv")
rel = json.load(open(f"{BASE}/logs/relatorios_por_classe.json", encoding="utf-8"))
carac = pd.read_csv(f"{BASE}/logs/caracterizacao_atributos.csv")

doc = SimpleDocTemplate(f"{BASE}/Relatorio_Dry_Bean.pdf", pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm,
                        title="Classificacao supervisionada - Dry Bean Dataset")
st = []

# ---------- Cabecalho ----------
st.append(Paragraph("Classificação Supervisionada de Variedades de Feijão<br/>— Dry Bean Dataset (UCI) —", estilo_titulo))
st.append(Spacer(1, 6))
st.append(Paragraph("<b>Integrantes:</b> Luciano [SOBRENOME] e [INTEGRANTE 2 — remover se individual]", estilo_centro))
st.append(Paragraph("<b>Disciplina:</b> Aprendizado de Máquina", estilo_centro))
st.append(Paragraph("<b>Data:</b> 11 de junho de 2026", estilo_centro))
st.append(Paragraph("<b>Repositório GitHub:</b> https://github.com/[SEU-USUARIO]/trabalho-dry-bean", estilo_centro))
st.append(Spacer(1, 10))

# ---------- 1. Apresentacao ----------
st.append(Paragraph("1. Apresentação do dataset", estilo_sub))
st.append(Paragraph(
    'O <b>Dry Bean Dataset</b> está disponível no repositório UCI Machine Learning Repository em '
    '<u>https://archive.ics.uci.edu/dataset/602/dry+bean+dataset</u>. O dataset foi construído por Koklu e Ozkan (2020) '
    'a partir de imagens de alta resolução de 13.611 grãos de feijão seco de sete variedades registradas na Turquia. '
    'Por meio de técnicas de visão computacional, cada grão foi segmentado e dele foram extraídos 16 atributos numéricos: '
    '12 dimensões (área, perímetro, comprimentos dos eixos, excentricidade, etc.) e 4 fatores de forma.', estilo_n))
st.append(Spacer(1, 4))
st.append(Paragraph(
    'O propósito do dataset é a <b>classificação automática da variedade do feijão</b> a partir das características '
    'geométricas do grão, tarefa relevante para a certificação de sementes e o controle de qualidade na indústria '
    'agrícola, substituindo a inspeção visual manual. O <b>atributo classe / target é o atributo nominal '
    '<i>Class</i></b>, que assume sete valores: BARBUNYA, BOMBAY, CALI, DERMASON, HOROZ, SEKER e SIRA. '
    'Todos os demais atributos (numéricos) são utilizados como preditores.', estilo_n))

# ---------- 2. Caracterizacao ----------
st.append(Paragraph("2. Caracterização dos dados", estilo_sub))
st.append(Paragraph(
    'O arquivo original (Dry_Bean_Dataset.xlsx) utilizado neste trabalho possui <b>13.611 instâncias</b> e '
    '<b>18 atributos</b>: um identificador sequencial (<i>Bean ID</i>, presente no espelho do arquivo utilizado), '
    '16 atributos preditores numéricos e o atributo classe (<i>Class</i>, nominal). '
    '<b>Nenhum atributo possui valores faltantes</b> (0 ausências em todas as colunas) e não há instâncias duplicadas. '
    'A Tabela 1 resume o tipo e o intervalo de valores de cada atributo.', estilo_n))
st.append(Spacer(1, 8))

dados_t1 = [["Atributo", "Tipo", "Intervalo / Conjunto de valores", "Faltantes"]]
for _, r in carac.iterrows():
    interv = r["Intervalo / Valores"]
    if len(interv) > 70: interv = interv[:67] + "..."
    dados_t1.append([r["Atributo"], r["Tipo"].replace(" (categórico)","").replace("Numérico ","Num. "),
                     Paragraph(interv, estilo_peq), str(r["Faltantes"])])
st.append(tabela(dados_t1, [4.2*cm, 3.2*cm, 7.6*cm, 1.8*cm], fonte=8))
st.append(Paragraph("Tabela 1 — Caracterização dos 18 atributos do dataset.", estilo_leg))

st.append(Paragraph(
    'Como os 16 preditores são todos numéricos e contínuos, o conceito de desbalanceamento aplica-se ao único '
    'atributo nominal do dataset: a própria classe. O <b>atributo mais desbalanceado é <i>Class</i></b> — a variedade '
    'majoritária DERMASON possui 3.546 instâncias (26,05%), enquanto a minoritária BOMBAY possui apenas 522 (3,84%), '
    'uma razão de desbalanceamento de <b>6,79:1</b>, como mostra a Figura 1.', estilo_n))
st.append(Spacer(1, 6))
st.append(Image(f"{BASE}/figuras/distribuicao_classe.png", width=14*cm, height=7.9*cm))
st.append(Paragraph("Figura 1 — Distribuição das 7 classes (desbalanceamento de 6,79:1).", estilo_leg))
st.append(Image(f"{BASE}/figuras/boxplot_area_por_classe.png", width=13*cm, height=7.3*cm))
st.append(Paragraph("Figura 2 — Atributo Area por classe: BOMBAY é claramente separável; as demais variedades se sobrepõem.", estilo_leg))

# ---------- 3. Pre-processamento ----------
st.append(Paragraph("3. Procedimentos de pré-processamento", estilo_sub))
st.append(Paragraph(
    'O atributo classe já é nominal, portanto não foi necessária a discretização do target exigida por alguns '
    'algoritmos. Foram aplicadas duas variações de pré-processamento, ambas geradas pelo script '
    '<i>02_experimentos.py</i> e publicadas no repositório:', estilo_n))
st.append(Spacer(1, 4))
st.append(Paragraph(
    '<b>P1 — Limpeza mínima (dados/dry_bean_preproc1.csv):</b> remoção do atributo <i>Bean ID</i>, que é um '
    'identificador sequencial sem valor preditivo (mantê-lo induziria os modelos a memorizar a ordem dos registros, '
    'pois o arquivo é ordenado por classe). Os 16 atributos numéricos foram mantidos em suas escalas originais.', estilo_n))
st.append(Spacer(1, 4))
st.append(Paragraph(
    '<b>P2 — P1 + padronização (dados/dry_bean_preproc2.csv):</b> aplicação de <i>StandardScaler</i> '
    '(média 0 e desvio-padrão 1 em cada atributo). A motivação é a grande diferença de escala entre atributos — '
    '<i>Area</i> varia de 20.420 a 254.616 pixels, enquanto <i>ShapeFactor2</i> varia de 0,0006 a 0,0037. Algoritmos '
    'baseados em distância, como o KNN, são fortemente afetados por essa disparidade, pois os atributos de maior '
    'magnitude dominam o cálculo da distância euclidiana.', estilo_n))

# ---------- 4. Resultados ----------
st.append(Paragraph("4. Resultados experimentais", estilo_sub))
st.append(Paragraph(
    'Os três algoritmos — Árvore de Decisão (CART), Random Forest (100 árvores) e KNN (k=5), implementações da '
    'biblioteca scikit-learn 1.7 — foram avaliados por <b>validação cruzada estratificada de 10 folds</b> (seed=42). '
    'As tabelas apresentam a média das métricas nos 10 folds; precisão, recall e F-Measure usam média macro '
    '(média simples entre as 7 classes, adequada a dados desbalanceados). O tempo refere-se ao treino médio por fold '
    '(12.250 instâncias).', estilo_n))

for prep, rotulo in [("P1 - sem normalizacao", "Tabela 2 — Resultados com pré-processamento P1 (sem normalização)."),
                     ("P2 - com padronizacao", "Tabela 3 — Resultados com pré-processamento P2 (com padronização).")]:
    sub = res[res["Pre-processamento"] == prep]
    dados = [["Algoritmo", "Acurácia", "Precisão", "Recall", "F-Measure", "Tempo de treino (s)"]]
    for _, r in sub.iterrows():
        nome = r["Algoritmo"].replace("Arvore de Decisao", "Árvore de Decisão")
        dados.append([nome, f"{100*r['Acuracia']:.2f}%", f"{r['Precisao']:.3f}",
                      f"{r['Recall']:.3f}", f"{r['F-Measure']:.3f}", f"{r['Tempo de treino (s)']:.4f}"])
    st.append(Spacer(1, 8))
    st.append(tabela(dados, [4.3*cm, 2.3*cm, 2.2*cm, 2.2*cm, 2.4*cm, 3.2*cm], fonte=9))
    st.append(Paragraph(rotulo, estilo_leg))

st.append(Paragraph(
    'A comparação entre as tabelas evidencia o papel do pré-processamento: a padronização (P2) não altera os '
    'resultados das árvores (Árvore de Decisão e Random Forest são invariantes a transformações monotônicas de '
    'escala), mas eleva a acurácia do KNN de <b>73,43% para 92,33%</b> (+18,9 pontos percentuais), confirmando a '
    'sensibilidade de algoritmos baseados em distância à escala dos atributos. Em tempo de treino, o KNN é o mais '
    'rápido (~0,005 s, treino "preguiçoso" que apenas armazena os dados), seguido da Árvore de Decisão (~0,20 s); '
    'o Random Forest é o mais custoso (~3,3 s, 100 árvores), cerca de 650× mais lento que o KNN.', estilo_n))

# ---------- 5. Melhor e pior ----------
st.append(Paragraph("5. Análise do melhor e do pior resultado", estilo_sub))
melhor = res.loc[res["F-Measure"].idxmax()]
st.append(Paragraph(
    f'<b>Melhor algoritmo — Random Forest (P2):</b> acurácia média de <b>{100*melhor["Acuracia"]:.2f}%</b>, '
    f'precisão de <b>{melhor["Precisao"]:.3f}</b>, recall de <b>{melhor["Recall"]:.3f}</b> e F-Measure de '
    f'<b>{melhor["F-Measure"]:.3f}</b>, com tempo médio de treino de {melhor["Tempo de treino (s)"]:.2f} s. '
    'O ensemble de 100 árvores reduz a variância da árvore individual e lida bem com a sobreposição entre classes. '
    'O KNN padronizado (92,33%) fica praticamente empatado, com fração do custo de treino.', estilo_n))
st.append(Spacer(1, 4))
st.append(Paragraph(
    '<b>Pior resultado — KNN sem normalização (P1):</b> acurácia de 73,43% e F-Measure de 0,734, consequência direta '
    'da escala desigual dos atributos. Considerando apenas o cenário com padronização (P2), o pior algoritmo é a '
    '<b>Árvore de Decisão</b> (acurácia de 89,58%, F-Measure de 0,910), que, por ser um modelo único, apresenta maior '
    'variância que o ensemble.', estilo_n))
st.append(Spacer(1, 6))
st.append(Paragraph(
    'A análise por valor do atributo classe (holdout estratificado 75/25, P2) é apresentada na Tabela 4. Em <b>todos '
    'os algoritmos, a classe BOMBAY obteve o melhor resultado, com precisão, recall e F1 perfeitos (1,000)</b> — seus '
    'grãos são muito maiores que os demais (Figura 2), tornando-a linearmente separável. O <b>pior desempenho ocorre '
    'sistematicamente na classe SIRA</b> (F1 de 0,860 no Random Forest e 0,813 na Árvore de Decisão), confundida '
    'principalmente com DERMASON — variedades de geometria semelhante —, como mostra a matriz de confusão (Figura 3). '
    'BARBUNYA e DERMASON também ficam abaixo da média do modelo.', estilo_n))
st.append(Spacer(1, 8))

dados_t4 = [["Classe", "Prec. (RF)", "Recall (RF)", "F1 (RF)", "Prec. (AD)", "Recall (AD)", "F1 (AD)", "n teste"]]
rf = rel["Random Forest"]; ad = rel["Arvore de Decisao"]
for cls in ["BARBUNYA", "BOMBAY", "CALI", "DERMASON", "HOROZ", "SEKER", "SIRA"]:
    dados_t4.append([cls, f"{rf[cls]['precision']:.3f}", f"{rf[cls]['recall']:.3f}", f"{rf[cls]['f1-score']:.3f}",
                     f"{ad[cls]['precision']:.3f}", f"{ad[cls]['recall']:.3f}", f"{ad[cls]['f1-score']:.3f}",
                     str(int(rf[cls]["support"]))])
st.append(tabela(dados_t4, [2.6*cm, 1.9*cm, 2.0*cm, 1.7*cm, 1.9*cm, 2.0*cm, 1.7*cm, 1.6*cm], fonte=8.5))
st.append(Paragraph("Tabela 4 — Desempenho por classe: melhor algoritmo (RF — Random Forest) e pior em P2 (AD — Árvore de Decisão).", estilo_leg))
st.append(Image(f"{BASE}/figuras/matriz_confusao_random.png", width=12.5*cm, height=10.7*cm))
st.append(Paragraph("Figura 3 — Matriz de confusão do Random Forest (conjunto de teste, P2): a principal confusão é SIRA × DERMASON.", estilo_leg))

# ---------- 6. Conclusoes ----------
st.append(Paragraph("6. Conclusões", estilo_sub))
st.append(Paragraph(
    'O artigo de origem do dataset (Koklu &amp; Ozkan, 2020), também com validação cruzada de 10 folds, reporta '
    'acurácias de 93,13% (SVM), 92,52% (Árvore de Decisão), 91,73% (MLP) e 87,92% (kNN). O nosso melhor resultado — '
    '<b>Random Forest com 92,60%</b> — é, portanto, compatível com a faixa reportada no repositório de origem, ficando '
    'apenas 0,5 ponto percentual abaixo do melhor modelo dos autores (SVM, não incluído em nosso comparativo) sem '
    'qualquer ajuste de hiperparâmetros. Nosso KNN com padronização (92,33%) supera o kNN reportado pelos autores '
    '(87,92%), o que reforça a importância do pré-processamento P2.', estilo_n))
st.append(Spacer(1, 4))
st.append(Paragraph(
    'A análise por classe também converge com o estudo original: lá, o SVM acertou 100% de BOMBAY e teve em SIRA seu '
    'pior desempenho (86,84%); aqui, BOMBAY foi perfeita (F1 = 1,000) e SIRA foi a classe mais difícil '
    '(F1 = 0,860 no RF). Conclui-se que (i) o desbalanceamento do dataset não impediu bom desempenho macro, '
    '(ii) a escolha do pré-processamento é decisiva para algoritmos baseados em distância e (iii) a dificuldade do '
    'problema concentra-se na fronteira SIRA × DERMASON, candidata natural a trabalhos futuros (e.g., ajuste de '
    'hiperparâmetros ou atributos adicionais de textura).', estilo_n))

# ---------- 7. Arquivos ----------
st.append(Paragraph("7. Arquivos publicados no GitHub", estilo_sub))
st.append(Paragraph(
    'O repositório <u>https://github.com/[SEU-USUARIO]/trabalho-dry-bean</u> contém: <b>dados/</b> (arquivo original '
    'xlsx/csv e os dois pré-processados), <b>scripts/</b> (01_exploracao.py, 02_experimentos.py e 03_relatorio.py), '
    '<b>modelos/</b> (três modelos finais e o scaler, formato joblib), <b>figuras/</b> (gráficos gerados) e '
    '<b>logs/</b> (logs de execução, tabela de caracterização, resultados da validação cruzada e relatórios por '
    'classe), além deste relatório em PDF.', estilo_n))

st.append(Paragraph("Referências", estilo_sub2))
st.append(Paragraph(
    'KOKLU, M.; OZKAN, I. A. Multiclass classification of dry beans using computer vision and machine learning '
    'techniques. <i>Computers and Electronics in Agriculture</i>, v. 174, 105507, 2020.<br/>'
    'DRY BEAN DATASET. UCI Machine Learning Repository, 2020. Disponível em: '
    'https://archive.ics.uci.edu/dataset/602/dry+bean+dataset.<br/>'
    'PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. <i>JMLR</i>, v. 12, p. 2825-2830, 2011.', estilo_peq))

doc.build(st)
print("PDF gerado: Relatorio_Dry_Bean.pdf")
