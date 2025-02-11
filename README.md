# MAIA

Esse projeto foi desenvovido como teste técnico para a MAIA
 

## Como rodar

O script principal se encontra em `src/maia` para devida execução é necessário configurar o arquivo .env com as variáveis de ambiente necessárias para conexão com o banco de dados.

O projeto foi concebido com o gerenciador de dependências poetry, para rodar com ele siga os seguintes comandos:

```BASH
    poetry install
```
```BASH
    poetry RUN python src/maia/populate_new_data.py
```

### Alternativa para banco de dados
Assumindo que você tem o Docker instalado na sua máquina/ambiente, rodar na raiz do projeto o comando:


```Bash
    docker-compose build --no-cache
```

```Bash
    docker-compose up -d
```
```BASH
    poetry install
```
```BASH
    poetry RUN python src/maia/populate_new_data.py
```

### usando gitpod
cole a url no navegador e o ambiente será configurado.
 `https://gitpod.io/new/#https://github.com/IamNatri/MAIA`



## Considerações
- Caso número de conexões, frequência e volumetria de dados altos, avaliar utilização de pool de conexões.
- Evitar dados duplicados na GCP
    - O fluxo de sync dos dados pode levar a enviar informações já existentes na GCP em caso de falha/indisponibilidade do banco de dados local. Podemos evitar tal situação configurando a GCP para aceitar dados únicos do id_leitura.
