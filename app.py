#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# Título do App
st.title('Calculadora de Parâmetros de Bacia Hidrográfica')

# Entrada dos dados da bacia hidrográfica
st.sidebar.header('Insira os dados da bacia')

# Inputs com padronização das unidades
area_km2 = st.sidebar.number_input('Área da Bacia (km²)', min_value=0.01, format="%.2f")
perimetro_km = st.sidebar.number_input('Perímetro da Bacia (km)', min_value=0.01, format="%.2f")
comprimento_curso_principal_km = st.sidebar.number_input('Comprimento do Curso Principal (km)', min_value=0.01, format="%.2f")
comprimento_retalinea_km = st.sidebar.number_input('Comprimento em Linha Reta (km)', min_value=0.01, format="%.2f")
comprimento_total_cursos_agua_km = st.sidebar.number_input('Comprimento Total dos Cursos d\'Água (km)', min_value=0.01, format="%.2f")
desnivel_m = st.sidebar.number_input('Desnível da Bacia (m)', min_value=0.01, format="%.2f")

# Cálculos dos parâmetros
kf = area_km2 / (comprimento_curso_principal_km ** 2)
kc = 0.28 * perimetro_km / (area_km2 ** 0.5)
dd = comprimento_total_cursos_agua_km / area_km2
lm = area_km2 / (4 * comprimento_total_cursos_agua_km)  # Correção aqui
sc = comprimento_curso_principal_km / comprimento_retalinea_km
dc = (desnivel_m / (comprimento_curso_principal_km * 1000)) * 100

# Exibição dos resultados
st.header('Resultados dos Parâmetros da Bacia')
st.markdown(f'''
- **Coeficiente de Forma (Kf)**: {kf:.3f}  
  Interpretação: quanto mais próximo de 1, mais arredondada é a bacia, indicando picos de vazões mais elevados e maior 
  tendência para enchentes rápidas, sendo o oposto para valores que se aproximam de 0.

- **Coeficiente de Compacidade (Kc)**: {kc:.3f}  
  Interpretação: quanto mais próximo de 1, mais circular é o formato da bacia e favorece o escoamento com altos picos de vazão, 
  sendo a bacia mais sujeita a inundações rápidas, sendo o oposto para valores que se afastam de 1

- **Densidade de Drenagem (Dd)**: {dd:.3f} km/km²  
  Interpretação: valores maiores que 1 indicam maior rapidez no escoamento superficial e menor infiltração, com maior risco de 
  enchentes, e o inverso para valores menores que 1.

- **Extensão Média do Escoamento (lm)**: {lm:.3f} km
  Interpretação: valores entre 100m e 250m indicam uma bacia com drenagem moderada, com equilíbrio entre infiltração e escoamento 
  superficial, contudo, abaixo de 100 m, o escoamento superficial tende a ser rápido com pico de vazões elevados, e acima de 250 m 
  o inverso.

- **Índice de Sinuosidade (Sc)**: {sc:.3f}  
  Interpretação: valores próximos de 1 indicam canais mais retos e maior eficiência de drenagem, portanto, quanto maior o valor 
  maior a sinuosidade e com isso, maior risco de enchentes.

- **Declividade do Curso D'água Principal (Dc)**: {dc:.3f}%  
  Interpretação: valores abaixo de 1% indicam maior risco de enchentes, pois a drenagem e demorada, sendo rios de planícies, 
  e acima de 5% indicam rios com corredeiras e elevada velocidade de escoamento. 
  .
''')

