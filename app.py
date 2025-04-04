#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# Inicializa o estado para as variáveis, se não existirem
if "tc" not in st.session_state:
    st.session_state.tc = None
if "i_max" not in st.session_state:
    st.session_state.i_max = None
if "Q" not in st.session_state:
    st.session_state.Q = None
if "P_n_percent" not in st.session_state:
    st.session_state.P_n_percent = None

# Título no sidebar e menu
st.sidebar.title("Drenagem Urbana")
menu = st.sidebar.radio("Cálculos", 
                          ["Características da Bacia", 
                           "Microdrenagem - Método Racional"])

if menu == "Características da Bacia":
    st.title('Bacia Hidrográfica de Contribuição')
    
    st.sidebar.header('Insira os dados da bacia')
    # Inputs com padronização das unidades (todos como float para evitar tipos mistos)
    area_km2 = st.sidebar.number_input('Área da Bacia (km²)', min_value=0.01, value=4.5, step=0.01, format="%.2f")
    perimetro_km = st.sidebar.number_input('Perímetro da Bacia (km)', min_value=0.1, value=9.6, step=0.1, format="%.2f")
    comprimento_curso_principal_km = st.sidebar.number_input('Comprimento do Curso Principal (km)', min_value=0.1, value=3.2, step=0.1, format="%.2f")
    comprimento_retalinea_km = st.sidebar.number_input('Comprimento em Linha Reta (km)', min_value=0.1, value=2.5, step=0.1, format="%.2f")
    # Ajustado para que min_value e value sejam do mesmo tipo (float)
    comprimento_total_cursos_agua_km = st.sidebar.number_input("Comprimento Total dos Cursos d'Água (km)", min_value=1.0, value=9.0, step=0.1, format="%.2f")
    desnivel_m = st.sidebar.number_input('Desnível da Bacia (m)', min_value=1.0, value=25.0, step=1.0, format="%.2f")
    
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
            "Declividade do Curso d'água Principal (Dc)",
            dc,
            "valores abaixo de 1% indicam maior risco de enchentes, pois a drenagem é demorada, sendo rios de planícies, e acima de 5% indicam rios com corredeiras e elevada velocidade de escoamento."
        )
    ]
    
    st.header('Resultados: Parâmetros da Bacia')
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
      **Interpretação**: valores próximos de 1 indicam canais mais retos e maior eficiência de drenagem, portanto, quanto maior o valor, 
      maior a sinuosidade e com isso, maior risco de enchentes.
    
    - **Declividade do Curso d'água Principal (Dc)**: {dc:.3f}%  
      **Interpretação**: valores abaixo de 1% indicam maior risco de enchentes, pois a drenagem é demorada, sendo rios de planícies, 
      e acima de 5% indicam rios com corredeiras e elevada velocidade de escoamento. 
    ''')
    
    # Inserindo os campos "Dados do Projeto" ao final do submenu "Características da Bacia"
    st.markdown("### Dados do Projeto")
    nome_projeto = st.text_input("Nome do Projeto")
    tecnico_responsavel = st.text_input("Técnico Responsável")
    
    # Botão de geração do relatório Word agora reposicionado para ficar ao final, após os campos de Dados do Projeto
    if st.button('📄 Gerar Relatório Word - Parâmetros Bacia'):
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
    
        # Inserindo os dados do projeto como as primeiras informações da página, itemizados com bullet
        doc.add_heading('Dados do Projeto', level=2)
        p_nome = doc.add_paragraph(style="List Bullet")
        run_label_nome = p_nome.add_run("Nome do Projeto: ")
        run_label_nome.bold = True
        run_label_nome.font.size = Pt(11)
        run_label_nome.font.name = 'Aptos'
        run_value_nome = p_nome.add_run(nome_projeto)
        run_value_nome.bold = True
        run_value_nome.font.size = Pt(11)
        run_value_nome.font.name = 'Aptos'
        p_nome.paragraph_format.space_after = Pt(6)
        
        p_tecnico = doc.add_paragraph(style="List Bullet")
        run_label_tecnico = p_tecnico.add_run("Responsável Técnico: ")
        run_label_tecnico.bold = True
        run_label_tecnico.font.size = Pt(11)
        run_label_tecnico.font.name = 'Aptos'
        run_value_tecnico = p_tecnico.add_run(tecnico_responsavel)
        run_value_tecnico.bold = True
        run_value_tecnico.font.size = Pt(11)
        run_value_tecnico.font.name = 'Aptos'
        p_tecnico.paragraph_format.space_after = Pt(12)
        
        # Adicionando um subtítulo "Resultados e Interpretações" antes dos coeficientes
        doc.add_heading('Índices Morfométricos: Resultados e Interpretações', level=2)
    
        for nome, valor, interpretacao in resultados:
            p_param = doc.add_paragraph(style="List Bullet")
            run_param = p_param.add_run(f"{nome}: ")
            run_param.bold = True
            run_param.font.size = Pt(11)
            run_param.font.name = 'Aptos'
            run_valor = p_param.add_run(f"{valor:.3f}")
            run_valor.font.size = Pt(11)
            run_valor.font.name = 'Aptos'
            p_param.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            p_param.paragraph_format.space_after = Pt(6)
            
            p_interp = doc.add_paragraph(style="List Bullet")
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
    modelo_tc = st.selectbox("Selecione o modelo para o cálculo do tempo de concentração:",
                             ["Kirpich", "Kirpich Modificado", "Van Te Chow", "Giandotti", "Piking", "USACE", "DNOS", "NRCS (SCS)"])
    
    # Inputs para os modelos – L em km e H em m; a conversão para m ocorre apenas no cálculo de S quando necessário.
    if modelo_tc == "Kirpich":
        st.markdown("#### Parâmetros para a fórmula de Kirpich")
        L_km = st.number_input("Comprimento máximo do percurso d'água (km)", min_value=0.1, value=1.0, step=0.1)
        H = st.number_input("Desnível da bacia (m)", min_value=1.0, value=20.0, step=1.0)
        st.session_state.tc = 57 * (((L_km ** 3) / H) ** 0.385)
    elif modelo_tc == "Kirpich Modificado":
        st.markdown("#### Parâmetros para a fórmula de Kirpich Modificado")
        L_km = st.number_input("Comprimento máximo do percurso d'água (km)", min_value=0.1, value=1.0, step=0.1)
        H = st.number_input("Desnível da bacia (m)", min_value=1.0, value=20.0, step=1.0)
        st.session_state.tc = 85.2 * (((L_km ** 3) / H) ** 0.385)
    elif modelo_tc == "Van Te Chow":
        st.markdown("#### Parâmetros para a fórmula de Van Te Chow")
        L_km = st.number_input("Comprimento máximo do percurso d'água (km)", min_value=0.1, value=1.0, step=0.1)
        H = st.number_input("Desnível da bacia (m)", min_value=1.0, value=20.0, step=1.0)
        S = H / (L_km * 1000)
        st.session_state.tc = 5.773 * ((L_km / (S ** 0.5)) ** 0.64)
    elif modelo_tc == "George Ribeiro":
        st.markdown("#### Parâmetros para a fórmula de George Ribeiro")
        L_km = st.number_input("Comprimento máximo do percurso d'água (km)", min_value=0.1, value=1.0, step=0.1)
        H = st.number_input("Desnível da bacia (m)", min_value=1.0, value=20.0, step=1.0)
        S = H / (L_km * 1000)
        pr = st.number_input("Parâmetro (pr) - Porção da bacia coberta por vegetação", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        st.session_state.tc = (16 * L_km) / ((1.05 - 0.2 * pr) * ((100 * S) ** 0.04))
    elif modelo_tc == "Piking":
        st.markdown("#### Parâmetros para a fórmula de Piking")
        L_km = st.number_input("Comprimento máximo do percurso d'água (km)", min_value=0.1, value=1.0, step=0.1)
        H = st.number_input("Desnível da bacia (m)", min_value=1.0, value=20.0, step=1.0)
        S = H / (L_km * 1000)
        st.session_state.tc = 5.3 * (((L_km ** 2) / S) ** (1/3))
    elif modelo_tc == "USACE":
        st.markdown("#### Parâmetros para a fórmula de USACE")
        L_km = st.number_input("Comprimento máximo do percurso d'água (km)", min_value=0.1, value=1.0, step=0.1)
        H = st.number_input("Desnível da bacia (m)", min_value=1.0, value=20.0, step=1.0)
        S = H / (L_km * 1000)
        st.session_state.tc = 7.504 * (L_km ** 0.76) * (S ** (-0.19))
    elif modelo_tc == "DNOS":
        st.markdown("#### Parâmetros para a fórmula de DNOS")
        L_km = st.number_input("Comprimento máximo do percurso d'água (km)", min_value=0.1, value=1.0, step=0.1)
        H = st.number_input("Desnível da bacia (m)", min_value=1.0, value=20.0, step=1.0)
        S = H / (L_km * 1000)
        A = st.session_state.get("area_km2_micro", 1.0)
        terreno_options = [
            "arenoso-argiloso, coberto de vegetação intensa, elevada absorção",
            "comum, coberto de vegetação, absorção apreciável",
            "argiloso, coberto de vegetação, absorção média",
            "argiloso de vegetação média, pouca absorção",
            "com rocha, escassa vegetação, baixa absorção",
            "Rochoso, vegetação rala, reduzida absorção"
        ]
        terreno = st.selectbox("Selecione o tipo de terreno", terreno_options)
        if terreno == terreno_options[0]:
            K = 2.0
        elif terreno == terreno_options[1]:
            K = 3.0
        elif terreno == terreno_options[2]:
            K = 4.0
        elif terreno == terreno_options[3]:
            K = 4.5
        elif terreno == terreno_options[4]:
            K = 5.0
        elif terreno == terreno_options[5]:
            K = 5.5
        st.session_state.tc = (10 / K) * (((100 * A ** 0.3) * (L_km ** 0.2)) / (S ** 0.4))
    elif modelo_tc == "NRCS (SCS)":
        st.markdown("#### Parâmetros para a fórmula de NRCS (SCS)")
        L_km = st.number_input("Comprimento máximo do percurso d'água (km)", min_value=0.1, value=1.0, step=0.1)
        H = st.number_input("Desnível da bacia (m)", min_value=1.0, value=20.0, step=1.0)
        S = H / L_km
        area_tipo = st.selectbox("Tipo de Área", ["Urbana", "Rural"])
        cond_area = st.selectbox("Condição da Área", ["Seco", "Úmido"])
        if area_tipo == "Urbana":
            uso = st.selectbox("Uso do Solo", ["100% pavimentadas", "Urbanas altamente impermeáveis", "Residenciais", "Com parques"])
            if uso == "100% pavimentadas":
                CN = 98 if cond_area=="Seco" else 99
            elif uso == "Urbanas altamente impermeáveis":
                CN = 85 if cond_area=="Seco" else 95
            elif uso == "Residenciais":
                CN = 70 if cond_area=="Seco" else 85
            elif uso == "Com parques":
                CN = 60 if cond_area=="Seco" else 75
        else:
            uso = st.selectbox("Uso do Solo", ["Pastagem", "Solo argiloso", "Florestas densas", "Solo compactado"])
            if uso == "Pastagem":
                CN = 39 if cond_area=="Seco" else 61
            elif uso == "Solo argiloso":
                CN = 66 if cond_area=="Seco" else 85
            elif uso == "Florestas densas":
                CN = 30 if cond_area=="Seco" else 55
            elif uso == "Solo compactado":
                CN = 75 if cond_area=="Seco" else 85
        st.session_state.tc = 3.42 * ((1000 / CN - 9) ** 0.7) * (L_km ** 0.8) * (S ** (-0.5))
    else:
        st.info("Selecione um modelo válido.")
        st.session_state.tc = None
    
    st.markdown("### Dados para o Cálculo da Intensidade Pluviométrica Máxima")
    a = st.number_input("Coeficiente a", value=1000.0, step=10.0)
    b = st.number_input("Coeficiente b", value=10.0, step=0.01)
    m = st.number_input("Expoente m", value=1.0, step=0.01)
    n = st.number_input("Expoente n", value=1.0, step=0.01)
    
    # Novos inputs para a equação de i_max e probabilidade
    T = st.number_input("Tempo de Retorno (anos)", min_value=1, max_value=1000, value=10, step=1)
    n_period = st.number_input("Período de análise (n anos)", min_value=1, max_value=T, value=1, step=1)
    
    st.markdown("### Coeficiente de Escoamento Superficial (C)")
    C = st.number_input("Insira o valor de C", value=0.6, step=0.01)
    
    st.markdown("### Dados da Bacia para o Método Racional")
    area_km2_md = st.number_input("Área da Bacia (km²)", min_value=0.001, value=1.0, step=0.001, key="area_km2_micro")
    area_m2 = area_km2_md * 1e6
    
    # Inserindo os campos "Dados do Projeto" após os dados da bacia
    st.markdown("### Dados do Projeto")
    nome_projeto = st.text_input("Nome do Projeto", key="nome_projeto")
    tecnico_responsavel = st.text_input("Técnico Responsável", key="tecnico_responsavel")
    
    # Botão de cálculo
    if st.button("Calcular"):
        if st.session_state.tc is None:
            st.error("Selecione um modelo de tempo de concentração implementado.")
        else:
            td = st.session_state.tc  # Considera td = tc
            try:
                st.session_state.i_max = (a * (T ** m)) / ((td + b) ** n)
            except Exception as e:
                st.error("Erro no cálculo da intensidade: verifique os valores inseridos.")
                st.session_state.i_max = None
            
            if st.session_state.i_max is not None:
                P = 1 / T
                P_n = 1 - ((1 - P) ** n_period)
                st.session_state.P_n_percent = P_n * 100
                
                i_max_ms = st.session_state.i_max * 2.78e-7
                st.session_state.Q = C * i_max_ms * area_m2
                
                st.markdown("#### Resultados do Projeto")
                st.write(f"Tempo de Concentração (tc = td): **{td:.2f} minutos**")
                st.write(f"Intensidade Pluviométrica Máxima (i_max): **{st.session_state.i_max:.2f} mm/h**")
                st.write(f"Vazão Máxima de Projeto (Q): **{st.session_state.Q:.3f} m³/s**")
                st.write(f"Probabilidade de ocorrência em {n_period} ano(s): **{st.session_state.P_n_percent:.2f}%**")
    
    if st.button("📄 Gerar Relatório Word - Microdrenagem"):
        if (st.session_state.tc is None or
            st.session_state.i_max is None or
            st.session_state.Q is None or
            st.session_state.P_n_percent is None):
            st.error("Realize o cálculo primeiro para gerar o relatório.")
        else:
            doc = Document()
            sec = doc.sections[0]
            sec.top_margin = Cm(2.0)
            sec.bottom_margin = Cm(2.0)
            sec.left_margin = Cm(2.5)
            sec.right_margin = Cm(2.5)
    
            titulo = doc.add_heading('Microdrenagem - Método Racional', 0)
            titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            titulo.runs[0].font.size = Pt(16)
            titulo.runs[0].bold = True
            titulo.runs[0].font.name = 'Aptos'
    
            # Inserindo os dados do projeto como as primeiras informações da página,
            # itemizados com bullet (círculo preto) e com ambos os textos em negrito.
            doc.add_heading('Dados do Projeto', level=2)
            p_dp1 = doc.add_paragraph(style="List Bullet")
            run_dp1_label = p_dp1.add_run("Nome do Projeto: ")
            run_dp1_label.bold = True
            run_dp1_label.font.size = Pt(11)
            run_dp1_label.font.name = 'Aptos'
            run_dp1_value = p_dp1.add_run(nome_projeto)
            run_dp1_value.bold = True
            run_dp1_value.font.size = Pt(11)
            run_dp1_value.font.name = 'Aptos'
            p_dp1.paragraph_format.space_after = Pt(6)
            
            p_dp2 = doc.add_paragraph(style="List Bullet")
            run_dp2_label = p_dp2.add_run("Responsável Técnico: ")
            run_dp2_label.bold = True
            run_dp2_label.font.size = Pt(11)
            run_dp2_label.font.name = 'Aptos'
            run_dp2_value = p_dp2.add_run(tecnico_responsavel)
            run_dp2_value.bold = True
            run_dp2_value.font.size = Pt(11)
            run_dp2_value.font.name = 'Aptos'
            p_dp2.paragraph_format.space_after = Pt(12)
    
            # Seção: Dados do Projeto (demais informações)
            doc.add_heading('Detalhes do Projeto', level=2)
            dados_projeto = [
                f"Modelo de Cálculo do tc: {modelo_tc}",
                f"Comprimento máximo do percurso d'água (km): {L_km}",
                f"Desnível da bacia (m): {H}",
                f"Tempo de Concentração (tc = td): {st.session_state.tc:.2f} minutos",
                f"Coeficiente a: {a}",
                f"Coeficiente b: {b}",
                f"Expoente m: {m}",
                f"Expoente n: {n}",
                f"Tempo de Retorno (T): {T} ano(s)",
                f"Período de análise (n anos): {n_period}",
                f"Coeficiente de Escoamento (C): {C}",
                f"Área da Bacia (km²): {area_km2_md}"
            ]
            for item in dados_projeto:
                doc.add_paragraph(item, style='List Bullet')
    
            doc.add_paragraph()  # Espaço entre seções
    
            # Seção: Resultados
            doc.add_heading('Resultados', level=2)
            resultados_rel = [
                f"Tempo de Concentração (tc = td): {st.session_state.tc:.2f} minutos",
                f"Intensidade Pluviométrica Máxima (i_max): {st.session_state.i_max:.2f} mm/h",
                f"Vazão Máxima de Projeto (Q): {st.session_state.Q:.3f} m³/s",
                f"Probabilidade de ocorrência em {n_period} ano(s): {st.session_state.P_n_percent:.2f}%"
            ]
            for item in resultados_rel:
                doc.add_paragraph(item, style='List Bullet')
    
            doc.save("relatorio_vazao_maxima.docx")
    
            with open("relatorio_vazao_maxima.docx", "rb") as f:
                st.download_button("⬇️ Baixar relatório", f, file_name="relatorio_vazao_maxima.docx")
            
            st.markdown("#### Resultados do Projeto (mantidos na tela)")
            st.write(f"Tempo de Concentração (tc = td): **{st.session_state.tc:.2f} minutos**")
            st.write(f"Intensidade Pluviométrica Máxima (i_max): **{st.session_state.i_max:.2f} mm/h**")
            st.write(f"Vazão Máxima de Projeto (Q): **{st.session_state.Q:.3f} m³/s**")
            st.write(f"Probabilidade de ocorrência em {n_period} ano(s): **{st.session_state.P_n_percent:.2f}%**")

