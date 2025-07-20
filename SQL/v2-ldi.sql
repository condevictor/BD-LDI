-- ============================================
-- SISTEMA DE LOCAÇÃO DE IMÓVEIS - DATABASE
-- ============================================

-- LIMPEZA DO BANCO (Remove tudo se já existir)
DROP TABLE IF EXISTS gera_pag_multa CASCADE;
DROP TABLE IF EXISTS gera_multa CASCADE;
DROP TABLE IF EXISTS multa CASCADE;
DROP TABLE IF EXISTS gera_estorno CASCADE;
DROP TABLE IF EXISTS estorno CASCADE;
DROP TABLE IF EXISTS reserva_cancelada CASCADE;
DROP TABLE IF EXISTS cancelamento CASCADE;
DROP TABLE IF EXISTS parcela CASCADE;
DROP TABLE IF EXISTS gera CASCADE;
DROP TABLE IF EXISTS pagamento CASCADE;
DROP TABLE IF EXISTS servicos_vinculados CASCADE;
DROP TABLE IF EXISTS experiencia_avaliada CASCADE;
DROP TABLE IF EXISTS avaliacao CASCADE;
DROP TABLE IF EXISTS reserva CASCADE;
DROP TABLE IF EXISTS oferece CASCADE;
DROP TABLE IF EXISTS servico_extra CASCADE;
DROP TABLE IF EXISTS comodidades CASCADE;
DROP TABLE IF EXISTS imovel CASCADE;
DROP TABLE IF EXISTS politica_cancelamento CASCADE;
DROP TABLE IF EXISTS hospede CASCADE;
DROP TABLE IF EXISTS anfitriao CASCADE;
DROP TABLE IF EXISTS telefone_usuario CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;
DROP TYPE IF EXISTS enum_forma_pagamento CASCADE;

-- Tipo ENUM para forma de pagamento
CREATE TYPE enum_forma_pagamento AS ENUM (
    'Cartão de crédito',
    'Pix',
    'Boleto',
    'Transferência Bancária',
    'Dinheiro'
);

-- Tabela de usuários
CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

-- Telefones associados a um usuário
CREATE TABLE telefone_usuario (
    telefone VARCHAR(30) NOT NULL,
    id_usuario INT NOT NULL,
    PRIMARY KEY (telefone, id_usuario),
    CONSTRAINT fk_telefone_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Usuário do tipo anfitrião
CREATE TABLE anfitriao (
    id_usuario INT PRIMARY KEY,
    CONSTRAINT fk_anfitriao_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Usuário do tipo hóspede
CREATE TABLE hospede (
    id_usuario INT PRIMARY KEY,
    CONSTRAINT fk_hospede_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Política de cancelamento
CREATE TABLE politica_cancelamento (
    id_politica INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tipo_politica VARCHAR(255) NOT NULL,
    descricao TEXT
);

-- Imóvel cadastrado por um anfitrião
CREATE TABLE imovel (
    id_imovel INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_usuario INT NOT NULL,
    id_politica INT NOT NULL,
    capacidade_max INT NOT NULL,
    valor_diaria NUMERIC(15,2) NOT NULL,
    rua VARCHAR(255),
    numero VARCHAR(10),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    cep VARCHAR(20),
    titulo VARCHAR(255),
    descricao TEXT,
    CONSTRAINT fk_imovel_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    CONSTRAINT fk_imovel_politica FOREIGN KEY (id_politica) REFERENCES politica_cancelamento(id_politica)
);

-- Comodidades associadas ao imóvel
CREATE TABLE comodidades (
    id_imovel INT NOT NULL,
    comodidade VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_imovel, comodidade),
    CONSTRAINT fk_comodidade_imovel FOREIGN KEY (id_imovel) REFERENCES imovel(id_imovel)
);

-- Serviços extras que podem ser oferecidos
CREATE TABLE servico_extra (
    id_servico INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    valor_servico NUMERIC(15,2) NOT NULL
);

-- Serviços oferecidos por um imóvel
CREATE TABLE oferece (
    id_servico INT NOT NULL,
    id_imovel INT NOT NULL,
    PRIMARY KEY (id_servico, id_imovel),
    CONSTRAINT fk_oferece_servico FOREIGN KEY (id_servico) REFERENCES servico_extra(id_servico),
    CONSTRAINT fk_oferece_imovel FOREIGN KEY (id_imovel) REFERENCES imovel(id_imovel)
);

-- Reservas feitas por hóspedes
CREATE TABLE reserva (
    id_reserva INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_usuario INT NOT NULL,
    id_imovel INT NOT NULL,
    num_hospedes INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    CONSTRAINT fk_reserva_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    CONSTRAINT fk_reserva_imovel FOREIGN KEY (id_imovel) REFERENCES imovel(id_imovel)
);

-- Avaliações feitas após a estadia
CREATE TABLE avaliacao (
    id_avaliacao INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nota INT NOT NULL CHECK (nota BETWEEN 0 AND 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relação entre avaliação e reserva
CREATE TABLE experiencia_avaliada (
    id_reserva INT PRIMARY KEY,
    id_avaliacao INT NOT NULL,
    CONSTRAINT fk_expav_reserva FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva),
    CONSTRAINT fk_expav_avaliacao FOREIGN KEY (id_avaliacao) REFERENCES avaliacao(id_avaliacao)
);

-- Vincula serviços extras às reservas
CREATE TABLE servicos_vinculados (
    id_servico INT NOT NULL,
    id_reserva INT NOT NULL,
    PRIMARY KEY (id_servico, id_reserva),
    CONSTRAINT fk_sv_servico FOREIGN KEY (id_servico) REFERENCES servico_extra(id_servico),
    CONSTRAINT fk_sv_reserva FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

-- Pagamentos realizados
CREATE TABLE pagamento (
    id_pagamento INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    valor_total NUMERIC(15,2) NOT NULL,
    forma_pagamento enum_forma_pagamento NOT NULL,
    data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relação entre pagamento e reserva
CREATE TABLE gera (
    id_pagamento INT PRIMARY KEY,
    id_reserva INT NOT NULL,
    CONSTRAINT fk_gera_pag FOREIGN KEY (id_pagamento) REFERENCES pagamento(id_pagamento),
    CONSTRAINT fk_gera_reserva FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

-- Parcelas de um pagamento
CREATE TABLE parcela (
    id_pagamento INT NOT NULL,
    num_parcelas INT NOT NULL,
    valor_parcela NUMERIC(15,2) NOT NULL,
    data_vencimento DATE NOT NULL,
    PRIMARY KEY (id_pagamento, num_parcelas),
    CONSTRAINT fk_parcela_pagamento FOREIGN KEY (id_pagamento) REFERENCES pagamento(id_pagamento)
);

-- Cancelamentos de reservas
CREATE TABLE cancelamento (
    id_cancelamento INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tipo_cancelamento VARCHAR(255),
    data_cancelamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relaciona cancelamento com pagamento
CREATE TABLE reserva_cancelada (
    id_cancelamento INT PRIMARY KEY,
    id_pagamento INT NOT NULL,
    CONSTRAINT fk_rc_cancelamento FOREIGN KEY (id_cancelamento) REFERENCES cancelamento(id_cancelamento),
    CONSTRAINT fk_rc_pagamento FOREIGN KEY (id_pagamento) REFERENCES pagamento(id_pagamento)
);

-- Estornos gerados a partir de cancelamentos
CREATE TABLE estorno (
    id_estorno INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    valor_estorno NUMERIC(15,2) NOT NULL,
    data_estorno TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE gera_estorno (
    id_estorno INT PRIMARY KEY,
    id_cancelamento INT NOT NULL,
    CONSTRAINT fk_ge_estorno FOREIGN KEY (id_estorno) REFERENCES estorno(id_estorno),
    CONSTRAINT fk_ge_cancel FOREIGN KEY (id_cancelamento) REFERENCES cancelamento(id_cancelamento)
);

-- Multas aplicadas por cancelamentos
CREATE TABLE multa (
    id_multa INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    valor_multa NUMERIC(15,2) NOT NULL
);

CREATE TABLE gera_multa (
    id_multa INT PRIMARY KEY,
    id_cancelamento INT NOT NULL,
    CONSTRAINT fk_gm_multa FOREIGN KEY (id_multa) REFERENCES multa(id_multa),
    CONSTRAINT fk_gm_cancel FOREIGN KEY (id_cancelamento) REFERENCES cancelamento(id_cancelamento)
);

-- Pagamento de multas
CREATE TABLE gera_pag_multa (
    id_multa INT NOT NULL,
    id_pagamento INT NOT NULL,
    PRIMARY KEY (id_multa, id_pagamento),
    CONSTRAINT fk_gpm_multa FOREIGN KEY (id_multa) REFERENCES multa(id_multa),
    CONSTRAINT fk_gpm_pag FOREIGN KEY (id_pagamento) REFERENCES pagamento(id_pagamento)
);

-- POPULANDO A BASE E CONSULTANDO DADOS DO SISTEMA DE LOCAÇÃO --

-- Inserção de políticas de cancelamento
INSERT INTO politica_cancelamento (tipo_politica, descricao) VALUES
('Flexível', 'Cancelamento gratuito até 7 dias antes da reserva'),
('Moderada', 'Cancelamento gratuito até 5 dias antes, depois multa de 50%'),
('Rígida', 'Sem cancelamento gratuito, multa de 100%');

-- Inserção de serviços extras
INSERT INTO servico_extra (nome, descricao, valor_servico) VALUES
('Café da manhã', 'Serviço diário de café da manhã', 50.00),
('Limpeza', 'Limpeza durante a estadia', 80.00),
('Transfer aeroporto', 'Transporte do aeroporto até o imóvel', 100.00),
('Wi-Fi premium', 'Internet de alta velocidade', 30.00),
('Estacionamento coberto', 'Vaga protegida para veículo', 25.00);

-- Inserção de usuários
INSERT INTO usuario (nome, email, senha) VALUES
('Carlos Silva', 'carlos@email.com', 'senha123'),    -- Anfitrião
('Ana Souza', 'ana@email.com', 'senha456'),         -- Hóspede
('João Lima', 'joao@email.com', 'senha789'),        -- Anfitrião E Hóspede
('Maria Santos', 'maria@email.com', 'senha101'),    -- Hóspede
('Pedro Costa', 'pedro@email.com', 'senha202'),     -- Hóspede
('Julia Oliveira', 'julia@email.com', 'senha303');  -- Hóspede

-- Inserção de telefones dos usuários
INSERT INTO telefone_usuario (id_usuario, telefone) VALUES
(1, '(11)90000-0001'), (2, '(21)98888-0001'), 
(3, '(31)97777-0001'), (4, '(85)99999-0001'),
(5, '(11)96666-0001'), (6, '(21)95555-0001');

-- Inserção de anfitriões (usuários 1 e 3)
INSERT INTO anfitriao (id_usuario) VALUES (1), (3);

-- Inserção de hóspedes (usuários 2, 3, 4, 5, 6)
INSERT INTO hospede (id_usuario) VALUES (2), (3), (4), (5), (6);

-- Inserção de imóveis
INSERT INTO imovel (id_usuario, id_politica, capacidade_max, valor_diaria, rua, numero, bairro, cidade, estado, cep, titulo, descricao) VALUES
(1, 1, 6, 400.00, 'Av. Atlântica', '100', 'Copacabana', 'Rio de Janeiro', 'RJ', '22000-000', 'Casa da Praia', 'Casa com vista para o mar'),
(3, 2, 4, 300.00, 'Rua das Pedras', '200', 'Centro', 'Campos do Jordão', 'SP', '12460-000', 'Chalé na Montanha', 'Ideal para relaxar'),
(4, 3, 2, 150.00, 'Rua das Flores', '50', 'Centro', 'São Paulo', 'SP', '01000-000', 'Apartamento Centro', 'Moderno e bem localizado'),
(6, 1, 8, 250.00, 'Estrada Rural', 'KM 5', 'Zona Rural', 'Atibaia', 'SP', '12940-000', 'Casa de Campo', 'Tranquila para família'),
(1, 2, 3, 200.00, 'Rua do Porto', '30', 'Centro Histórico', 'Salvador', 'BA', '40000-000', 'Loft Colonial', 'Charme histórico');

-- Inserção de comodidades dos imóveis
INSERT INTO comodidades (id_imovel, comodidade) VALUES
(1, 'Wi-Fi'), (1, 'Piscina'), (1, 'Ar-condicionado'), (1, 'Estacionamento'),
(2, 'Wi-Fi'), (2, 'Ar-condicionado'), (2, 'Lareira'),
(3, 'Wi-Fi'), (3, 'Academia'),
(4, 'Wi-Fi'), (4, 'Piscina'), (4, 'Churrasqueira'), (4, 'Estacionamento'),
(5, 'Wi-Fi'), (5, 'Ar-condicionado'), (5, 'Vista histórica');

-- Inserção de serviços extras disponíveis por imóvel
INSERT INTO oferece (id_servico, id_imovel) VALUES
(1, 1), (2, 1), (3, 1), (4, 1),  -- Casa da Praia oferece quase todos
(2, 2), (3, 2),                   -- Chalé oferece limpeza e transfer
(1, 3), (4, 3),                   -- Apartamento oferece café e Wi-Fi premium
(1, 4), (2, 4), (5, 4),          -- Casa de Campo oferece café, limpeza e estacionamento
(1, 5), (2, 5);                   -- Loft oferece café e limpeza

-- 2. CENÁRIOS ABRANGENTES DE RESERVAS


-- Inserção de todas as reservas (confirmadas, pendentes, futuras e canceladas)
INSERT INTO reserva (id_usuario, id_imovel, num_hospedes, data_inicio, data_fim, status) VALUES
-- Reservas confirmadas (para testar pagamentos e avaliações)
(2, 1, 4, '2025-01-15', '2025-01-20', 'confirmada'),  -- Ana na Casa da Praia
(4, 2, 2, '2025-02-10', '2025-02-15', 'confirmada'),  -- Maria no Chalé
(5, 3, 1, '2025-03-01', '2025-03-05', 'confirmada'),  -- Pedro no Apartamento
(6, 4, 6, '2025-04-01', '2025-04-07', 'confirmada'),  -- Julia na Casa de Campo
-- Reservas pendentes (para testar status)
(3, 5, 2, '2025-05-10', '2025-05-15', 'pendente'),    -- João no Loft
-- Reservas ATUAIS (julho 2025 - para mostrar ocupação real)
(2, 1, 3, '2025-07-18', '2025-07-25', 'confirmada'),  -- Ana na Casa da Praia (ATUAL)
(4, 3, 1, '2025-07-20', '2025-07-23', 'confirmada'),  -- Maria no Apartamento (ATUAL)
-- Reservas futuras (para testar disponibilidade)
(2, 2, 3, '2025-08-20', '2025-08-25', 'confirmada'),  -- Ana no Chalé (futura)
(4, 1, 5, '2025-09-10', '2025-09-17', 'confirmada'),  -- Maria na Casa da Praia (futura)
-- Reservas canceladas (para testar cancelamentos, multas e estornos)
(5, 1, 2, '2025-06-01', '2025-06-05', 'cancelada'),   -- Pedro cancelou Casa da Praia (política flexível)
(6, 3, 1, '2025-07-01', '2025-07-03', 'cancelada'),   -- Julia cancelou Apartamento (política rígida)
(3, 4, 4, '2025-08-01', '2025-08-05', 'cancelada');   -- João cancelou Casa de Campo (política flexível)

-- 3. PAGAMENTOS PRINCIPAIS DAS RESERVAS CONFIRMADAS

INSERT INTO pagamento (valor_total, forma_pagamento, data_pagamento) VALUES
(2000.00, 'Cartão de crédito', '2025-01-10'),  -- Reserva 1 (5 diárias × 400)
(1500.00, 'Pix', '2025-02-05'),                -- Reserva 2 (5 diárias × 300)
(600.00, 'Boleto', '2025-02-25'),              -- Reserva 3 (4 diárias × 150)
(1750.00, 'Transferência Bancária', '2025-03-25'), -- Reserva 4 (7 diárias × 250)
(1000.00, 'Cartão de crédito', '2025-05-05'),  -- Reserva 5 (5 diárias × 200)
(2800.00, 'Cartão de crédito', '2025-07-15'),  -- Reserva 6 (atual - Casa da Praia)
(450.00, 'Pix', '2025-07-18'),                 -- Reserva 7 (atual - Apartamento)
(1500.00, 'Pix', '2025-08-15'),                -- Reserva 8 (futura - Chalé)
(2800.00, 'Cartão de crédito', '2025-09-05'),  -- Reserva 9 (futura - Casa da Praia)
(1600.00, 'Boleto', '2025-05-25'),             -- Reserva 10 (cancelada)
(450.00, 'Pix', '2025-06-25'),                 -- Reserva 11 (cancelada)
(1000.00, 'Cartão de crédito', '2025-07-25');  -- Reserva 12 (cancelada)

-- Relacionar pagamentos com reservas
INSERT INTO gera (id_pagamento, id_reserva) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12);

-- 4. PARCELAMENTOS (ALGUNS PAGAMENTOS À VISTA, OUTROS PARCELADOS)

INSERT INTO parcela (id_pagamento, num_parcelas, valor_parcela, data_vencimento) VALUES
-- Pagamento 1 - PARCELADO em 2x (cartão de crédito)
(1, 1, 1000.00, '2025-01-10'),
(1, 2, 1000.00, '2025-02-10'),

-- Pagamento 2 - À VISTA (Pix)
(2, 1, 1500.00, '2025-02-05'),

-- Pagamento 3 - À VISTA (Boleto)  
(3, 1, 600.00, '2025-02-25'),

-- Pagamento 4 - PARCELADO em 3x (transferência)
(4, 1, 583.33, '2025-03-25'),
(4, 2, 583.33, '2025-04-25'),
(4, 3, 583.34, '2025-05-25'),

-- Pagamento 5 - À VISTA (cartão débito)
(5, 1, 1000.00, '2025-05-05'),

-- Pagamento 6 - PARCELADO em 2x (reserva atual)
(6, 1, 1400.00, '2025-07-15'),
(6, 2, 1400.00, '2025-08-15'),

-- Pagamento 7 - À VISTA (reserva atual)
(7, 1, 450.00, '2025-07-18'),

-- Pagamento 8 - PARCELADO em 2x (futura)
(8, 1, 750.00, '2025-08-15'),
(8, 2, 750.00, '2025-09-15'),

-- Pagamento 9 - PARCELADO em 2x (futura)
(9, 1, 1400.00, '2025-09-10'),
(9, 2, 1400.00, '2025-10-10'),

-- Pagamentos cancelados - todos à vista
-- Pagamento 10 - À VISTA (cancelado)
(10, 1, 1600.00, '2025-05-25'),

-- Pagamento 11 - À VISTA (cancelado)  
(11, 1, 450.00, '2025-06-25'),

-- Pagamento 12 - À VISTA (cancelado)
(12, 1, 1000.00, '2025-07-25');


-- 5. SERVIÇOS EXTRAS CONTRATADOS

INSERT INTO servicos_vinculados (id_servico, id_reserva) VALUES
(1, 1), (2, 1), (3, 1),  -- Reserva 1: café, limpeza, transfer
(2, 2), (3, 2),          -- Reserva 2: limpeza, transfer
(1, 3), (4, 3),          -- Reserva 3: café, Wi-Fi premium
(1, 4), (2, 4),          -- Reserva 4: café, limpeza
(1, 5);                   -- Reserva 5: café

-- 6. CANCELAMENTOS E CONSEQUÊNCIAS

-- Cancelamento com política flexível (sem multa, estorno total)
-- Inserção de todos os cancelamentos
INSERT INTO cancelamento (tipo_cancelamento, data_cancelamento) VALUES
-- Cancelamentos com política flexível (estorno parcial)
('Voluntário pelo hóspede', '2025-05-20'),  -- Cancelamento da reserva 8
('Voluntário pelo hóspede', '2025-07-20'),  -- Cancelamento da reserva 10
-- Cancelamento com política rígida (multa total, sem estorno)
('Voluntário pelo hóspede', '2025-06-25');  -- Cancelamento da reserva 9

-- Relacionar cancelamentos com pagamentos
INSERT INTO reserva_cancelada (id_cancelamento, id_pagamento) VALUES
(1, 10), (2, 12), (3, 11);

-- Estornos para cancelamentos com política flexível
INSERT INTO estorno (valor_estorno, data_estorno) VALUES
(1600.00, '2025-05-22'),  -- Estorno total da reserva 10
(1000.00, '2025-07-22');  -- Estorno total da reserva 12

INSERT INTO gera_estorno (id_estorno, id_cancelamento) VALUES
(1, 1), (2, 2);

-- Multa para cancelamento com política rígida
INSERT INTO multa (valor_multa) VALUES
(450.00);  -- Multa total da reserva 11

INSERT INTO gera_multa (id_multa, id_cancelamento) VALUES
(1, 3);

-- Pagamento da multa
INSERT INTO pagamento (valor_total, forma_pagamento, data_pagamento) VALUES
(450.00, 'Pix', '2025-06-26');

INSERT INTO gera_pag_multa (id_multa, id_pagamento) VALUES
(1, 13);

-- 7. AVALIAÇÕES DAS RESERVAS FINALIZADAS

INSERT INTO avaliacao (nota, comentario, data_avaliacao) VALUES
(5, 'Excelente estadia! Casa maravilhosa com vista incrível.', '2025-01-21'),
(4, 'Muito bom, apenas o wi-fi poderia ser melhor.', '2025-02-16'),
(3, 'Apartamento ok, mas barulhento à noite.', '2025-03-06'),
(5, 'Perfeito para família! Crianças adoraram a piscina.', '2025-04-08'),
(4, 'Charme histórico único, recomendo!', '2025-05-16');

-- Relacionar avaliações com reservas
INSERT INTO experiencia_avaliada (id_reserva, id_avaliacao) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5);


-- ============================================================================
-- CONSULTAS SQL PARA DEMONSTRAÇÃO - IDÊNTICAS AO SISTEMA PYTHON
-- ============================================================================
-- Total: 21 consultas organizadas por categoria
-- Sincronizadas com apresentacao_ldi.py para apresentação consistente

-- =============================================================================
-- 🏢 CONSULTAS OPERACIONAIS BÁSICAS (4 consultas)
-- =============================================================================

-- Consulta 1: USUÁRIOS E SEUS PERFIS
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

-- Consulta 2: IMÓVEIS DISPONÍVEIS E SUAS CARACTERÍSTICAS
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

-- Consulta 3: RESERVAS E STATUS ATUAL
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

-- Consulta 4: DISPONIBILIDADE DE IMÓVEIS - CONSULTA PRÁTICA
SELECT 
    i.titulo,
    i.cidade || ', ' || i.estado as localizacao,
    i.capacidade_max as capacidade,
    'R$ ' || i.valor_diaria as diaria_base,
    pc.tipo_politica as politica,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM reserva r 
            WHERE r.id_imovel = i.id_imovel 
            AND r.status IN ('confirmada', 'pendente')
            AND r.data_inicio <= CURRENT_DATE + INTERVAL '90 days'
            AND r.data_fim >= CURRENT_DATE
        ) THEN '🟡 Reservado próximos 90 dias'
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

-- =============================================================================
-- ANÁLISES FINANCEIRAS (4 consultas)
-- =============================================================================

-- Consulta 5: ANÁLISE FINANCEIRA - PAGAMENTOS
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

-- Consulta 6: RECEITA TOTAL POR IMÓVEL
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

-- Consulta 7: PARCELAS EM ABERTO - GESTÃO FINANCEIRA
SELECT 
    u.nome as hospede,
    i.titulo as imovel,
    'R$ ' || pg.valor_total as valor_total,
    pg.forma_pagamento,
    'Parcela ' || p.num_parcelas as parcela,
    'R$ ' || p.valor_parcela as valor_parcela,
    TO_CHAR(p.data_vencimento, 'DD/MM/YYYY') as vencimento,
    CASE 
        WHEN p.data_vencimento < CURRENT_DATE THEN '🔴 EM ATRASO'
        WHEN p.data_vencimento = CURRENT_DATE THEN '🟡 VENCE HOJE'
        WHEN p.data_vencimento <= CURRENT_DATE + INTERVAL '7 days' THEN '🟠 PRÓXIMO VENCIMENTO'
        ELSE '🟢 EM DIA'
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

-- Consulta 8: RECEITA MENSAL POR ANFITRIÃO
SELECT 
    u.nome as anfitriao,
    TO_CHAR(p.data_pagamento, 'YYYY-MM') as mes_ano,
    COUNT(r.id_reserva) as reservas,
    'R$ ' || SUM(p.valor_total) as receita_mensal
FROM usuario u
JOIN anfitriao a ON u.id_usuario = a.id_usuario
JOIN imovel i ON a.id_usuario = i.id_usuario
JOIN reserva r ON i.id_imovel = r.id_imovel
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN pagamento p ON g.id_pagamento = p.id_pagamento
WHERE r.status = 'confirmada'
GROUP BY u.nome, u.id_usuario, TO_CHAR(p.data_pagamento, 'YYYY-MM')
ORDER BY mes_ano DESC, SUM(p.valor_total) DESC;

-- Consulta 21: FLUXO FINANCEIRO COMPLETO POR RESERVA
-- Unifica pagamentos principais e multas para análise integrada
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

-- =============================================================================
-- BUSINESS INTELLIGENCE (4 consultas)
-- =============================================================================

-- Consulta 9: RANKING DE ANFITRIÕES - PERFORMANCE COMPLETA
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
    'R$ ' || COALESCE(SUM(p.valor_total), 0) as receita_total,
    'R$ ' || CAST(COALESCE(AVG(p.valor_total), 0) AS DECIMAL(10,2)) as ticket_medio,
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

-- Consulta 10: HÓSPEDES MAIS ATIVOS - RANKING
SELECT 
    u.nome, 
    COUNT(*) AS total_reservas,
    COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END) as confirmadas,
    COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END) as canceladas
FROM usuario u
JOIN reserva r ON u.id_usuario = r.id_usuario
GROUP BY u.nome, u.id_usuario
ORDER BY total_reservas DESC;

-- Consulta 11: OCUPAÇÃO POR PERÍODO - ANÁLISE TEMPORAL
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

-- Consulta 12: RELATÓRIO DE OCUPAÇÃO COMPLETO
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

-- =============================================================================
-- 🛎️ SERVIÇOS E AVALIAÇÕES (4 consultas)
-- =============================================================================

-- Consulta 13: SERVIÇOS EXTRAS MAIS CONTRATADOS
SELECT 
    se.nome as servico,
    'R$ ' || se.valor_servico as valor,
    COUNT(sv.id_reserva) as vezes_contratado,
    'R$ ' || (se.valor_servico * COUNT(sv.id_reserva)) as receita_total
FROM servico_extra se
LEFT JOIN servicos_vinculados sv ON se.id_servico = sv.id_servico
GROUP BY se.id_servico, se.nome, se.valor_servico
ORDER BY COUNT(sv.id_reserva) DESC;

-- Consulta 14: SERVIÇOS EXTRAS - CONTRATAÇÕES POR HÓSPEDE
SELECT 
    u.nome AS hospede, 
    se.nome AS servico,
    'R$ ' || se.valor_servico as valor,
    COUNT(*) as vezes_contratado
FROM reserva r
JOIN servicos_vinculados sv ON r.id_reserva = sv.id_reserva
JOIN servico_extra se ON sv.id_servico = se.id_servico
JOIN usuario u ON r.id_usuario = u.id_usuario
GROUP BY u.nome, se.nome, se.valor_servico
ORDER BY u.nome, vezes_contratado DESC;

-- Consulta 15: AVALIAÇÕES E QUALIDADE DOS IMÓVEIS
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

-- Consulta 16: EFETIVIDADE DAS POLÍTICAS DE CANCELAMENTO
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

-- =============================================================================
-- 🔄 CANCELAMENTOS E POLÍTICAS (2 consultas)
-- =============================================================================

-- Consulta 17: CANCELAMENTOS E IMPACTO FINANCEIRO
SELECT 
    c.data_cancelamento as data_cancel,
    c.tipo_cancelamento,
    'R$ ' || p.valor_total as valor_reserva,
    COALESCE('R$ ' || e.valor_estorno, 'Sem estorno') as valor_estorno,
    CASE 
        WHEN e.valor_estorno IS NULL THEN 'R$ ' || p.valor_total
        ELSE 'R$ ' || (p.valor_total - e.valor_estorno)
    END as receita_liquida
FROM cancelamento c
JOIN reserva_cancelada rc ON c.id_cancelamento = rc.id_cancelamento
JOIN pagamento p ON rc.id_pagamento = p.id_pagamento
LEFT JOIN gera_estorno ge ON c.id_cancelamento = ge.id_cancelamento
LEFT JOIN estorno e ON ge.id_estorno = e.id_estorno
ORDER BY c.data_cancelamento DESC;

-- Consulta 18: ANÁLISE DE ESTORNOS POR POLÍTICA
SELECT 
    pc.tipo_politica,
    COUNT(*) as total_estornos,
    'R$ ' || ROUND(AVG(e.valor_estorno), 2) as valor_medio_estorno,
    'R$ ' || SUM(e.valor_estorno) as valor_total_estornos
FROM politica_cancelamento pc
JOIN imovel i ON pc.id_politica = i.id_politica
JOIN reserva r ON i.id_imovel = r.id_imovel
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN reserva_cancelada rc ON g.id_pagamento = rc.id_pagamento
JOIN gera_estorno ge ON rc.id_cancelamento = ge.id_cancelamento
JOIN estorno e ON ge.id_estorno = e.id_estorno
GROUP BY pc.tipo_politica;

-- =============================================================================
-- RELATÓRIOS ESPECIAIS (2 consultas)
-- =============================================================================

-- Consulta 19: HISTÓRICO COMPLETO - CASA DA PRAIA
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

-- Consulta 20: DASHBOARD EXECUTIVO - KPIs DO NEGÓCIO
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
    'R$ ' || (SELECT COALESCE(SUM(valor_total), 0) FROM pagamento)::text
UNION ALL
SELECT 
    'Nota Média Geral',
    (SELECT COALESCE(ROUND(AVG(nota), 1), 0) FROM avaliacao)::text || '/5';

-- ============================================================================
-- FIM DAS CONSULTAS - TOTAL: 21 CONSULTAS 
-- ============================================================================
