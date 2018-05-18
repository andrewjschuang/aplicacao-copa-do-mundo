# MC536 - Projeto de aplicação de suporte ao público da Copa do Mundo

## Como criar o banco de dados

### Instalar Postgres  
`sudo apt-get install postgresql`

### Logar como usuário postgres  
`sudo su - postgres`

### Criar e acessar banco de dados  
`createdb mydb`  
`psql mydb`

### Popular esquemas  
`\i script.sql`

### Popular tuplas  
`\i fill_database.sql`

##### Aqui dá pra usar os comandos sql  
`SELECT * FROM pessoa;`

##### Para ver as tabelas  
`\dt `

##### Para ver os esquemas de cada tabela  
`\d pessoa`

### Permitir acesso ao usuário x  
`GRANT ALL PRIVILEGES ON DATABASE mydb TO x;`  
`GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO x;`  
`\q`

## Como rodar o servidor
Faça os passos dentro do diretório do projeto depois de ter criado um banco de dados com os esquemas e tuplas.

### Modificar na linha 6 do server.py  
```database.init(dbname='nomedobd', user='seuusuario')```

### Instalar virtualenv  
`pip install virtualenv`

### Criar uma virtual environment no diretorio do projeto  
`python -m virtualenv venv`

### Ativar virtualenv  
`source venv/bin/activate`

### Instalar módulos do python  
`pip install -r requirements.txt`

### Rodar o server  
`python server.py`

### Acessar pela web  
`http://localhost:5000`
