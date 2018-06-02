CREATE DATABASE copadb;

CREATE TABLE pessoa (
  idpessoa int NOT NULL PRIMARY KEY ,
  nomepessoa varchar(30),
  nacionalidade varchar(30)
);

CREATE TABLE selecao (
  idselecao int NOT NULL PRIMARY KEY ,
  pais varchar(30)
);

CREATE TABLE cidade (
  nomecidade varchar(30) NOT NULL PRIMARY KEY ,
  fundacao timestamp
);

CREATE TABLE membro_selecao (
  idpessoa int NOT NULL PRIMARY KEY  REFERENCES pessoa (idpessoa),
  numeroparticipacoescopa int,
  idselecao int REFERENCES selecao (idselecao),
  funcaotecnica varchar(30),
  numerogols int,
  posicao varchar(20)
);

CREATE TABLE guia_voluntario (
  idpessoa int NOT NULL PRIMARY KEY  REFERENCES pessoa (idpessoa),
  disponibilidade boolean,
  nomecidade varchar(30) REFERENCES cidade (nomecidade)
);



CREATE TABLE tradutor (
  idpessoa int NOT NULL PRIMARY KEY  REFERENCES pessoa (idpessoa),
  disponibilidade boolean,
  idioma varchar(20),
  valorhora int
);


CREATE TABLE torcedor (
  idpessoa int NOT NULL PRIMARY KEY  REFERENCES pessoa (idpessoa),
  email varchar(30),
  senha varchar(30)
);

CREATE TABLE evento (
  codevento int NOT NULL PRIMARY KEY ,
  nomeevento varchar(40),
  dataevento timestamp,
  idademinima int,
  descricao varchar(248),
  nomecidade varchar(30) REFERENCES cidade (nomecidade)
);

CREATE TABLE hotel (
  codhotel int NOT NULL PRIMARY KEY ,
  nomehotel varchar(30),
  valordiaria int,
  disponivel boolean,
  nomecidade varchar(30) REFERENCES cidade (nomecidade)
);

CREATE TABLE partida (
  codpartida int NOT NULL PRIMARY KEY ,
  datapartida timestamp,
  valoringresso int,
  golselecao1 int,
  golselecao2 int,
  idselecao1 int REFERENCES selecao (idselecao),
  idselecao2 int REFERENCES selecao (idselecao),
  nomecidade varchar(30) REFERENCES cidade (nomecidade)
);



CREATE TABLE viagem (
  codviagem int NOT NULL PRIMARY KEY ,
  nomeorigem varchar(30) REFERENCES cidade (nomecidade),
  nomedestino varchar(30) REFERENCES cidade (nomecidade),
  meiotransporte varchar(30),
  dataviagem timestamp,
  precoviagem int
);




CREATE TABLE ajuda (
  idguia int REFERENCES pessoa (idpessoa),
  idtorcedor int REFERENCES pessoa (idpessoa),
  PRIMARY KEY  (idguia, idtorcedor)
);

CREATE TABLE contrata (
  idtradutor int NOT NULL REFERENCES pessoa (idpessoa),
  idtorcedor int NOT NULL REFERENCES pessoa (idpessoa),
  PRIMARY KEY (idtradutor, idtorcedor)
);

CREATE TABLE compraingresso (
  idpessoa int REFERENCES pessoa (idpessoa),
  codpartida int REFERENCES partida (codpartida),
  PRIMARY KEY (idpessoa, codpartida)
);

CREATE TABLE interesse (
  idpessoa int REFERENCES pessoa (idpessoa),
  codevento int REFERENCES evento (codevento),
  valorrating int,
  PRIMARY KEY (idpessoa, codevento)
);

