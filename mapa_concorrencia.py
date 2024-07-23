import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


# Função para carregar dados do CSV
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


# Função para criar mapa com folium
def create_map(data):
    # Dicionário para mapear tipos de estabelecimentos a cores
    tipo_to_color = {
        'John Deere': 'green',
        'Case': 'red',
        'Stara': 'orange',
        'Massey Ferguson': 'purple',
        'New Holland': 'yellow',
        # Adicione mais tipos e cores conforme necessário
    }

    mapa = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)  # Centro aproximado do Brasil

    for idx, row in data.iterrows():
        popup_text = f"""
            <b>Município:</b> {row['municipio']}<br>
            <b>Grupo:</b> {row['grupo']}<br>
            <b>Marca:</b> {row['marca']}
            """
        # Definir a cor do marcador com base no tipo de estabelecimento
        color = tipo_to_color.get(row['marca'], 'gray')  # 'gray' como cor padrão se o tipo não estiver no dicionário

        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=popup_text,
            icon=folium.Icon(color=color)
        ).add_to(mapa)

    return mapa


# Caminho do arquivo CSV
csv_file_path = 'concessionarias.csv'

# Carregando dados
st.title("Mapa de Concessionarias")
data = load_data(csv_file_path)

# Criando filtros suspensos em lista
selected_municipio = st.sidebar.selectbox('Selecione o município', ['Todos'] + list(data['municipio'].unique()))
selected_marca = st.sidebar.selectbox('Selecione a Marca', ['Todos'] + list(data['marca'].unique()))
selected_grupo = st.sidebar.selectbox('Selecione o Grupo', ['Todos'] + list(data['grupo'].unique()))

# Aplicando filtros
if selected_municipio != 'Todos':
    data = data[data['municipio'] == selected_municipio]

if selected_marca != 'Todos':
    data = data[data['marca'] == selected_marca]

if selected_grupo != 'Todos':
    data = data[data['grupo'] == selected_grupo]

#st.write(data)

# Criar mapa
mapa = create_map(data)

# Exibir mapa no Streamlit
st_folium(mapa, width=700, height=500)
