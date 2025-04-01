#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# Título no sidebar
st.sidebar.title("Drenagem Urbana")
menu = st.sidebar.radio("Cálculos", 
                          ["Características - Bacia Hidrográfica Contribuição", 
                           "Microdrenagem - Método Racional"])

if menu == "Características - Bacia Hidrográfica Contribuição":
    st.title('Calculadora de Parâmetros de Bacia Hidrográfica')
    
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
    
    st.header('Resultados dos Parâmetros da Bacia')
    st.markdown(f'''
    - **Coeficiente de Forma (Kf)**: {kf:.3f}  
      **Interpretação**: quanto mais próximo de 1, mais arredondada é a bacia, indicando picos de vazões mais elevados e maior 
      tendência para enchentes rápidas, sendo o oposto para valores que se aproximam de 0.
    
    - **Coeficiente de Compacidade (Kc)**: {kc:.3f}  
      **Interpretação**: quanto mais próximo de 1, mais circular é o formato da bacia e favorece o escoamento com altos picos de vazão, 
      sendo a bacia mais sujeita a inundações rápidas, sendo o oposto para valores que se afastam de 1.
    
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
    ''')
    
    # Geração do documento Word (mesma formatação já existente)
    if st.button('📄 Gerar Relatório Word - Drenagem Urbana'):
        doc = Document()
    
        sec = doc.sections[0]
        sec.top_margin = Cm(2.0)
        sec.bottom_margin = Cm(2.0)
        sec.left_margin = Cm(2.5)
        sec.right_margin = Cm(2.5)
    
        titulo = doc.add_heading('Relatório de Parâmetros da Bacia Hidrográfica', 0)
        titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        titulo.runs[0].font.size = Pt(16)
        titulo.runs[0].bold = True
        titulo.runs[0].font.name = 'Aptos'
    
        doc.add_paragraph()
    
        for nome, valor, interpretacao in resultados:
            p_param = doc.add_paragraph()
            run_param = p_param.add_run(f"{nome}: ")
            run_param.bold = True
            run_param.font.size = Pt(11)
            run_param.font.name = 'Aptos'
            run_valor = p_param.add_run(f"{valor:.3f}")
            run_valor.font.size = Pt(11)
            run_valor.font.name = 'Aptos'
            p_param.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            p_param.paragraph_format.space_after = Pt(6)
            
            p_interp = doc.add_paragraph()
            run_interp_label = p_interp.add_run("Interpretação: ")
            run_interp_label.bold = True
            run_interp_label.font.size = Pt(11)
            run_interp_label.font.name = 'Aptos'
            run_interp_text = p_interp.add_run(interpretacao)
            run_interp_text.font.size = Pt(11)
            run_interp_text.font.name = 'Aptos'
            p_interp.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
            p_interp.paragraph_format.space_after = Pt(12)
    
        doc.save("relatorio_bacia.docx")
    
        with open("relatorio_bacia.docx", "rb") as f:
            st.download_button("⬇️ Baixar relatório", f, file_name="relatorio_bacia.docx")

elif menu == "Microdrenagem - Método Racional":
    st.title("Microdrenagem - Método Racional")
    
    st.markdown("### Escolha do Modelo de Tempo de Concentração")
    # Seleção do modelo
    modelo_tc = st.selectbox("Selecione o modelo para o cálculo do tempo de concentração:",
                             ["Kirpich", "Kirpich Modificado", "Van Te Chow", "Giandotti", "Piking", "USACE", "DNOS", "NRCS (SCS)"])
    
    # Inputs para o modelo escolhido – para este exemplo, implementaremos a fórmula de Kirpich
    if modelo_tc == "Kirpich":
        st.markdown("#### Parâmetros para a fórmula de Kirpich")
        L_km = st.number_input("Comprimento máximo do percurso d'água (km)", min_value=0.1, value=5.0, step=0.1)
        H = st.number_input("Desnível da bacia (m)", min_value=1.0, value=20.0, step=1.0)
        # Cálculo do tempo de concentração (tc) em minutos conforme a nova fórmula:
        # t_c = 57 * ((L^3 / H)^0.385)
        tc = 57 * (((L_km ** 3) / H) ** 0.385)
    else:
        st.info("Modelo selecionado ainda não implementado. Utilize o modelo 'Kirpich' para este exemplo.")
        tc = None
    
    st.markdown("### Dados para o Cálculo da Intensidade Pluviométrica Máxima")
    a = st.number_input("Coeficiente a", value=1000.0, step=100.0)
    b = st.number_input("Coeficiente b", value=100.0, step=0.01)
    m = st.number_input("Expoente m", value=1.0, step=0.01)
    n = st.number_input("Expoente n", value=1.0, step=0.01)
    
    # Novos inputs para a equação de i_max e probabilidade
    T = st.number_input("Tempo de Retorno (anos)", min_value=1, max_value=1000, value=1, step=1)
    n_period = st.number_input("Período de análise (n anos)", min_value=1, max_value=T, value=1, step=1)
    
    st.markdown("### Coeficiente de Escoamento Superficial (C)")
    C = st.number_input("Insira o valor de C", value=0.7, step=0.01)
    
    st.markdown("### Dados da Bacia para o Método Racional")
    # Reutiliza a área já definida para a bacia (em km²) – converte para m²
    area_km2_md = st.number_input("Área da Bacia (km²)", min_value=0.001, value=10.0, step=0.001)
    area_m2 = area_km2_md * 1e6
    
    # Botão de cálculo
    if st.button("Calcular"):
        if tc is None:
            st.error("Selecione um modelo de tempo de concentração implementado.")
        else:
            # Considera que o tempo de duração da chuva (td) é igual ao tempo de concentração (tc)
            td = tc  
            # Nova equação da intensidade máxima: i_max = (a * T^m) / ((td + b)^n)
            try:
                i_max = (a * (T ** m)) / ((td + b) ** n)
            except Exception as e:
                st.error("Erro no cálculo da intensidade: verifique os valores inseridos.")
                i_max = None
            
            if i_max is not None:
                # Cálculo da probabilidade de ocorrência do evento crítico em n_period anos:
                # P = 1/T; P_n = 1 - (1 - P)^n_period, expresso em %
                P = 1 / T
                P_n = 1 - ((1 - P) ** n_period)
                P_n_percent = P_n * 100
                
                # Vazão máxima de projeto pelo Método Racional: Q = C * i_max * A
                # Supondo que i_max esteja em mm/h, convertemos para m/s: 1 mm/h = 2.78e-7 m/s.
                i_max_ms = i_max * 2.78e-7
                Q = C * i_max_ms * area_m2  # Vazão em m³/s
                
                st.markdown("#### Resultados do Projeto")
                st.write(f"Tempo de Concentração (tc = td): **{tc:.2f} minutos**")
                st.write(f"Intensidade Pluviométrica Máxima (i_max): **{i_max:.2f} mm/h**")
                st.write(f"Vazão Máxima de Projeto (Q): **{Q:.3f} m³/s**")
                st.write(f"Probabilidade de ocorrência em {n_period} ano(s): **{P_n_percent:.2f}%**")
    
    # Botão para gerar relatório Word da vazão máxima e demais resultados
    if st.button("📄 Gerar Relatório Word - Vazão Máxima"):
        if tc is None or i_max is None:
            st.error("Realize o cálculo primeiro para gerar o relatório.")
        else:
            doc = Document()
    
            sec = doc.sections[0]
            sec.top_margin = Cm(2.0)
            sec.bottom_margin = Cm(2.0)
            sec.left_margin = Cm(2.5)
            sec.right_margin = Cm(2.5)
    
            titulo = doc.add_heading('Relatório - Vazão Máxima de Projeto', 0)
            titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            titulo.runs[0].font.size = Pt(16)
            titulo.runs[0].bold = True
            titulo.runs[0].font.name = 'Aptos'
    
            doc.add_paragraph()
    
            p_tc = doc.add_paragraph()
            run_tc = p_tc.add_run(f"Tempo de Concentração (tc = td): {tc:.2f} minutos")
            run_tc.font.size = Pt(11)
            run_tc.font.name = 'Aptos'
            p_tc.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            p_tc.paragraph_format.space_after = Pt(6)
    
            p_i_max = doc.add_paragraph()
            run_i_max = p_i_max.add_run(f"Intensidade Pluviométrica Máxima (i_max): {i_max:.2f} mm/h")
            run_i_max.font.size = Pt(11)
            run_i_max.font.name = 'Aptos'
            p_i_max.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            p_i_max.paragraph_format.space_after = Pt(6)
    
            p_Q = doc.add_paragraph()
            run_Q = p_Q.add_run(f"Vazão Máxima de Projeto (Q): {Q:.3f} m³/s")
            run_Q.font.size = Pt(11)
            run_Q.font.name = 'Aptos'
            p_Q.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            p_Q.paragraph_format.space_after = Pt(6)
    
            p_prob = doc.add_paragraph()
            run_prob = p_prob.add_run(f"Probabilidade de ocorrência em {n_period} ano(s): {P_n_percent:.2f}%")
            run_prob.font.size = Pt(11)
            run_prob.font.name = 'Aptos'
            p_prob.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            p_prob.paragraph_format.space_after = Pt(12)
    
            doc.save("relatorio_vazao_maxima.docx")
    
            with open("relatorio_vazao_maxima.docx", "rb") as f:
                st.download_button("⬇️ Baixar relatório", f, file_name="relatorio_vazao_maxima.docx")

