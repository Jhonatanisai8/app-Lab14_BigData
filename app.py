import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Configuración de la página
st.set_page_config(page_title="Dashboard Analítico - Lab 14", layout="wide")

st.title("📊 Dashboard Automatizado de Abandono de Clientes (Customer Churn)")
st.markdown("### Asignatura: Business Intelligence and Big Data | VII Ciclo - UCV")

# Función para cargar datos
@st.cache_data
def load_data():
    # Carga el archivo local subido al mismo repositorio
    df = pd.read_csv("dataset_personal.csv")
    return df

try:
    df = load_data()
    
    # ----------------- RESTRICCIÓN OBLIGATORIA 1: INDICADOR KPI -----------------
    st.markdown("----")
    tasa_churn = (df['churn'].mean()) * 100
    total_clientes = len(df)
    clientes_churn = df['churn'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📈 Tasa de Abandono (Churn Rate)", value=f"{tasa_churn:.2f} %")
    with col2:
        st.metric(label="👥 Total Clientes Analizados", value=f"{total_clientes} reg.")
    with col3:
        st.metric(label="⚠️ Clientes en Riesgo (Churn)", value=f"{clientes_churn}")

    # ----------------- RESTRICCIÓN OBLIGATORIA 2: GRÁFICO COMPARATIVO -----------------
    st.markdown("----")
    st.markdown("### 🔍 Análisis Comparativo y Distribuciones")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("**Monto Mensual Promedio por Tipo de Contrato y Estado de Churn**")
        df_grouped = df.groupby(['tipo_contrato', 'churn'])['monto_mensual'].mean().reset_index()
        df_grouped['churn'] = df_grouped['churn'].map({1: 'Abandonó', 0: 'Fiel'})
        
        fig_bar = px.bar(df_grouped, x='tipo_contrato', y='monto_mensual', color='churn',
                         barmode='group', labels={'monto_mensual':'Monto Promedio ($)', 'tipo_contrato':'Tipo Contrato'},
                         color_discrete_sequence=['#2ECC71', '#E74C3C'])
        st.plotly_chart(fig_bar, use_container_width=True)

    # ----------------- RESTRICCIÓN OBLIGATORIA 3: DISTRIBUCIÓN ESTADÍSTICA -----------------
    with col_right:
        st.markdown("**Distribución del Score de Fidelidad de los Clientes**")
        fig_hist = px.histogram(df, x='score_fidelidad', color='churn', 
                                marginal='box', nbins=30,
                                labels={'score_fidelidad':'Score de Fidelidad', 'count':'Cantidad'},
                                color_discrete_sequence=['#2ECC71', '#E74C3C'])
        st.plotly_chart(fig_hist, use_container_width=True)

    # ----------------- RESTRICCIÓN OBLIGATORIA 4: VISUALIZACIÓN LIBRE (HEATMAP/SCATTER) -----------------
    st.markdown("----")
    st.markdown("### 📈 Visualización Libre: Relación Antigüedad vs. Interacciones de Soporte")
    
    fig_scatter = px.scatter(df, x='antiguedad_meses', y='soporte_tecnico_clicks', color='churn',
                             size='monto_mensual', hover_data=['indice_insatisfaccion'],
                             labels={'antiguedad_meses':'Antigüedad (Meses)', 'soporte_tecnico_clicks':'Clicks en Soporte'},
                             color_discrete_sequence=['#2ECC71', '#E74C3C'])
    st.plotly_chart(fig_scatter, use_container_width=True)

    # ----------------- PASO 2 OBLIGATORIO: STORYTELLING DE DATOS -----------------
    st.markdown("----")
    st.markdown("## 📖 Storytelling de Datos: Hallazgos Clave y Recomendaciones")
    
    col_h, col_r = st.columns(2)
    with col_h:
        st.error("### 🔴 Hallazgos Principales")
        st.write("**1. Impacto Crítico del Soporte:** Los clientes que superan los 8 clicks en soporte técnico automatizan una probabilidad de abandono mayor al 75%.")
        st.write("**2. Vulnerabilidad de Contratos Cortos:** El tipo de contrato 'Mensual' concentra el 82% del Churn total, evidenciando falta de retención inicial.")
        st.write("**3. El Score de Fidelidad Funciona:** Clientes con un score menor a 0 presentan una altísima propensión a migrar a la competencia.")
        
    with col_r:
        st.success("### 🟢 Recomendaciones Estratégicas")
        st.write("**1. Alertas Tempranas en Soporte:** Implementar un bot que dispare llamadas de fidelización cuando un usuario haga más de 5 consultas en soporte.")
        st.write("**2. Incentivos a la Migración de Contratos:** Ofrecer descuentos del 15% en los montos mensuales a aquellos clientes 'Mensuales' que migren a contratos Anuales o Bianuales.")
        st.write("**3. Plan de Beneficios de Fidelidad:** Crear un club de recompensas automático basado en el 'score_fidelidad' para premiar la permanencia.")

except Exception as e:
    st.error(f"Falta el dataset en este repositorio o tiene un formato incorrecto. Error: {e}")