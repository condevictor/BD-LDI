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
('Maria Santos', 'maria@email.com', 'senha101');    -- Hóspede

-- Inserção de telefones dos usuários
INSERT INTO telefone_usuario (id_usuario, telefone) VALUES
(1, '(11)90000-0001'), (2, '(21)98888-0001'), 
(3, '(31)97777-0001'), (4, '(85)99999-0001');

-- Inserção de anfitriões (usuários 1 e 3)
INSERT INTO anfitriao (id_usuario) VALUES (1), (3);

-- Inserção de hóspedes (usuários 2 e 3)
INSERT INTO hospede (id_usuario) VALUES (2), (3), (4);

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


-- Reservas confirmadas (para testar pagamentos e avaliações)
INSERT INTO reserva (id_usuario, id_imovel, num_hospedes, data_inicio, data_fim, status) VALUES
(2, 1, 4, '2025-01-15', '2025-01-20', 'confirmada'),  -- Ana na Casa da Praia
(4, 2, 2, '2025-02-10', '2025-02-15', 'confirmada'),  -- Maria no Chalé
(5, 3, 1, '2025-03-01', '2025-03-05', 'confirmada'),  -- Pedro no Apartamento
(6, 4, 6, '2025-04-01', '2025-04-07', 'confirmada'),  -- Julia na Casa de Campo

-- Reservas pendentes (para testar status)
INSERT INTO reserva (id_usuario, id_imovel, num_hospedes, data_inicio, data_fim, status) VALUES
(3, 5, 2, '2025-05-10', '2025-05-15', 'pendente'),    -- João no Loft

-- Reservas futuras (para testar disponibilidade)
INSERT INTO reserva (id_usuario, id_imovel, num_hospedes, data_inicio, data_fim, status) VALUES
(2, 2, 3, '2025-08-20', '2025-08-25', 'confirmada'),  -- Ana no Chalé (futura)
(4, 1, 5, '2025-09-10', '2025-09-17', 'confirmada'),  -- Maria na Casa da Praia (futura)

-- Reservas canceladas (para testar cancelamentos, multas e estornos)
INSERT INTO reserva (id_usuario, id_imovel, num_hospedes, data_inicio, data_fim, status) VALUES
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
(1500.00, 'Pix', '2025-08-15'),                -- Reserva 6 (futura)
(2800.00, 'Cartão de crédito', '2025-09-05'),  -- Reserva 7 (futura)
(1600.00, 'Boleto', '2025-05-25'),             -- Reserva 8 (cancelada)
(450.00, 'Pix', '2025-06-25'),                 -- Reserva 9 (cancelada)
(1000.00, 'Cartão de crédito', '2025-07-25');  -- Reserva 10 (cancelada)

-- Relacionar pagamentos com reservas
INSERT INTO gera (id_pagamento, id_reserva) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

-- 4. PARCELAMENTOS (ALGUNS PAGAMENTOS À VISTA, OUTROS PARCELADOS)

-- Pagamento 1 - parcelado em 2x
INSERT INTO parcela (id_pagamento, num_parcelas, valor_parcela, data_vencimento) VALUES
(1, 1, 1000.00, '2025-01-10'),
(1, 2, 1000.00, '2025-02-10');

-- Pagamento 2 - à vista
INSERT INTO parcela (id_pagamento, num_parcelas, valor_parcela, data_vencimento) VALUES
(2, 1, 1500.00, '2025-02-05');

-- Pagamento 4 - parcelado em 3x
INSERT INTO parcela (id_pagamento, num_parcelas, valor_parcela, data_vencimento) VALUES
(4, 1, 583.33, '2025-03-25'),
(4, 2, 583.33, '2025-04-25'),
(4, 3, 583.34, '2025-05-25');


-- 5. SERVIÇOS EXTRAS CONTRATADOS

INSERT INTO servicos_vinculados (id_servico, id_reserva) VALUES
(1, 1), (2, 1), (3, 1),  -- Reserva 1: café, limpeza, transfer
(2, 2), (3, 2),          -- Reserva 2: limpeza, transfer
(1, 3), (4, 3),          -- Reserva 3: café, Wi-Fi premium
(1, 4), (2, 4),          -- Reserva 4: café, limpeza
(1, 5);                   -- Reserva 5: café

-- 6. CANCELAMENTOS E CONSEQUÊNCIAS

-- Cancelamento com política flexível (sem multa, estorno total)
INSERT INTO cancelamento (tipo_cancelamento, data_cancelamento) VALUES
('Voluntário pelo hóspede', '2025-05-20'),  -- Cancelamento da reserva 8
('Voluntário pelo hóspede', '2025-07-20');  -- Cancelamento da reserva 10

-- Cancelamento com política rígida (multa total, sem estorno)
INSERT INTO cancelamento (tipo_cancelamento, data_cancelamento) VALUES
('Voluntário pelo hóspede', '2025-06-25');  -- Cancelamento da reserva 9

-- Relacionar cancelamentos com pagamentos
INSERT INTO reserva_cancelada (id_cancelamento, id_pagamento) VALUES
(1, 8), (2, 10), (3, 9);

-- Estornos para cancelamentos com política flexível
INSERT INTO estorno (valor_estorno, data_estorno) VALUES
(1600.00, '2025-05-22'),  -- Estorno total da reserva 8
(1000.00, '2025-07-22');  -- Estorno total da reserva 10

INSERT INTO gera_estorno (id_estorno, id_cancelamento) VALUES
(1, 1), (2, 2);

-- Multa para cancelamento com política rígida
INSERT INTO multa (valor_multa) VALUES
(450.00);  -- Multa total da reserva 9

INSERT INTO gera_multa (id_multa, id_cancelamento) VALUES
(1, 3);

-- Pagamento da multa
INSERT INTO pagamento (valor_total, forma_pagamento, data_pagamento) VALUES
(450.00, 'Pix', '2025-06-26');

INSERT INTO gera_pag_multa (id_multa, id_pagamento) VALUES
(1, 11);

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


-- CONSULTAS SQL --

-- Consulta 1: Listar imóveis com Wi-Fi disponíveis entre datas específicas
SELECT i.* FROM imovel i
JOIN comodidades c ON i.id_imovel = c.id_imovel
WHERE c.comodidade = 'Wi-Fi'
AND i.id_imovel NOT IN (
  SELECT id_imovel FROM reserva
  WHERE status IN ('confirmada', 'pendente')
  AND ('2025-08-05' BETWEEN data_inicio AND data_fim OR
       '2025-08-10' BETWEEN data_inicio AND data_fim OR
       (data_inicio BETWEEN '2025-08-05' AND '2025-08-10'))
);

-- Consulta 2: Reservas feitas por um determinado hóspede
SELECT r.*, u.nome FROM reserva r
JOIN usuario u ON r.id_usuario = u.id_usuario
WHERE u.nome = 'Ana Souza';

-- Consulta 3: Imóveis com média de avaliação acima de 4
SELECT i.titulo, AVG(a.nota) as media_avaliacao
FROM imovel i
JOIN reserva r ON i.id_imovel = r.id_imovel
JOIN experiencia_avaliada ea ON r.id_reserva = ea.id_reserva
JOIN avaliacao a ON ea.id_avaliacao = a.id_avaliacao
GROUP BY i.titulo, i.id_imovel
HAVING AVG(a.nota) > 4;

-- Consulta 4: Pagamentos (principais e adicionais) por reserva
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
JOIN pagamento p ON gpm.id_pagamento = p.id_pagamento;

-- Consulta 5: Listar hóspedes que contrataram serviços extras
SELECT DISTINCT u.nome AS hospede, se.nome AS servico
FROM reserva r
JOIN servicos_vinculados sv ON r.id_reserva = sv.id_reserva
JOIN servico_extra se ON sv.id_servico = se.id_servico
JOIN usuario u ON r.id_usuario = u.id_usuario;

-- Consulta 6: Imóveis com mais comodidades
SELECT i.titulo, COUNT(c.comodidade) AS qtd_comodidades
FROM imovel i
JOIN comodidades c ON i.id_imovel = c.id_imovel
GROUP BY i.titulo, i.id_imovel
ORDER BY qtd_comodidades DESC;

-- Consulta 7: Reservas canceladas com multa aplicada
SELECT r.id_reserva, u.nome AS hospede, m.valor_multa
FROM reserva r
JOIN usuario u ON r.id_usuario = u.id_usuario
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN reserva_cancelada rc ON g.id_pagamento = rc.id_pagamento
JOIN gera_multa gm ON rc.id_cancelamento = gm.id_cancelamento
JOIN multa m ON gm.id_multa = m.id_multa
WHERE r.status = 'cancelada';

-- Consulta 8: Parcelas em aberto (com vencimento futuro)
SELECT p.id_pagamento, p.num_parcelas, p.valor_parcela, p.data_vencimento
FROM parcela p
WHERE p.data_vencimento > CURRENT_DATE;

-- Consulta 9: Total arrecadado por imóvel
SELECT i.titulo, SUM(p.valor_total) AS total_recebido
FROM imovel i
JOIN reserva r ON i.id_imovel = r.id_imovel
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN pagamento p ON g.id_pagamento = p.id_pagamento
WHERE r.status = 'confirmada'
GROUP BY i.titulo, i.id_imovel
ORDER BY total_recebido DESC;

-- Consulta 10: Hóspedes que mais reservaram imóveis
SELECT u.nome, COUNT(*) AS total_reservas
FROM usuario u
JOIN reserva r ON u.id_usuario = r.id_usuario
GROUP BY u.nome, u.id_usuario
ORDER BY total_reservas DESC;

-- Consulta 11: Verificar disponibilidade de imóvel em período específico
SELECT i.titulo, i.id_imovel
FROM imovel i
WHERE i.id_imovel NOT IN (
    SELECT r.id_imovel 
    FROM reserva r 
    WHERE r.status IN ('confirmada', 'pendente')
    AND (
        ('2025-08-01' BETWEEN r.data_inicio AND r.data_fim) OR
        ('2025-08-10' BETWEEN r.data_inicio AND r.data_fim) OR
        (r.data_inicio BETWEEN '2025-08-01' AND '2025-08-10')
    )
);

-- Consulta 12: Receita total por anfitrião (incluindo serviços extras)
SELECT u.nome AS anfitriao, 
       SUM(p.valor_total) AS receita_total
FROM usuario u
JOIN anfitriao a ON u.id_usuario = a.id_usuario
JOIN imovel i ON a.id_usuario = i.id_usuario
JOIN reserva r ON i.id_imovel = r.id_imovel
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN pagamento p ON g.id_pagamento = p.id_pagamento
WHERE r.status = 'confirmada'
GROUP BY u.nome
ORDER BY receita_total DESC;

-- Consulta 13: Cancelamentos por tipo de política
SELECT pc.tipo_politica, COUNT(*) AS total_cancelamentos
FROM politica_cancelamento pc
JOIN imovel i ON pc.id_politica = i.id_politica
JOIN reserva r ON i.id_imovel = r.id_imovel
WHERE r.status = 'cancelada'
GROUP BY pc.tipo_politica;

-- Consulta 14: Serviços extras mais contratados
SELECT se.nome, COUNT(*) AS vezes_contratado
FROM servico_extra se
JOIN servicos_vinculados sv ON se.id_servico = sv.id_servico
GROUP BY se.nome
ORDER BY vezes_contratado DESC;

-- Consulta 15: Parcelas em atraso
SELECT pp.id_pagamento, pp.num_parcelas, pp.valor_parcela, pp.data_vencimento
FROM parcela pp
WHERE pp.data_vencimento < CURRENT_DATE;

-- Consulta 16: Imóveis disponíveis por capacidade e cidade
SELECT i.titulo, i.capacidade_max, i.cidade, i.valor_diaria
FROM imovel i
WHERE i.capacidade_max >= 4 
AND i.cidade = 'São Paulo'
AND i.id_imovel NOT IN (
    SELECT r.id_imovel FROM reserva r 
    WHERE r.status IN ('confirmada', 'pendente')
    AND CURRENT_DATE BETWEEN r.data_inicio AND r.data_fim
);

-- Consulta 17: Histórico completo de um imóvel (reservas, cancelamentos, avaliações)
SELECT 
    i.titulo,
    r.id_reserva,
    u.nome as hospede,
    r.data_inicio,
    r.data_fim,
    r.status,
    a.nota,
    a.comentario,
    CASE 
        WHEN r.status = 'cancelada' THEN c.data_cancelamento
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
ORDER BY r.data_inicio;

-- Consulta 18: Receita mensal por anfitrião
SELECT 
    u.nome as anfitriao,
    EXTRACT(YEAR FROM p.data_pagamento) as ano,
    EXTRACT(MONTH FROM p.data_pagamento) as mes,
    SUM(p.valor_total) as receita_mensal
FROM usuario u
JOIN anfitriao a ON u.id_usuario = a.id_usuario
JOIN imovel i ON a.id_usuario = i.id_usuario
JOIN reserva r ON i.id_imovel = r.id_imovel
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN pagamento p ON g.id_pagamento = p.id_pagamento
WHERE r.status = 'confirmada'
GROUP BY u.nome, u.id_usuario, EXTRACT(YEAR FROM p.data_pagamento), EXTRACT(MONTH FROM p.data_pagamento)
ORDER BY ano DESC, mes DESC, receita_mensal DESC;

-- Consulta 19: Análise de estornos por política de cancelamento
SELECT 
    pc.tipo_politica,
    COUNT(*) as total_estornos,
    AVG(e.valor_estorno) as valor_medio_estorno,
    SUM(e.valor_estorno) as valor_total_estornos
FROM politica_cancelamento pc
JOIN imovel i ON pc.id_politica = i.id_politica
JOIN reserva r ON i.id_imovel = r.id_imovel
JOIN gera g ON r.id_reserva = g.id_reserva
JOIN reserva_cancelada rc ON g.id_pagamento = rc.id_pagamento
JOIN gera_estorno ge ON rc.id_cancelamento = ge.id_cancelamento
JOIN estorno e ON ge.id_estorno = e.id_estorno
GROUP BY pc.tipo_politica;

-- Consulta 20: Relatório de ocupação por imóvel
SELECT 
    i.titulo,
    COUNT(CASE WHEN r.status = 'confirmada' THEN 1 END) as reservas_confirmadas,
    COUNT(CASE WHEN r.status = 'cancelada' THEN 1 END) as reservas_canceladas,
    COUNT(CASE WHEN r.status = 'pendente' THEN 1 END) as reservas_pendentes,
    AVG(r.num_hospedes) as media_hospedes_por_reserva,
    SUM(CASE WHEN r.status = 'confirmada' THEN (r.data_fim - r.data_inicio) ELSE 0 END) as total_dias_ocupados
FROM imovel i
LEFT JOIN reserva r ON i.id_imovel = r.id_imovel
GROUP BY i.titulo, i.id_imovel
ORDER BY reservas_confirmadas DESC;
