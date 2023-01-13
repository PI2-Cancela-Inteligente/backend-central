-- CREATE DATABASE IF NOT EXISTS canintel;

\c canintel

CREATE SCHEMA IF NOT EXISTS "public";

CREATE TABLE "public"."usuario" (
    "id_usuario" BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY(START 1),
    "email" VARCHAR(100) NOT NULL,
    "senha" VARCHAR(500) NOT NULL,
    CONSTRAINT "PK_Usuario" PRIMARY KEY ("id_usuario"),
    CONSTRAINT "UQ_email" UNIQUE ("email")
);

CREATE TABLE "public"."admin" (
    "id_admin" BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY(START 1),
    "id_usuario" BIGINT NOT NULL,
    PRIMARY KEY ("id_admin", "id_usuario"),
    CONSTRAINT "FK_usuario_admin" FOREIGN KEY ("id_usuario") 
    REFERENCES "public"."usuario" ("id_usuario") 
    ON DELETE CASCADE
);

CREATE TABLE "public"."motorista" (
    "telefone" VARCHAR(20) NOT NULL,
    "cpf" VARCHAR(15) NOT NULL,
    "nome" VARCHAR(200) NOT NULL,
    "id_usuario" BIGINT NOT NULL,
    "matricula" VARCHAR(50),
    CONSTRAINT "PK_motorista" PRIMARY KEY ("cpf", "id_usuario"),
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
    "motorista_cpf" VARCHAR(15) NOT NULL,
    "usuario_id" BIGINT NOT NULL,
    CONSTRAINT "PK_carro" PRIMARY KEY ("placa"),
    CONSTRAINT "FK_motorista_caro" FOREIGN KEY ("motorista_cpf", "usuario_id")
    REFERENCES "public"."motorista" ("cpf", "id_usuario")
    ON DELETE RESTRICT
);

CREATE TABLE "public"."estaciona" (
    "placa" VARCHAR(50),
    "entrada" timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "saida" timestamp(6) with time zone,
    CONSTRAINT "PK_estaciona" PRIMARY KEY ("placa", "entrada"),
    CONSTRAINT "FK_carro_estaciona" FOREIGN KEY ("placa")
    REFERENCES "public"."carro" ("placa")
    ON DELETE SET NULL
);