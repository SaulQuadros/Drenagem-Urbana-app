#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# Título do App
st.title('Calculadora de Parâmetros de Bacia Hidrográfica')

# Entrada dos dados da bacia hidrográfica
st.sidebar.header('Insira os dados da bacia')

# Inputs com padronização das unidades
area_km2 = st.sidebar.number_input('Área da Bacia (km²)', min_value=10.0, format="%.2f")
perimetro_km = st.sidebar.number_input('Perímetro da Bacia (km)', min_value=20.0, format="%.2f")
comprimento_curso_principal_km = st.sidebar.number_input('Comprimento do Curso Principal (km)', min_value=2.0, format="%.2f")
comprimento_retalinea_km = st.sidebar.number_input('Comprimento em Linha Reta (km)', min_value=1.5, format="%.2f")
comprimento_total_cursos_agua_km = st.sidebar.number_input("Comprimento Total dos Cursos d'Água (km)", min_value=4.0, format="%.2f")
desnivel_m = st.sidebar.number_input('Desnível da Bacia (m)', min_value=10.0, format="%.2f")

# Cálculos dos parâmetros
kf = area_km2 / (comprimento_curso_principal_km ** 2)
kc = 0.28 * perimetro_km / (area_km2 ** 0.5)
dd = comprimento_total_cursos_agua_km / area_km2
lm = area_km2 / (4 * comprimento_total_cursos_agua_km)
sc = comprimento_curso_principal_km / comprimento_retalinea_km
dc = (desnivel_m / (comprimento_curso_principal_km * 1000)) * 100

# Definição dos resultados para iteração
resultados = [
    (
        "Coeficiente de Forma (Kf)",
        kf,
        "quanto mais próximo de 1, mais arredondada é a bacia, indicando picos de vazões mais elevados e maior tendência para enchentes rápidas, sendo o oposto para valores que se aproximam de 0."
    ),
    (
        "Coeficiente de Compacidade (Kc)",
        kc,
        "quanto mais próximo de 1, mais circular é o formato da bacia e favorece o escoamento com altos picos de vazão, sendo a bacia mais sujeita a inundações rápidas, sendo o oposto para valores que se afastam de 1."
    ),
    (
        "Densidade de Drenagem (Dd)",
        dd,
        "valores maiores que 1 indicam maior rapidez no escoamento superficial e menor infiltração, com maior risco de enchentes, e o inverso para valores menores que 1."
    ),
    (
        "Extensão Média do Escoamento (lm)",
        lm,
        "valores entre 100m e 250m indicam uma bacia com drenagem moderada, com equilíbrio entre infiltração e escoamento superficial, contudo, abaixo de 100 m, o escoamento superficial tende a ser rápido com pico de vazões elevados, e acima de 250 m o inverso."
    ),
    (
        "Índice de Sinuosidade (Sc)",
        sc,
        "valores próximos de 1 indicam canais mais retos e maior eficiência de drenagem, portanto, quanto maior o valor maior a sinuosidade e com isso, maior risco de enchentes."
    ),
    (
        "Declividade do Curso D'água Principal (Dc)",
        dc,
        "valores abaixo de 1% indicam maior risco de enchentes, pois a drenagem é demorada, sendo rios de planícies, e acima de 5% indicam rios com corredeiras e elevada velocidade de escoamento."
    )
]

# Exibição dos resultados
st.header('Resultados dos Parâmetros da Bacia')
st.markdown(f'''
- **Coeficiente de Forma (Kf)**: {kf:.3f}  
  **Interpretação**: quanto mais próximo de 1, mais arredondada é a bacia, indicando picos de vazões mais elevados e maior 
  tendência para enchentes rápidas, sendo o oposto para valores que se aproximam de 0.

- **Coeficiente de Compacidade (Kc)**: {kc:.3f}  
  **Interpretação**: quanto mais próximo de 1, mais circular é o formato da bacia e favorece o escoamento com altos picos de vazão, 
  sendo a bacia mais sujeita a inundações rápidas, sendo o oposto para valores que se afastam de 1

- **Densidade de Drenagem (Dd)**: {dd:.3f} km/km²  
  **Interpretação**: valores maiores que 1 indicam maior rapidez no escoamento superficial e menor infiltração, com maior risco de 
  enchentes, e o inverso para valores menores que 1.

- **Extensão Média do Escoamento (lm)**: {lm:.3f} km
  **Interpretação**: valores entre 100m e 250m indicam uma bacia com drenagem moderada, com equilíbrio entre infiltração e escoamento 
  superficial, contudo, abaixo de 100 m, o escoamento superficial tende a ser rápido com pico de vazões elevados, e acima de 250 m 
  o inverso.

- **Índice de Sinuosidade (Sc)**: {sc:.3f}  
  **Interpretação**: valores próximos de 1 indicam canais mais retos e maior eficiência de drenagem, portanto, quanto maior o valor 
  maior a sinuosidade e com isso, maior risco de enchentes.

- **Declividade do Curso D'água Principal (Dc)**: {dc:.3f}%  
  **Interpretação**: valores abaixo de 1% indicam maior risco de enchentes, pois a drenagem é demorada, sendo rios de planícies, 
  e acima de 5% indicam rios com corredeiras e elevada velocidade de escoamento. 
  .
''')

for nome, valor, interpretacao in resultados:
    st.markdown(f"- **{nome}**: {valor:.3f}  \n  **Interpretação**: {interpretacao}")

# Gerar documento Word formatado
if st.button('📄 Gerar Relatório em Word'):
    doc = Document()

    # Configuração das margens
    sec = doc.sections[0]
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.5)

    # Título do relatório
    titulo = doc.add_heading('Relatório de Parâmetros da Bacia Hidrográfica', 0)
    titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    titulo.runs[0].font.size = Pt(16)
    titulo.runs[0].bold = True
    titulo.runs[0].font.name = 'Aptos'

    # Adicionando os resultados
    for nome, valor, interpretacao in resultados:
        p = doc.add_paragraph()
        run = p.add_run(f"{nome}: {valor:.3f}\nInterpretação: {interpretacao}")
        run.font.size = Pt(11)
        run.font.name = 'Aptos'
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_after = Pt(8)

    doc.save("relatorio_bacia.docx")

    with open("relatorio_bacia.docx", "rb") as f:
        st.download_button("⬇️ Baixar relatório", f, file_name="relatorio_bacia.docx")

