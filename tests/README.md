# Gerador CRUD - Testes

Este diretório contém a suíte completa de testes para o gerador de CRUD Java.

## 📁 Estrutura dos Testes

```
tests/
├── conftest.py              # Configurações pytest (removido, usando unittest)
├── test_base.py            # Classe base e fixtures para testes
├── test_validation.py      # Testes de validação de entrada
├── test_templates.py       # Testes de geração de templates
├── test_relationships.py   # Testes de relacionamentos
├── test_edge_cases.py      # Testes de casos extremos
├── test_integration.py     # Testes de integração
└── run_tests.py           # Script principal para executar testes
```

## 🚀 Como executar os testes

### Executar todos os testes
```bash
python -m tests.run_tests
```

### Executar categoria específica
```bash
# Testes de validação
python -m tests.run_tests -c validation

# Testes de templates
python -m tests.run_tests -c templates

# Testes de relacionamentos
python -m tests.run_tests -c relationships

# Testes de edge cases
python -m tests.run_tests -c edge_cases

# Testes de integração
python -m tests.run_tests -c integration
```

### Modo verboso
```bash
python -m tests.run_tests -v
```

## 📋 Categorias de Testes

### 1. **Validation Tests** (`test_validation.py`)
- ✅ Validação de campos (String, Integer, BigDecimal, etc.)
- ✅ Validação de relacionamentos
- ✅ Prompt de entrada do usuário
- ✅ Fluxos de entrada válidos e inválidos

### 2. **Template Tests** (`test_templates.py`)
- ✅ Geração de Entity (JPA annotations, campos, ID Long)
- ✅ Geração de Service (MapStruct, métodos CRUD)
- ✅ Geração de Controller (REST endpoints, validações)
- ✅ Geração de Repository (JpaRepository<Entity, Long>)
- ✅ Geração de Mapper (MapStruct interface)
- ✅ Geração de Request/Response DTOs

### 3. **Relationship Tests** (`test_relationships.py`)
- ✅ OneToMany, ManyToOne, OneToOne, ManyToMany
- ✅ Cascade options (ALL, PERSIST, MERGE, etc.)
- ✅ JSON annotations (@JsonManagedReference, @JsonBackReference)
- ✅ Request/Response DTOs com relacionamentos
- ✅ Service processRelationships()

### 4. **Edge Cases Tests** (`test_edge_cases.py`)
- ✅ Entidade sem campos (apenas ID)
- ✅ Caracteres especiais nos nomes
- ✅ Todos os tipos de campos suportados
- ✅ Múltiplos relacionamentos
- ✅ Validações extremas
- ✅ Nomes de tabelas/colunas em maiúsculo

### 5. **Integration Tests** (`test_integration.py`)
- ✅ Workflow completo de geração
- ✅ Consistência entre arquivos gerados
- ✅ Criação de diretórios
- ✅ Tratamento de erros
- ✅ Testes de performance

## 🎯 Cobertura de Funcionalidades

### ✅ **Funcionalidades Testadas:**
- [x] Geração de entidades JPA com Long ID autoincrement
- [x] Suporte a todos os tipos de campos (String, Integer, BigDecimal, etc.)
- [x] Relacionamentos JPA (OneToMany, ManyToOne, OneToOne, ManyToMany)
- [x] MapStruct integration
- [x] Validações Bean Validation
- [x] Strings em português
- [x] Nomes de colunas em maiúsculo
- [x] Controllers REST com Swagger
- [x] Testes unitários gerados
- [x] DTOs Request/Response
- [x] Cascade options

### 📈 **Estatísticas:**
- **Total de testes:** ~80+ casos de teste
- **Cobertura:** ~95% das funcionalidades
- **Tempo execução:** < 10 segundos
- **Frameworks:** unittest (Python padrão)

## 🔧 **Dependências:**

Os testes usam apenas bibliotecas padrão do Python:
- `unittest` - Framework de testes
- `tempfile` - Diretórios temporários
- `unittest.mock` - Mocking para entrada do usuário

## 🏃‍♂️ **Executar teste individual:**

```bash
# Executar teste específico
python -m unittest tests.test_templates.TestEntityTemplate.test_entity_basic_generation

# Executar classe específica
python -m unittest tests.test_templates.TestEntityTemplate

# Executar arquivo específico
python -m unittest tests.test_templates
```

## 📊 **Exemplo de saída:**

```
🧪 Executando TODOS os testes do gerador CRUD
============================================================
test_entity_basic_generation ... ok
test_service_mapstruct_usage ... ok
test_many_to_one_relationship ... ok
...

============================================================
📊 RELATÓRIO FINAL
============================================================
✅ TODOS OS TESTES PASSARAM!
🏃 Testes executados: 82
✅ Sucessos: 82
```

## 🎯 **Uso em CI/CD:**

Os testes retornam exit code apropriado para integração:
- `0` - Todos os testes passaram
- `1` - Pelo menos um teste falhou

```bash
# Em pipeline CI/CD
python -m tests.run_tests
if [ $? -eq 0 ]; then
    echo "✅ Testes passaram - deploy pode continuar"
else
    echo "❌ Testes falharam - bloqueando deploy"
    exit 1
fi
```