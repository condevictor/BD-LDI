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
    .stSelectbox label, .stRadio label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
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
    .stMarkdown p {
        color: #333333 !important;
    }
    .css-1d391kg {
        background-color: #2c3e50 !important;
    }
    .css-1d391kg .stSelectbox label, 
    .css-1d391kg label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
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
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stSelectbox > label {
        color: white !important;
    }
    .stSidebar label,
    .stSidebar .stSelectbox label,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    .css-1544g2n label,
    .css-1544g2n .stSelectbox label {
        color: white !important;
        font-weight: 600 !important;
    }
    .consulta-titulo {
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 0.5rem;
        background: #1976d2;
        border-radius: 5px;
        margin: 1rem 0;
    }
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
        df = pd.read_sql_query(sql, conn) # type: ignore
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
        # Remove 'R$ ' e pontos de milhar / vírgula decimal (ajuste conforme seu formato)
        df_clean['receita_num'] = df_clean['receita_total'].astype(str).str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.')
        try:
            df_clean['receita_num'] = df_clean['receita_num'].astype(float)
        except:
            # se já estiver numérico, ignore
            df_clean['receita_num'] = pd.to_numeric(df_clean['receita_num'], errors='coerce').fillna(0.0)
        
        fig = px.bar(
            df_clean, 
            x=df_clean.columns[0] if 'titulo' not in df_clean.columns else 'titulo', 
            y='receita_num',
            title="💰 Receita Total por Imóvel",
            labels={'receita_num': 'Receita (R$)', df_clean.columns[0]: 'Imóvel'},
            color='receita_num',
            color_continuous_scale='viridis'
        )
        fig.update_layout(showlegend=False, height=400)
        return fig
    return None

def criar_grafico_ocupacao(df):
    """Cria gráfico de ocupação temporal"""
    # aceita tanto 'mes_ano' quanto 'mes' dependendo da query
    mes_col = None
    for c in ['mes_ano', 'mes']:
        if c in df.columns:
            mes_col = c
            break
    if not df.empty and mes_col is not None and 'confirmadas' in df.columns and 'canceladas' in df.columns:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[mes_col], 
            y=df['confirmadas'],
            mode='lines+markers',
            name='Confirmadas',
            line=dict(color='green', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df[mes_col], 
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

# Definição das consultas organizadas (todas as 21 que você enviou)
CONSULTAS = {
    "🏢 CONSULTAS OPERACIONAIS": {
        "1. Usuários e Perfis": """
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
        "2. Imóveis Disponíveis e suas Características": """
SELECT 
    i.titulo,
    CONCAT(i.cidade, ', ', i.estado) as localizacao,
    i.capacidade_max as capacidade,
    CONCAT('R$ ', i.valor_diaria) as diaria,
    pc.tipo_politica as politica,
    COUNT(DISTINCT c.comodidade) as total_comodidades
FROM imovel i
JOIN politica_cancelamento pc ON i.id_politica = pc.id_politica
LEFT JOIN comodidades c ON i.id_imovel = c.id_imovel
GROUP BY i.id_imovel, i.titulo, i.cidade, i.estado, i.capacidade_max, i.valor_diaria, pc.tipo_politica
ORDER BY i.valor_diaria DESC;
        """,
        "3. Reservas e Status Atual": """
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
        """,
        "4. Disponibilidade de Imóveis - Consulta Prática": """
SELECT 
    i.titulo,
    CONCAT(i.cidade, ', ', i.estado) as localizacao,
    i.capacidade_max as capacidade,
    CONCAT('R$ ', i.valor_diaria) as diaria_base,
    pc.tipo_politica as politica,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM reserva r 
            WHERE r.id_imovel = i.id_imovel 
            AND r.status IN ('confirmada', 'pendente')
            AND r.data_inicio <= CURRENT_DATE + INTERVAL '90 days'
            AND r.data_fim >= CURRENT_DATE
        ) THEN 'Reservado próximos 90 dias'
        WHEN EXISTS (
            SELECT 1 FROM reserva r 
            WHERE r.id_imovel = i.id_imovel 
            AND r.status = 'confirmada'
            AND r.data_inicio > CURRENT_DATE
        ) THEN 'Reservas futuras confirmadas'
        ELSE 'Disponível para reserva'
    END as disponibilidade_30d,
    COALESCE(ROUND(AVG(av.nota), 1), 0) as avaliacao_media,
    COUNT(DISTINCT cm.comodidade) as total_comodidades
FROM imovel i
JOIN politica_cancelamento pc ON i.id_politica = pc.id_politica
LEFT JOIN reserva r_av ON i.id_imovel = r_av.id_imovel AND r_av.status = 'confirmada'
LEFT JOIN experiencia_avaliada ea ON r_av.id_reserva = ea.id_reserva
LEFT JOIN avaliacao av ON ea.id_avaliacao = av.id_avaliacao
LEFT JOIN comodidades cm ON i.id_imovel = cm.id_imovel
GROUP BY i.id_imovel, i.titulo, i.cidade, i.estado, i.capacidade_max, 
         i.valor_diaria, pc.tipo_politica
ORDER BY avaliacao_media DESC, i.valor_diaria ASC;
        """
    },
    "💰 ANÁLISES FINANCEIRAS": {
        "5. Análise de Pagamentos": """
SELECT 
    p.id_pagamento as pagamento_id,
    CONCAT('R$ ', p.valor_total) as valor,
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
        "6. Receita por Imóvel": """
SELECT 
    i.titulo, 
    COUNT(r.id_reserva) as total_reservas,
    CONCAT('R$ ', COALESCE(SUM(p.valor_total), 0)) AS receita_total
FROM imovel i
LEFT JOIN reserva r ON i.id_imovel = r.id_imovel AND r.status = 'confirmada'
LEFT JOIN gera g ON r.id_reserva = g.id_reserva
LEFT JOIN pagamento p ON g.id_pagamento = p.id_pagamento
GROUP BY i.titulo, i.id_imovel
ORDER BY COALESCE(SUM(p.valor_total), 0) DESC;
        """,
        "7. Parcelas em Aberto - Gestão Financeira": """
SELECT 
    u.nome as hospede,
    i.titulo as imovel,
    CONCAT('R$ ', pg.valor_total) as valor_total,
    pg.forma_pagamento,
    CONCAT('Parcela ', p.num_parcelas) as parcela,
    CONCAT('R$ ', p.valor_parcela) as valor_parcela,
    TO_CHAR(p.data_vencimento, 'DD/MM/YYYY') as vencimento,
    CASE 
        WHEN p.data_vencimento < CURRENT_DATE THEN 'EM ATRASO'
        WHEN p.data_vencimento = CURRENT_DATE THEN 'VENCE HOJE'
        WHEN p.data_vencimento <= CURRENT_DATE + INTERVAL '7 days' THEN 'PRÓXIMO VENCIMENTO'
        ELSE 'EM DIA'
    END as status,
    (p.data_vencimento - CURRENT_DATE) as dias_para_vencimento
FROM parcela p
JOIN pagamento pg ON p.id_pagamento = pg.id_pagamento
JOIN gera g ON pg.id_pagamento = g.id_pagamento
JOIN reserva r ON g.id_reserva = r.id_reserva
JOIN usuario u ON r.id_usuario = u.id_usuario
JOIN imovel i ON r.id_imovel = i.id_imovel
WHERE p.data_vencimento >= CURRENT_DATE
ORDER BY p.data_vencimento, u.nome;
        """,
        "8. Receita Mensal por Anfitrião": """
SELECT 
    u.nome as anfitriao,
    TO_CHAR(p.data_pagamento, 'YYYY-MM') as mes_ano,
    COUNT(r.id_reserva) as reservas,
    CONCAT('R$ ', SUM(p.valor_total)) as receita_mensal
FROM usuario u
JOIN anfitriao a ON u.id_usuario = a.id_usuario
JOIN imovel i ON a.id_usuario = i.id_usuario
JOIN reserva r ON i.id_imovel = r.id_imovel
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN pagamento p ON g.id_pagamento = p.id_pagamento
WHERE r.status = 'confirmada'
GROUP BY u.nome, u.id_usuario, TO_CHAR(p.data_pagamento, 'YYYY-MM')
ORDER BY mes_ano DESC, SUM(p.valor_total) DESC;
        """,
        "9. Fluxo Financeiro Completo": """
SELECT r.id_reserva, 'Principal' as tipo, p.valor_total, p.forma_pagamento, p.data_pagamento
FROM reserva r
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN pagamento p ON g.id_pagamento = p.id_pagamento
UNION ALL
SELECT r.id_reserva, 'Multa' as tipo, p.valor_total, p.forma_pagamento, p.data_pagamento
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
        "10. Ranking de Anfitriões": """
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
    CONCAT('R$ ', COALESCE(SUM(p.valor_total), 0)) as receita_total,
    CONCAT('R$ ', CAST(COALESCE(AVG(p.valor_total), 0) AS DECIMAL(10,2))) as ticket_medio,
    CAST(COALESCE(AVG(a.nota), 0) AS DECIMAL(3,1)) as nota_media,
    COUNT(DISTINCT ea.id_avaliacao) as total_avaliacoes,
    CASE 
        WHEN AVG(a.nota) >= 4.5 THEN 'Excelente'
        WHEN AVG(a.nota) >= 4.0 THEN 'Muito Bom'
        WHEN AVG(a.nota) >= 3.0 THEN 'Bom'
        WHEN AVG(a.nota) >= 2.0 THEN 'Regular'
        ELSE 'Precisa Melhorar'
    END as classificacao
FROM usuario u
JOIN anfitriao af ON u.id_usuario = af.id_usuario
JOIN imovel i ON u.id_usuario = i.id_usuario
LEFT JOIN reserva r ON i.id_imovel = r.id_imovel
LEFT JOIN gera g ON r.id_reserva = g.id_reserva
LEFT JOIN pagamento p ON g.id_pagamento = p.id_pagamento
LEFT JOIN experiencia_avaliada ea ON r.id_reserva = ea.id_reserva
LEFT JOIN avaliacao a ON ea.id_avaliacao = a.id_avaliacao
GROUP BY u.id_usuario, u.nome
ORDER BY receita_total DESC, nota_media DESC;
        """,
        "11. Hóspedes Mais Ativos": """
SELECT 
    u.nome, 
    COUNT(*) AS total_reservas,
    COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END) as confirmadas,
    COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END) as canceladas
FROM usuario u
JOIN reserva r ON u.id_usuario = r.id_usuario
GROUP BY u.nome, u.id_usuario
ORDER BY total_reservas DESC;
        """,
        "12. Ocupação por Período": """
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
        "13. Relatório de Ocupação Completo": """
SELECT 
    i.titulo,
    i.capacidade_max as capacidade,
    COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END) as confirmadas,
    COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END) as canceladas,
    COUNT(CASE WHEN r.status = 'pendente' THEN 1 END) as pendentes,
    ROUND(AVG(r.num_hospedes), 1) as media_hospedes,
    COALESCE(SUM(CASE WHEN r.status = 'confirmada' THEN (r.data_fim - r.data_inicio) ELSE 0 END), 0) as dias_ocupados
FROM imovel i
LEFT JOIN reserva r ON i.id_imovel = r.id_imovel
GROUP BY i.titulo, i.id_imovel, i.capacidade_max
ORDER BY confirmadas DESC, dias_ocupados DESC;
        """
    },
    "⭐ SERVIÇOS E AVALIAÇÕES": {
        "14. Serviços Extras Mais Contratados": """
SELECT 
    se.nome as servico,
    CONCAT('R$ ', se.valor_servico) as valor,
    COUNT(sv.id_reserva) as vezes_contratado,
    CONCAT('R$ ', (se.valor_servico * COUNT(sv.id_reserva))) as receita_total
FROM servico_extra se
LEFT JOIN servicos_vinculados sv ON se.id_servico = sv.id_servico
GROUP BY se.id_servico, se.nome, se.valor_servico
ORDER BY COUNT(sv.id_reserva) DESC;
        """,
        "15. Serviços Extras - Contratações por Hóspede": """
SELECT 
    u.nome AS hospede, 
    se.nome AS servico,
    CONCAT('R$ ', se.valor_servico) as valor,
    COUNT(*) as vezes_contratado
FROM reserva r
JOIN servicos_vinculados sv ON r.id_reserva = sv.id_reserva
JOIN servico_extra se ON sv.id_servico = se.id_servico
JOIN usuario u ON r.id_usuario = u.id_usuario
GROUP BY u.nome, se.nome, se.valor_servico
ORDER BY u.nome, vezes_contratado DESC;
        """,
        "16. Avaliações e Qualidade dos Imóveis": """
SELECT 
    i.titulo as imovel,
    ROUND(AVG(a.nota), 1) as nota_media,
    COUNT(a.nota) as total_avaliacoes,
    CASE 
        WHEN AVG(a.nota) >= 4.5 THEN 'Excelente'
        WHEN AVG(a.nota) >= 4.0 THEN 'Muito Bom'
        WHEN AVG(a.nota) >= 3.5 THEN 'Bom'
        WHEN AVG(a.nota) >= 3.0 THEN 'Regular'
        ELSE 'Ruim'
    END as classificacao
FROM imovel i
LEFT JOIN reserva r ON i.id_imovel = r.id_imovel
LEFT JOIN experiencia_avaliada ea ON r.id_reserva = ea.id_reserva
LEFT JOIN avaliacao a ON ea.id_avaliacao = a.id_avaliacao
WHERE r.status = 'confirmada'
GROUP BY i.id_imovel, i.titulo
HAVING COUNT(a.nota) > 0
ORDER BY AVG(a.nota) DESC NULLS LAST;
        """,
        "17. Efetividade das Políticas de Cancelamento": """
SELECT 
    pc.tipo_politica,
    COUNT(DISTINCT i.id_imovel) as imoveis_com_politica,
    COUNT(r.id_reserva) as total_reservas,
    COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END) as cancelamentos,
    ROUND(COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END)::numeric / 
          NULLIF(COUNT(r.id_reserva), 0) * 100, 1) as taxa_cancelamento,
    COALESCE(SUM(e.valor_estorno), 0) as total_estornos
FROM politica_cancelamento pc
JOIN imovel i ON pc.id_politica = i.id_politica
LEFT JOIN reserva r ON i.id_imovel = r.id_imovel
LEFT JOIN reserva_cancelada rc ON r.id_reserva = (
    SELECT g.id_reserva FROM gera g 
    JOIN reserva_cancelada rc2 ON g.id_pagamento = rc2.id_pagamento 
    WHERE rc2.id_cancelamento = rc.id_cancelamento
)
LEFT JOIN gera_estorno ge ON rc.id_cancelamento = ge.id_cancelamento
LEFT JOIN estorno e ON ge.id_estorno = e.id_estorno
GROUP BY pc.id_politica, pc.tipo_politica
ORDER BY taxa_cancelamento ASC;
        """
    },
    "🚫 CANCELAMENTOS E POLÍTICAS": {
        "18. Cancelamentos e Impacto Financeiro": """
SELECT 
    c.data_cancelamento as data_cancel,
    c.tipo_cancelamento,
    CONCAT('R$ ', p.valor_total) as valor_reserva,
    COALESCE(CONCAT('R$ ', e.valor_estorno), 'Sem estorno') as valor_estorno,
    CASE 
        WHEN e.valor_estorno IS NULL THEN CONCAT('R$ ', p.valor_total)
        ELSE CONCAT('R$ ', (p.valor_total - e.valor_estorno))
    END as receita_liquida
FROM cancelamento c
JOIN reserva_cancelada rc ON c.id_cancelamento = rc.id_cancelamento
JOIN pagamento p ON rc.id_pagamento = p.id_pagamento
LEFT JOIN gera_estorno ge ON c.id_cancelamento = ge.id_cancelamento
LEFT JOIN estorno e ON ge.id_estorno = e.id_estorno
ORDER BY c.data_cancelamento DESC;
        """,
        "19. Análise de Estornos por Política": """
SELECT 
    pc.tipo_politica,
    COUNT(*) as total_estornos,
    CONCAT('R$ ', ROUND(AVG(e.valor_estorno), 2)) as valor_medio_estorno,
    CONCAT('R$ ', SUM(e.valor_estorno)) as valor_total_estornos
FROM politica_cancelamento pc
JOIN imovel i ON pc.id_politica = i.id_politica
JOIN reserva r ON i.id_imovel = r.id_imovel
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN reserva_cancelada rc ON g.id_pagamento = rc.id_pagamento
JOIN gera_estorno ge ON rc.id_cancelamento = ge.id_cancelamento
JOIN estorno e ON ge.id_estorno = e.id_estorno
GROUP BY pc.tipo_politica;
        """
    },
    "📋 RELATÓRIOS ESPECIAIS": {
        "20. Histórico Completo - Casa da Praia": """
SELECT 
    u.nome as hospede,
    TO_CHAR(r.data_inicio, 'DD/MM/YYYY') as check_in,
    TO_CHAR(r.data_fim, 'DD/MM/YYYY') as check_out,
    r.status,
    COALESCE(a.nota::text, 'Sem avaliação') as nota,
    CASE 
        WHEN r.status = 'cancelada' THEN TO_CHAR(c.data_cancelamento, 'DD/MM/YYYY')
        ELSE NULL 
    END as data_cancelamento
FROM imovel i
LEFT JOIN reserva r ON i.id_imovel = r.id_imovel
LEFT JOIN usuario u ON r.id_usuario = u.id_usuario
LEFT JOIN experiencia_avaliada ea ON r.id_reserva = ea.id_reserva
LEFT JOIN avaliacao a ON ea.id_avaliacao = a.id_avaliacao
LEFT JOIN gera g ON r.id_reserva = g.id_reserva
LEFT JOIN reserva_cancelada rc ON g.id_pagamento = rc.id_pagamento
LEFT JOIN cancelamento c ON rc.id_cancelamento = c.id_cancelamento
WHERE i.titulo = 'Casa da Praia'
ORDER BY r.data_inicio DESC;
        """,
        "21. KPIs do Negócio": """
SELECT 
    'Total de Usuários' as metrica,
    (SELECT COUNT(*) FROM usuario)::text as valor
UNION ALL
SELECT 
    'Anfitriões Ativos',
    (SELECT COUNT(*) FROM anfitriao)::text
UNION ALL
SELECT 
    'Hóspedes Ativos', 
    (SELECT COUNT(*) FROM hospede)::text
UNION ALL
SELECT 
    'Total de Imóveis',
    (SELECT COUNT(*) FROM imovel)::text
UNION ALL
SELECT 
    'Total de Reservas',
    (SELECT COUNT(*) FROM reserva)::text
UNION ALL
SELECT 
    'Reservas Confirmadas',
    (SELECT COUNT(*) FROM reserva WHERE status = 'confirmada')::text
UNION ALL
SELECT 
    'Reservas Canceladas',
    (SELECT COUNT(*) FROM reserva WHERE status = 'cancelada')::text
UNION ALL
SELECT 
    'Reservas Pendentes',
    (SELECT COUNT(*) FROM reserva WHERE status = 'pendente')::text
UNION ALL
SELECT 
    'Receita Total',
    CONCAT('R$ ', (SELECT COALESCE(SUM(valor_total), 0) FROM pagamento)::text)
UNION ALL
SELECT 
    'Nota Média Geral',
    CONCAT((SELECT COALESCE(ROUND(AVG(nota), 1), 0) FROM avaliacao)::text, '/5');
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
