INSERT INTO pessoa (idpessoa, nomepessoa, nacionalidade) VALUES (1, 'Andrew Chuang', 'Brasil');
INSERT INTO pessoa (idpessoa, nomepessoa, nacionalidade) VALUES (2, 'João Silva', 'Brasil');
INSERT INTO pessoa (idpessoa, nomepessoa, nacionalidade) VALUES (3, 'Balalaika', 'Russia');

INSERT INTO selecao (idselecao, pais) VALUES (1, 'Brasil');
INSERT INTO selecao (idselecao, pais) VALUES (2, 'Argentina');
INSERT INTO selecao (idselecao, pais) VALUES (3, 'Portugal');
INSERT INTO selecao (idselecao, pais) VALUES  (4, 'Alemanha');


--Trecho colocado para teste com o login Comente depois
-- Notar que a chave idpessoa de pessoa deve ser igual idpessoa de Torcedor
INSERT INTO pessoa (idpessoa,nomepessoa,nacionalidade) values (4,'Ronaldo de Nazare','Brasil');
INSERT INTO torcedor (idpessoa, email, senha) VALUES (4 , 'RONALDO@hotmail.com', 'EHNOIS');
INSERT INTO cidade (nomecidade,fundacao) values ('moscow', to_timestamp(1530406862) );
INSERT INTO partida(codpartida, datapartida, valoringresso,golselecao1, golselecao2, idselecao1, idselecao2, nomecidade ) VALUES (1,to_timestamp(1530406862) ,100,0,0,1,2,'moscow');
INSERT INTO partida(codpartida, datapartida, valoringresso,golselecao1, golselecao2, idselecao1, idselecao2, nomecidade ) VALUES (2,to_timestamp(1530406862) ,100,0,0,3,2,'moscow');
INSERT INTO guia_voluntario(idpessoa,disponibilidade,nomecidade) VALUES (1,TRUE,'moscow');
INSERT INTO tradutor(idpessoa,disponibilidade,idioma,valorhora) VALUES (1,TRUE,'ENGLISH',12);
INSERT INTO evento(codevento,nomeevento,dataevento,idademinima,descricao,nomecidade)	VALUES (1,'TESTE',to_timestamp(1530406862),12,NULL,'moscow');
INSERT INTO evento(codevento,nomeevento,dataevento,idademinima,descricao,nomecidade)	VALUES (2,'TESTE2',to_timestamp(153040622),12,NULL,'moscow');
INSERT INTO evento(codevento,nomeevento,dataevento,idademinima,descricao,nomecidade)	VALUES (3,'TESTE3',to_timestamp(1530406700),12,NULL,'moscow');
