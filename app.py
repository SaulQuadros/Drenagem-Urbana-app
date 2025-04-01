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
desnivel_m = st.sidebar.number_input('Desnível da Bacia (m)', min_value=0.01, format="%.2f")
comprimento_total_cursos_agua_km = st.sidebar.number_input('Comprimento Total dos Cursos d\'Água (km)', min_value=0.01, format="%.2f")

# Cálculos dos parâmetros
kf = area_km2 / (comprimento_curso_principal_km ** 2)
kc = 0.28 * perimetro_km / (area_km2 ** 0.5)
dd = comprimento_total_cursos_agua_km / area_km2
lm = 1 / (2 * dd)
sc = comprimento_curso_principal_km / comprimento_retalinea_km
dc = (desnivel_m / (comprimento_curso_principal_km * 1000)) * 100

# Exibição dos resultados
st.header('Resultados dos Parâmetros da Bacia')
st.markdown(f'''
- **Coeficiente de Forma (Kf)**: {kf:.3f}  
  Interpretação: Quanto mais próximo de 1, mais arredondada é a bacia, indicando maior tendência para enchentes rápidas.

- **Coeficiente de Compacidade (Kc)**: {kc:.3f}  
  Interpretação: Quanto mais próximo de 1, mais circular e menos sujeita a inundações rápidas é a bacia.

- **Densidade de Drenagem (Dd)**: {dd:.3f} km/km²  
  Interpretação: Valores altos indicam maior rapidez no escoamento superficial e menor infiltração.

- **Extensão Média do Escoamento (lm)**: {lm:.3f} km  
  Interpretação: Valores baixos indicam menor caminho da água até os cursos principais, favorecendo escoamentos rápidos.

- **Índice de Sinuosidade (Sc)**: {sc:.3f}  
  Interpretação: Valores próximos de 1 indicam canais mais retos e maior eficiência de drenagem.

- **Declividade do Curso D'água Principal (Dc)**: {dc:.3f}%  
  Interpretação: Valores elevados indicam cursos d'água com maior velocidade de escoamento.
''')