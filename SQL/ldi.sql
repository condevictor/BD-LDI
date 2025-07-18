CREATE TABLE usuario( 
	id_usuario INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	nome VARCHAR(255) NOT NULL,
	email VARCHAR(255) UNIQUE NOT NULL,
	senha VARCHAR(255) NOT NULL
);

CREATE TABLE anfitriao(
	id_usuario INT PRIMARY KEY,
	CONSTRAINT fk_usuario_anfitriao FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE hospede(
	id_usuario INT PRIMARY KEY,
	CONSTRAINT fk_usuario_anfitriao FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE telefone_usuario(
	telefone VARCHAR(30) NOT NULL,
	id_usuario INT NOT NULL,
	PRIMARY KEY(telefone, id_usuario),
	CONSTRAINT fk_usuario_telefone FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE avaliacao(
	id_avaliacao INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	nota INT NOT NULL,
	comentario TEXT,
	data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE enum_forma_pagamento AS ENUM(
	'Cartão de crédito',
	'Pix',
	'Boleto',
	'Transferência Bancária',
	'Dinheiro'
);

CREATE TABLE pagamento(
	id_pagamento INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	valor_total NUMERIC(15, 2) NOT NULL,
	forma_pagamento enum_forma_pagamento NOT NULL,
	data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE multa(
	id_multa INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	valor_multa NUMERIC(15,2) NOT NULL
);

CREATE TABLE servico_extra(
	id_servico INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	nome VARCHAR(255) NOT NULL,
	descricao TEXT,
	valor_servico NUMERIC(15,2) NOT NULL
);

CREATE TABLE estorno(
	id_estorno INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	valor_estorno NUMERIC(15,2) NOT NULL,
	data_estorno TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cancelamento(
	id_cancelamento INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	tipo_cancelamento VARCHAR(255),
	data_cancelamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

