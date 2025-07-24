import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from database import db_manager

# Configuração da página
st.set_page_config(
    page_title="Sistema de Locação de Imóveis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para deixar mais bonito
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79, #2e75b6);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .main-header h1 {
        color: white !important;
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        margin: 0;
        font-size: 2rem;
    }
    .category-header {
        background: #e3f2fd;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #1976d2;
        margin: 1rem 0;
        color: #1565c0;
        font-weight: bold;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1976d2;
    }
    /* Melhorar legibilidade dos títulos das consultas */
    .stSelectbox label, .stRadio label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    /* Títulos das seções */
    .stMarkdown h1 {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    .stMarkdown h2 {
        color: #333333 !important;
        font-weight: bold !important;
    }
    .stMarkdown h3 {
        color: #1976d2 !important;
        font-weight: 600 !important;
    }
    .stMarkdown h4 {
        color: #424242 !important;
        font-weight: 600 !important;
    }
    /* Melhorar contraste do texto */
    .stMarkdown p {
        color: #333333 !important;
    }
    /* Estilizar sidebar */
    .css-1d391kg {
        background-color: #2c3e50 !important;
    }
    /* Textos do sidebar - labels dos selectbox */
    .css-1d391kg .stSelectbox label, 
    .css-1d391kg label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    /* Textos markdown no sidebar */
    .css-1d391kg .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ecf0f1 !important;
    }
    .css-1d391kg .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
        font-weight: bold !important;
    }
    .css-1d391kg .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #bdc3c7 !important;
    }
    /* Forçar cor branca nos labels do sidebar */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stSelectbox > label {
        color: white !important;
    }
    /* Forçar ainda mais - usando todos os seletores possíveis */
    .stSidebar label,
    .stSidebar .stSelectbox label,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    .css-1544g2n label,
    .css-1544g2n .stSelectbox label {
        color: white !important;
        font-weight: 600 !important;
    }
    /* Título da consulta em branco */
    .consulta-titulo {
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 0.5rem;
        background: #1976d2;
        border-radius: 5px;
        margin: 1rem 0;
    }
    /* Melhorar tabelas */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

def executar_consulta(sql):
    """Executa consulta e retorna DataFrame"""
    try:
        conn = db_manager.get_connection()
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro na consulta: {e}")
        return pd.DataFrame()

def criar_grafico_receita_imoveis(df):
    """Cria gráfico de receita por imóvel"""
    if not df.empty and 'receita_total' in df.columns:
        # Limpar formato R$ e converter para número
        df_clean = df.copy()
        df_clean['receita_num'] = df_clean['receita_total'].str.replace('R$ ', '').str.replace(',', '').astype(float)
        
        fig = px.bar(
            df_clean, 
            x='titulo', 
            y='receita_num',
            title="💰 Receita Total por Imóvel",
            labels={'receita_num': 'Receita (R$)', 'titulo': 'Imóvel'},
            color='receita_num',
            color_continuous_scale='viridis'
        )
        fig.update_layout(showlegend=False, height=400)
        return fig
    return None

def criar_grafico_ocupacao(df):
    """Cria gráfico de ocupação temporal"""
    if not df.empty and 'mes_ano' in df.columns:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['mes_ano'], 
            y=df['confirmadas'],
            mode='lines+markers',
            name='Confirmadas',
            line=dict(color='green', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['mes_ano'], 
            y=df['canceladas'],
            mode='lines+markers', 
            name='Canceladas',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="📊 Evolução das Reservas por Período",
            xaxis_title="Período",
            yaxis_title="Quantidade de Reservas",
            height=400,
            hovermode='x unified'
        )
        return fig
    return None

# Definição das consultas organizadas
CONSULTAS = {
    "🏢 CONSULTAS OPERACIONAIS": {
        "Usuários e Perfis": """
            SELECT 
                u.nome,
                u.email,
                CASE 
                    WHEN a.id_usuario IS NOT NULL THEN 'Anfitrião'
                    WHEN h.id_usuario IS NOT NULL THEN 'Hóspede'
                    ELSE 'Sem perfil'
                END as perfil,
                COUNT(DISTINCT tu.telefone) as total_telefones
            FROM usuario u
            LEFT JOIN anfitriao a ON u.id_usuario = a.id_usuario
            LEFT JOIN hospede h ON u.id_usuario = h.id_usuario
            LEFT JOIN telefone_usuario tu ON u.id_usuario = tu.id_usuario
            GROUP BY u.id_usuario, u.nome, u.email, a.id_usuario, h.id_usuario
            ORDER BY u.nome;
        """,
        
        "Imóveis e Características": """
            SELECT 
                i.titulo,
                i.cidade || ', ' || i.estado as localizacao,
                i.capacidade_max as capacidade,
                'R$ ' || i.valor_diaria as diaria,
                pc.tipo_politica as politica,
                COUNT(DISTINCT c.comodidade) as total_comodidades
            FROM imovel i
            JOIN politica_cancelamento pc ON i.id_politica = pc.id_politica
            LEFT JOIN comodidades c ON i.id_imovel = c.id_imovel
            GROUP BY i.id_imovel, i.titulo, i.cidade, i.estado, i.capacidade_max, i.valor_diaria, pc.tipo_politica
            ORDER BY i.valor_diaria DESC;
        """,
        
        "Status das Reservas": """
            SELECT 
                u.nome as hospede,
                i.titulo as imovel,
                r.num_hospedes as hospedes,
                TO_CHAR(r.data_inicio, 'DD/MM/YYYY') as check_in,
                TO_CHAR(r.data_fim, 'DD/MM/YYYY') as check_out,
                r.status,
                CASE 
                    WHEN r.data_inicio > CURRENT_DATE THEN 'Futura'
                    WHEN r.data_fim < CURRENT_DATE THEN 'Finalizada'
                    ELSE 'Em andamento'
                END as situacao
            FROM reserva r
            JOIN usuario u ON r.id_usuario = u.id_usuario
            JOIN imovel i ON r.id_imovel = i.id_imovel
            ORDER BY r.data_inicio DESC;
        """
    },
    
    "💰 ANÁLISES FINANCEIRAS": {
        "Análise de Pagamentos": """
            SELECT 
                p.id_pagamento as pagamento_id,
                'R$ ' || p.valor_total as valor,
                p.forma_pagamento,
                TO_CHAR(p.data_pagamento, 'DD/MM/YYYY') as data_pag,
                COALESCE(COUNT(pa.num_parcelas), 0) as total_parcelas,
                CASE 
                    WHEN COUNT(pa.num_parcelas) = 0 THEN 'À vista'
                    WHEN COUNT(pa.num_parcelas) = 1 THEN 'À vista' 
                    ELSE 'Parcelado'
                END as tipo_pagamento
            FROM pagamento p
            LEFT JOIN parcela pa ON p.id_pagamento = pa.id_pagamento
            GROUP BY p.id_pagamento, p.valor_total, p.forma_pagamento, p.data_pagamento
            ORDER BY p.data_pagamento DESC;
        """,
        
        "Receita por Imóvel": """
            SELECT 
                i.titulo, 
                COUNT(r.id_reserva) as total_reservas,
                'R$ ' || COALESCE(SUM(p.valor_total), 0) AS receita_total
            FROM imovel i
            LEFT JOIN reserva r ON i.id_imovel = r.id_imovel AND r.status = 'confirmada'
            LEFT JOIN gera g ON r.id_reserva = g.id_reserva
            LEFT JOIN pagamento p ON g.id_pagamento = p.id_pagamento
            GROUP BY i.titulo, i.id_imovel
            ORDER BY COALESCE(SUM(p.valor_total), 0) DESC;
        """,
        
        "Fluxo Financeiro Completo": """
            SELECT 
                r.id_reserva, 
                'Principal' as tipo, 
                'R$ ' || p.valor_total as valor,
                p.forma_pagamento, 
                TO_CHAR(p.data_pagamento, 'DD/MM/YYYY') as data_pagamento
            FROM reserva r
            JOIN gera g ON r.id_reserva = g.id_reserva
            JOIN pagamento p ON g.id_pagamento = p.id_pagamento
            UNION ALL
            SELECT 
                r.id_reserva, 
                'Multa' as tipo, 
                'R$ ' || p.valor_total as valor,
                p.forma_pagamento, 
                TO_CHAR(p.data_pagamento, 'DD/MM/YYYY') as data_pagamento
            FROM reserva r
            JOIN reserva_cancelada rc ON EXISTS (
                SELECT 1 FROM gera g2 WHERE g2.id_reserva = r.id_reserva AND g2.id_pagamento = rc.id_pagamento
            )
            JOIN gera_multa gm ON rc.id_cancelamento = gm.id_cancelamento
            JOIN gera_pag_multa gpm ON gm.id_multa = gpm.id_multa
            JOIN pagamento p ON gpm.id_pagamento = p.id_pagamento
            ORDER BY id_reserva, tipo;
        """
    },
    
    "📊 BUSINESS INTELLIGENCE": {
        "Ranking de Anfitriões": """
            SELECT 
                u.nome as anfitriao,
                COUNT(DISTINCT i.id_imovel) as total_imoveis,
                COUNT(r.id_reserva) as total_reservas,
                COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END) as confirmadas,
                COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END) as canceladas,
                CAST(
                    (COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END)::float / 
                     NULLIF(COUNT(r.id_reserva), 0) * 100) AS DECIMAL(5,1)
                ) as taxa_sucesso_percent,
                'R$ ' || COALESCE(SUM(p.valor_total), 0) as receita_total
            FROM usuario u
            JOIN anfitriao af ON u.id_usuario = af.id_usuario
            JOIN imovel i ON u.id_usuario = i.id_usuario
            LEFT JOIN reserva r ON i.id_imovel = r.id_imovel
            LEFT JOIN gera g ON r.id_reserva = g.id_reserva
            LEFT JOIN pagamento p ON g.id_pagamento = p.id_pagamento
            GROUP BY u.id_usuario, u.nome
            ORDER BY COALESCE(SUM(p.valor_total), 0) DESC;
        """,
        
        "Ocupação por Período": """
            SELECT 
                TO_CHAR(r.data_inicio, 'YYYY-MM') as mes_ano,
                COUNT(r.id_reserva) as total_reservas,
                COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END) as confirmadas,
                COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END) as canceladas,
                COUNT(CASE WHEN r.status = 'pendente' THEN 1 END) as pendentes,
                ROUND(COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END)::numeric / 
                      NULLIF(COUNT(r.id_reserva), 0) * 100, 1) as taxa_sucesso
            FROM reserva r
            GROUP BY TO_CHAR(r.data_inicio, 'YYYY-MM')
            ORDER BY mes_ano DESC;
        """,
        
        "Hóspedes Mais Ativos": """
            SELECT 
                u.nome, 
                COUNT(*) AS total_reservas,
                COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END) as confirmadas,
                COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END) as canceladas
            FROM usuario u
            JOIN reserva r ON u.id_usuario = r.id_usuario
            GROUP BY u.nome, u.id_usuario
            ORDER BY total_reservas DESC;
        """
    },
    
    "📋 DASHBOARD EXECUTIVO": {
        "KPIs do Negócio": """
            SELECT 
                '👥 Total de Usuários' as metrica,
                (SELECT COUNT(*) FROM usuario)::text as valor
            UNION ALL
            SELECT 
                '🏠 Anfitriões Ativos',
                (SELECT COUNT(*) FROM anfitriao)::text
            UNION ALL
            SELECT 
                '🧳 Hóspedes Ativos', 
                (SELECT COUNT(*) FROM hospede)::text
            UNION ALL
            SELECT 
                '🏢 Total de Imóveis',
                (SELECT COUNT(*) FROM imovel)::text
            UNION ALL
            SELECT 
                '📋 Total de Reservas',
                (SELECT COUNT(*) FROM reserva)::text
            UNION ALL
            SELECT 
                '✅ Reservas Confirmadas',
                (SELECT COUNT(*) FROM reserva WHERE status = 'confirmada')::text
            UNION ALL
            SELECT 
                '❌ Reservas Canceladas',
                (SELECT COUNT(*) FROM reserva WHERE status = 'cancelada')::text
            UNION ALL
            SELECT 
                '💰 Receita Total',
                'R$ ' || (SELECT COALESCE(SUM(valor_total), 0) FROM pagamento)::text;
        """
    }
}

# Interface principal
def main():
    # Header principal
    st.markdown('''
    <div class="main-header">
        <h1>🏠 Sistema de Locação de Imóveis</h1>
        <p style="color: #e8f4fd; font-size: 1.1em; margin: 0.5rem 0 0 0; font-weight: 500;">
            Análise Completa do Banco de Dados
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Navegação")
    st.sidebar.markdown("---")
    
    # Seleção de categoria
    categoria_selecionada = st.sidebar.selectbox(
        "Selecione uma categoria:",
        list(CONSULTAS.keys())
    )
    
    # Seleção de consulta
    consulta_selecionada = st.sidebar.selectbox(
        "Selecione uma consulta:",
        list(CONSULTAS[categoria_selecionada].keys())
    )
    
    st.sidebar.markdown("---")
    
    # Informações do sistema
    st.sidebar.markdown("### ℹ️ Sobre o Sistema")
    st.sidebar.info(
        "Sistema desenvolvido para projeto acadêmica de banco de dados, projetando um banco para um Sistema de Locação de Imóveis por Temporada com 21 consultas organizadas por categoria."
    )
    
    # Área principal
    # Cabeçalho da consulta
    st.markdown(f'<div class="category-header"><h3>{categoria_selecionada}</h3></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="consulta-titulo">Consulta: {consulta_selecionada}</div>', unsafe_allow_html=True)
    
    # Layout em colunas para SQL e resultado inicial
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Mostrar código SQL
        sql_query = CONSULTAS[categoria_selecionada][consulta_selecionada]
        st.markdown("### 📝 Código SQL")
        st.code(sql_query, language='sql', line_numbers=True)
    
    with col2:
        st.markdown("### 📊 Resultado da Consulta")
        
        # Executar consulta
        with st.spinner('Executando consulta...'):
            df_resultado = executar_consulta(sql_query)
        
        if not df_resultado.empty:
            # Mostrar tabela completa com scroll
            st.dataframe(
                df_resultado, 
                use_container_width=True,
                height=400
            )
            st.info(f"📋 Total de {len(df_resultado)} registros encontrados")
        else:
            st.warning("Nenhum resultado encontrado.")
    
    # Opção de visualização em tela cheia
    if not df_resultado.empty:
        st.markdown("---")
        with st.expander("🔍 Visualização Completa", expanded=False):
            st.dataframe(
                df_resultado, 
                use_container_width=True,
                height=600
            )
            
            # Mostrar métricas para KPIs
            if consulta_selecionada == "KPIs do Negócio":
                st.markdown("### 📈 Métricas Principais")
                cols = st.columns(4)
                for idx, (i, row) in enumerate(df_resultado.iterrows()):
                    with cols[idx % 4]:
                        st.metric(
                            label=row['metrica'].replace('👥 ', '').replace('🏠 ', '').replace('🧳 ', '').replace('🏢 ', '').replace('📋 ', '').replace('✅ ', '').replace('❌ ', '').replace('💰 ', ''),
                            value=row['valor']
                        )
            
            # Gráficos específicos
            if consulta_selecionada == "Receita por Imóvel":
                fig = criar_grafico_receita_imoveis(df_resultado)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            elif consulta_selecionada == "Ocupação por Período":
                fig = criar_grafico_ocupacao(df_resultado)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Download dos dados
            csv = df_resultado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{consulta_selecionada.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )
    else:
        st.warning("Nenhum resultado encontrado para esta consulta.")
    
    # Footer
    st.markdown("---")
    st.markdown("### 🎓 Informações do Projeto")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Banco de Dados:** PostgreSQL")
    with col2:
        st.info("**Total de Consultas:** 21")
    with col3:
        st.info(f"**Última Atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

if __name__ == "__main__":
    main()
