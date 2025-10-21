# GGV-AUTO-CRUD

## 🚀 Descrição

O **GGV-AUTO-CRUD** é um gerador automático de código CRUD (Create, Read, Update, Delete) para aplicações Java Spring Boot com JPA/Hibernate. Este projeto utiliza templates Jinja2 para gerar automaticamente todas as camadas de uma aplicação (Entity, Repository, Service, Controller, DTOs, Mappers e testes) com suporte completo a relacionamentos entre entidades.

## ✨ Funcionalidades

- ✅ **Geração automática de entidades JPA** com IDs Long autoincrementais
- ✅ **Suporte completo a relacionamentos** (OneToMany, ManyToOne, OneToOne, ManyToMany)
- ✅ **Integração MapStruct** para mapeamento profissional entre DTOs e entidades
- ✅ **DTOs de Request e Response** com validações Bean Validation
- ✅ **Services** com mapeamento automático MapStruct
- ✅ **Controllers REST** com documentação Swagger/OpenAPI
- ✅ **Testes unitários completos** (54 testes) para todas as camadas
- ✅ **Configurações avançadas** de cascade, not_null e relacionamentos
- ✅ **Validação de entrada** com formato colon-separated
- ✅ **Suporte a BigDecimal** com precisão e validações específicas
- ✅ **Nomes de tabela personalizados** e colunas em maiúsculo
- ✅ **Localização completa em português** (mensagens de erro, comentários, strings)
- ✅ **Suporte a UUID** para referências de relacionamentos
- ✅ **Suite de testes abrangente** com cobertura completa

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Jinja2** para templates
- **Java 17+** (código gerado)
- **Spring Boot 3.x** (código gerado)
- **Jakarta Persistence (JPA)**
- **MapStruct** para mapeamento de objetos
- **Lombok**
- **Bean Validation**
- **Swagger/OpenAPI**
- **JUnit 5** e **Mockito** (testes gerados)

## 📦 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd ggv-auto-crud
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### Execução Básica

```bash
python main.py
```

### Configuração de Campos

O sistema suporta os seguintes tipos de campos usando formato colon-separated:

```
nome:String:100              # String com tamanho máximo
idade:Integer::positive      # Integer com validação positiva
preco:BigDecimal::positive   # BigDecimal com validação positiva e precisão
percentual:Double::positive  # Double com validação positiva
ativo:Boolean               # Boolean simples
nascimento:LocalDate        # Data
criacao:LocalDateTime       # Data e hora
codigo:UUID                 # Identificador único
valor:Long                  # Números inteiros grandes
custo:Float                 # Números decimais simples
```

**Formato:** `nome:tipo[:tamanho][:opcoes]`

**Tipos suportados:**
- String, Integer, Long, Double, Float, Boolean
- LocalDateTime, LocalDate, UUID, BigDecimal

**Opções especiais:**
- `positive`: Adiciona validação `@Positive` para números
- Para BigDecimal: Adiciona `@DecimalMin` e `@Digits(integer=19, fraction=2)`

### Configuração de Relacionamentos

**Formato:** `nome:tipo:target[:mapped_by][:opcoes]`

#### OneToMany (Um para Muitos)
```
pedidos:OneToMany:Pedido:cliente:cascade
```

#### ManyToOne (Muitos para Um)
```
categoria:ManyToOne:Categoria::not_null
```

#### OneToOne (Um para Um)
```
endereco:OneToOne:Endereco::cascade
```

#### ManyToMany (Muitos para Muitos)
```
tags:ManyToMany:Tag::cascade
```

**Opções disponíveis:**
- `cascade`: Operações em cascata
- `not_null`: Campo obrigatório (adiciona `@NotNull`)

### Funcionalidades do MapStruct

O gerador agora inclui interfaces MapStruct profissionais:

- **Mapeamento Entity ↔ Request**: Conversão bidirecional automática
- **Mapeamento Entity → Response**: Com summary objects para relacionamentos
- **Métodos personalizados**: Para objetos relacionados complexos
- **Ignoring de relacionamentos**: Para evitar lazy loading issues
- **Update methods**: Para atualizar entidades existentes a partir de requests
## 📁 Estrutura dos Arquivos Gerados

Para uma entidade `Cliente`, o sistema gera:

```
output/Cliente/
├── Cliente.java              # Entidade JPA com IDs Long e relacionamentos
├── ClienteRepository.java    # Interface Repository
├── ClienteRequest.java       # DTO de entrada com validações
├── ClienteResponse.java      # DTO de saída
├── ClienteMapper.java        # Interface MapStruct para conversões
├── ClienteService.java       # Lógica de negócios com MapStruct
├── ClienteController.java    # Endpoints REST com Swagger
├── ClienteServiceTest.java   # Testes do Service (Mockito)
└── ClienteControllerTest.java # Testes do Controller (MockMvc)
```

## 🧪 Suite de Testes

O projeto inclui **54 testes unitários** organizados em categorias:

### Estrutura de Testes
```
tests/
├── test_validation.py      # Testes de validação de entrada (10 testes)
├── test_templates.py       # Testes de geração de templates (13 testes)
├── test_relationships.py   # Testes de relacionamentos JPA (12 testes)
├── test_edge_cases.py      # Testes de casos extremos (11 testes)
├── test_integration.py     # Testes de integração completa (8 testes)
├── test_base.py           # Classe base para testes
└── conftest.py            # Configurações do pytest
```

### Executar Testes
```bash
# Instalar pytest
pip install pytest

# Executar todos os testes
python -m pytest tests/ -v

# Executar categoria específica
python -m pytest tests/test_templates.py -v
```

**Cobertura dos Testes:**
- ✅ Validação de entrada de campos e relacionamentos
- ✅ Geração correta de todos os templates
- ✅ Relacionamentos JPA (OneToMany, ManyToOne, OneToOne, ManyToMany)
- ✅ Casos extremos e validações especiais
- ✅ Workflow completo de geração de arquivos
- ✅ MapStruct integration
- ✅ Localização em português

## 🔧 Configuração

### config.py
```python
PACKAGE_BASE = "com.erp"        # Pacote base da aplicação
OUTPUT_DIR = "output"           # Diretório de saída
TEMPLATE_DIR = "templates"      # Diretório dos templates
```

## 💡 Exemplos de Uso

## 💡 Exemplos de Uso

### Exemplo 1: Entidade Simples
```
📝 Nome da entidade: Produto
�️  Nome da tabela: TB_PRODUTOS
�🔧 Campos:
   nome:String:100
   preco:BigDecimal::positive
   ativo:Boolean

✅ Sem relacionamentos
```

### Exemplo 2: Entidade com Relacionamentos
```
📝 Nome da entidade: Pedido
🗃️  Nome da tabela: TB_PEDIDOS
🔧 Campos:
   numero:String:50
   total:BigDecimal::positive
   data:LocalDateTime

🔗 Relacionamentos:
   cliente:ManyToOne:Cliente::not_null
   itens:OneToMany:ItemPedido:pedido:cascade
```

**Resultado gerado:**
- **ID Long autoincremental** em todas as entidades
- **Tabela**: `TB_PEDIDOS` com colunas `NUMERO`, `TOTAL`, `DATA`, `CLIENTE_ID`
- **MapStruct Mapper** com conversões automáticas
- **Request DTO** com `UUID clienteId` e `List<UUID> itensIds`
- **Service** com métodos que usam MapStruct
- **Validações**: `@NotNull` no relacionamento cliente
- **Testes completos** para todas as camadas

## 🎨 Funcionalidades dos Templates

### Entity (Cliente.java)
- ✅ **ID Long** com `@GeneratedValue(strategy = GenerationType.IDENTITY)`
- ✅ Anotações JPA otimizadas e relacionamentos
- ✅ Lombok para redução de boilerplate
- ✅ Controle de serialização JSON com Jackson
- ✅ **Colunas em maiúsculo** automaticamente

### Mapper (ClienteMapper.java) - **NOVIDADE MapStruct**
- ✅ **Interface MapStruct** com `@Mapper(componentModel = "spring")`
- ✅ Conversões automáticas `Entity ↔ Request`
- ✅ Conversões `Entity → Response` com summary objects
- ✅ **Métodos customizados** para relacionamentos complexos
- ✅ **Ignore de relacionamentos** para evitar lazy loading

### Request DTO (ClienteRequest.java)
- ✅ **Record classes** para imutabilidade
- ✅ Validações Bean Validation automáticas
- ✅ **UUID para relacionamentos** (`clienteId`, `itensIds`)
- ✅ **@NotNull** em relacionamentos obrigatórios

### Service (ClienteService.java)
- ✅ **Injeção automática do Mapper** MapStruct
- ✅ Métodos CRUD que usam `mapper.toEntity()` e `mapper.toResponse()`
- ✅ **Processamento de relacionamentos** automático
- ✅ **Mensagens de erro em português**
- ✅ Transações otimizadas

### Controller (ClienteController.java)
- ✅ **Endpoints REST** com `@PathVariable` Long
- ✅ **Documentação Swagger/OpenAPI** completa
- ✅ **Response Status** apropriados (201, 204, etc.)
- ✅ **Strings em português** (descrições, summaries)

## 🧪 Testes

### Testes Gerados
Os arquivos de teste incluem:

- **ServiceTest**: Testa lógica de negócios com Mockito
- **ControllerTest**: Testa endpoints REST com MockMvc
- Cobertura de cenários CRUD básicos
- Mocks apropriados para dependências

### Suite de Testes do Projeto
Execute a suite completa de 54 testes:

```bash
python -m pytest tests/ -v
```

## 🆕 Principais Melhorias Implementadas

### ✅ MapStruct Integration
- **Interfaces MapStruct** profissionais em vez de conversões manuais
- **Mapeamento automático** entre DTOs e entidades
- **Métodos customizados** para relacionamentos complexos
- **Performance otimizada** com geração de código em compile-time

### ✅ IDs Long Autoincrementais
- **Todas as entidades** usam `Long id` com `@GeneratedValue`
- **Path variables** em controllers usam `Long` 
- **Referências de relacionamento** usam `UUID` nos DTOs

### ✅ Localização Portuguesa Completa
- **Mensagens de erro** em português
- **Comentários de código** em português
- **Documentação Swagger** em português
- **Strings de interface** em português

### ✅ Relacionamentos Avançados
- Suporte completo aos 4 tipos de relacionamento JPA
- **Configurações de cascade** automáticas
- **Validação @NotNull** para relacionamentos obrigatórios
- **Summary objects** para evitar problemas de serialização

### ✅ Validações Bean Validation
- **@NotNull** automático em relacionamentos obrigatórios
- **@Positive** para campos numéricos positivos
- **@DecimalMin e @Digits** para BigDecimal
- **@Size** para campos String com tamanho

### ✅ Interface de Usuário Melhorada
- **Formato colon-separated** mais eficiente
- **Validação de entrada** robusta
- **Feedback visual** com emojis e cores
- **Resumo antes da geração** com confirmação

## 🔧 Dependências do Projeto Gerado

O código gerado requer as seguintes dependências no `pom.xml`:

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
        <groupId>org.mapstruct</groupId>
        <artifactId>mapstruct</artifactId>
        <version>1.5.5.Final</version>
    </dependency>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
    <dependency>
        <groupId>org.springdoc</groupId>
        <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
        <version>2.2.0</version>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <annotationProcessorPaths>
                    <path>
                        <groupId>org.mapstruct</groupId>
                        <artifactId>mapstruct-processor</artifactId>
                        <version>1.5.5.Final</version>
                    </path>
                    <path>
                        <groupId>org.projectlombok</groupId>
                        <artifactId>lombok</artifactId>
                        <version>${lombok.version}</version>
                    </path>
                </annotationProcessorPaths>
            </configuration>
        </plugin>
    </plugins>
</build>
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request
