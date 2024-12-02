# Balerion API
#### API for task management with priority and status tracking.
___  

## Iniciando o projeto  

Abaixo estão os métodos para execução do serviço via Poetry ou Docker. O método recomendado é o Docker.  

- **Python**: Python 3.12  
- **Docker**: Docker version 27.2.0  
- **Docker Compose**: v2.29.2-desktop.2  

### Observação:  
- O arquivo `.env` foi incluído no repositório para facilitar os testes. **Não é uma boa prática**.  
___  

## Iniciando o projeto com Docker  

Certifique-se de estar no diretório raiz do projeto.  

Execute o comando abaixo para subir os serviços da API e do PostgreSQL:  
```bash  
docker-compose up -d  
```  

Os testes e o alembic irão executar automaticamente com o docker da api e algo semelhante deve aparecer:  
```bash  
balerion-api          | ============================= test session starts ==============================
balerion-api          | platform linux -- Python 3.12.7, pytest-8.3.3, pluggy-1.5.0
balerion-api          | rootdir: /src
balerion-api          | configfile: pyproject.toml
balerion-api          | plugins: asyncio-0.24.0, cov-6.0.0
balerion-api          | asyncio: mode=Mode.AUTO, default_loop_scope=function
balerion-api          | collected 6 items
balerion-api          |
balerion-api          | tests/src/services/tasks/unit/test_tasks_service.py ......               [100%]
balerion-api          |
balerion-api          | ---------- coverage: platform linux, python 3.12.7-final-0 -----------
balerion-api          | Name                             Stmts   Miss  Cover   Missing
balerion-api          | --------------------------------------------------------------
balerion-api          | src/services/__init__.py             0      0   100%
balerion-api          | src/services/tasks/__init__.py       0      0   100%
balerion-api          | src/services/tasks/service.py       27      0   100%
balerion-api          | --------------------------------------------------------------
balerion-api          | TOTAL                               27      0   100%
balerion-api          |
balerion-api          |
balerion-api          | ============================== 6 passed in 0.33s ===============================
balerion-api          | INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
balerion-api          | INFO  [alembic.runtime.migration] Will assume transactional DDL.
balerion-api          | INFO  [alembic.runtime.migration] Running upgrade  -> 77b55b2c0aa2, create tables
```  

Verifique se os serviços estão funcionando:  
```bash  
docker-compose ps  
```  

Você verá uma saída semelhante a:  
```bash  
NAME                IMAGE              SERVICE             CREATED             STATUS
balerion-api        balerion-api       api                2 minutes ago       Up 2 minutes        0.0.0.0:5000->5000/tcp
balerion-db         postgres:latest    db                 2 minutes ago       Up 2 minutes        0.0.0.0:5432->5432/tcp
```  
___  

## Iniciando o projeto com Poetry  

### Passo 1  
Instale o Poetry (https://python-poetry.org/docs/).  

### Passo 2  
Entre no diretório raiz do projeto e crie o ambiente virtual:  
```bash  
poetry shell  
```  

### Passo 3  
Instale as dependências:  
```bash  
poetry install  
```  

### Passo 4  
Suba o serviço do PostgreSQL necessário para persistência:  
```bash  
docker-compose up -d db  
```

### Passo 5  
Rode o alembic, para aplicar migration e criar tabelas:  
```bash  
alembic upgrade head
```

### Passo 6  
Inicie a aplicação:  
```bash  
python3 main.py  
```  

Você verá uma saída semelhante:  
```bash  
balerion-api          | Server is ready at URL 0.0.0.0:5000/caraxes-api
balerion-api          |                                                      _
balerion-api          |  _           _           _                               _
balerion-api          | | |__   __ _| | ___ _ __(_) ___  _ __         __ _ _ __ (_)
balerion-api          | | '_ \ / _` | |/ _ \ '__| |/ _ \| '_ \ _____ / _` | '_ \| |
balerion-api          | | |_) | (_| | |  __/ |  | | (_) | | | |_____| (_| | |_) | |
balerion-api          | |_.__/ \__,_|_|\___|_|  |_|\___/|_| |_|      \__,_| .__/|_|
balerion-api          |                                                   |_|
balerion-api          |
```  
___  

## Swagger - Documentação  

Acesse a documentação gera pelo swagger em:  
> [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)  
___  

## Padrão de Resposta  

Todas as respostas da API seguem um padrão consistente, garantindo uma fácil interpretação dos resultados e dos possíveis erros.  

### Estrutura de Resposta  

```json  
{  
  "success": true,  
  "internal_code": 0,  
  "message": "Operação realizada com sucesso",  
  "status_code": 200,  
  "payload": {  
    // Dados específicos da resposta  
  }  
}  
```  

### Descrição dos Campos  

- **success**: Indicador do resultado da operação (verdadeiro/falso)
- **internal_code**: Código interno para identificação de resposta/erro
- **message**: Mensagem explicativa sobre o resultado da operação
- **status_code**: Código HTTP padrão
- **payload**: Dados retornados pela operação

### Exemplo de Resposta de Sucesso  
```json  
{  
  "success": true,  
  "internal_code": 0,  
  "message": "New task has ben created",  
  "status_code": 201,  
  "payload": {  
    "id": 1  
  }  
}  
```  

### Exemplo de Resposta de Erro  
```json  
{  
  "success": false,  
  "internal_code": 40,  
  "message": "Task with id 5 not found",  
  "status_code": 404  
}
```

## Endpoints

#### 1. Criar Nova Tarefa
- **Rota**: `POST /balerion-api/v1/tasks`
- **Descrição**: Cria uma nova tarefa.

**Parâmetros do Corpo da Requisição**:
| Parâmetro    | Descrição           | Obrigatório | Exemplo          |
|--------------|---------------------|-------------|------------------|
| title        | Título da tarefa    | Sim         | "Nova Tarefa"    |
| description  | Descrição da tarefa | Não         | "Descrição"      |
| status       | Status da tarefa    | Sim         | "TODO"           |
| priority     | Prioridade          | Sim         | "HIGH"           |
| deadline     | Data limite         | Não         | "2024-12-31"     |

#### 2. Listar Tarefas Paginadas
- **Rota**: `GET /balerion-api/v1/tasks`
- **Descrição**: Lista tarefas com paginação.

**Parâmetros de Consulta**:
| Parâmetro | Descrição         | Obrigatório | Padrão |
|-----------|------------------|-------------|---------|
| limit     | Limite de itens  | Não         | 10      |
| offset    | Deslocamento     | Não         | 0       |

**Resposta**:
```json
{
  "success": true,
  "payload": {
    "tasks": [
      {
        "id": 1,
        "title": "Tarefa 1",
        "description": "Descrição da tarefa",
        "status": "TODO",
        "priority": "HIGH",
        "deadline": "2024-12-31"
      }
    ],
    "total": 1,
    "limit": 10,
    "offset": 0
  }
}
```

#### 3. Obter Tarefa Específica
- **Rota**: `GET /balerion-api/v1/tasks/{task_id}`
- **Descrição**: Retorna detalhes de uma tarefa específica.

**Parâmetros de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  
| task_id    | ID da tarefa    | Sim         | 1       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "payload": {  
    "id": 1,
    "title": "Task 1",  
    "status": "TODO", 
    "priority": "HIGH",
    "deadline": "2024-12-31"
  }  
}  
```  

#### 4. Atualizar Tarefa
- **Rota**: `PUT /balerion-api/v1/tasks/{task_id}`
- **Descrição**: Atualiza uma tarefa existente.

**Parâmetros de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  
| task_id    | ID da tarefa    | Sim         | 1       |  

**Parâmetros do corpo da requisição**:  
| Parâmetro | Descrição        | Obrigatório | Exemplo          |  
|-----------|------------------|-------------|------------------|  
| name      | Nome da tarefa   | Sim         | "Updated Task"   |  
| status    | Status da tarefa | Sim         | "IN_PROGRESS"    |  
| priority  | Prioridade       | Não         | "LOW"            |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "Task updated successfully",  
  "payload": {  
    "id": 1  
  }  
}  
```  

#### 5. Atualizar Status da Tarefa
- **Rota**: `PATCH /balerion-api/v1/tasks/{task_id}/status`
- **Descrição**: Atualiza apenas o status da tarefa.

**Parâmetros de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  
| task_id    | ID da tarefa    | Sim         | 1       |  

**Parâmetros do corpo da requisição**:  
| Parâmetro | Descrição       | Obrigatório | Exemplo          |  
|-----------|-----------------|-------------|------------------|  
| status    | Novo status     | Sim         | "DONE"           |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "Task status updated successfully"
}  
``` 

#### 6. Deletar Tarefa
- **Rota**: `DELETE /balerion-api/v1/tasks/{task_id}`
- **Descrição**: Remove uma tarefa existente.

**Parâmetros de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|
| task_id    | ID da tarefa    | Sim         | 1       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "Task deleted successfully"  
}  
```  

___  

## Códigos de Status HTTP

### Códigos de Sucesso
- **200 OK**: Requisição bem-sucedida
- **201 Created**: Recurso criado com sucesso

### Códigos de Erro
- **400 Bad Request**: Erro na sintaxe/semântica da requisição
- **422 Unprocessable Content**: Violação de regra de negócio
- **500 Internal Server Error**: Erro inesperado no servidor
