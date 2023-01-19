-- CREATE DATABASE canintel;

\c canintel

CREATE SCHEMA IF NOT EXISTS "public";

CREATE TABLE "public"."usuario" (
    "id_usuario" BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY(START 1),
    "email" VARCHAR(100) NOT NULL,
    "senha" VARCHAR(500) NOT NULL,
    "is_admin" BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT "PK_Usuario" PRIMARY KEY ("id_usuario"),
    CONSTRAINT "UQ_email" UNIQUE ("email")
);

CREATE TABLE "public"."motorista" (
    "telefone" VARCHAR(20),
    "cpf" VARCHAR(15) NOT NULL,
    "nome" VARCHAR(200) NOT NULL,
    "id_usuario" BIGINT NOT NULL,
    "matricula" VARCHAR(50),
    CONSTRAINT "PK_motorista" PRIMARY KEY ("cpf"),
    CONSTRAINT "UQ_matricula" UNIQUE ("matricula"),
    CONSTRAINT "FK_usuario_motorista" FOREIGN KEY ("id_usuario") 
    REFERENCES "public"."usuario" ("id_usuario") 
    ON DELETE CASCADE
);

CREATE TABLE "public"."carro" (
    "placa" VARCHAR(50) NOT NULL,
    "cor" VARCHAR(50) NOT NULL,
    "modelo" VARCHAR(50) NOT NULL,
    "marca" VARCHAR(50) NOT NULL,
    "cpf" VARCHAR(15) NOT NULL,
    CONSTRAINT "PK_carro" PRIMARY KEY ("placa"),
    CONSTRAINT "FK_motorista_carro" FOREIGN KEY ("cpf")
    REFERENCES "public"."motorista" ("cpf")
    ON DELETE RESTRICT
);

CREATE TABLE "public"."estaciona" (
    "placa" VARCHAR(50) NOT NULL,
    "entrada" timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "saida" timestamp(6) with time zone,
    CONSTRAINT "PK_estaciona" PRIMARY KEY ("placa", "entrada"),
    CONSTRAINT "FK_carro_estaciona" FOREIGN KEY ("placa")
    REFERENCES "public"."carro" ("placa")
    ON DELETE CASCADE
);

-- Cria usuário admin 
INSERT INTO public.usuario (email,senha,is_admin)
	VALUES ('bigode@mail.com','123456',true),
    ('rodoupho@mail.com','123456',false);

-- Cria usuário motorista
INSERT INTO public.motorista (telefone,cpf,nome,id_usuario,matricula) VALUES 
('61 35520281','11111111111','Bigode',1,'180106970'),
('61 3333441','22222222222','Rodoupho',2,'180106971');

-- Cria carro
-- Auto-generated SQL script #202301181036
INSERT INTO public.carro (placa,cor,modelo,marca,cpf) VALUES 
('RFS0D21','Branca','Kwid','Renault','11111111111'),
('KEE0987','Branca','Gol','Volkswagen','22222222222');

-- Cria estacionamento
-- Auto-generated SQL script #202301181036
INSERT INTO public.estaciona (placa,entrada,saida)
    VALUES 
    ('RFS0D21','2021-01-18 10:36:00.000000','2021-01-18 11:36:00.000000'),
    ('RFS0D21','2021-01-18 12:36:00.000000','2021-01-18 13:36:00.000000'),
    ('RFS0D21','2021-01-18 14:36:00.000000','2021-01-18 15:36:00.000000'),
    ('RFS0D21','2021-01-18 16:36:00.000000','2021-01-18 17:36:00.000000'),
    ('KEE0987','2021-01-18 10:36:00.000000','2021-01-18 11:36:00.000000'),
    ('KEE0987','2021-01-18 12:36:00.000000','2021-01-18 13:36:00.000000'),
    ('KEE0987','2021-01-18 14:36:00.000000','2021-01-18 15:36:00.000000'),
    ('KEE0987','2021-01-18 16:36:00.000000','2021-01-18 17:36:00.000000');
