# GGV-AUTO-CRUD

## 🚀 Descrição

O **GGV-AUTO-CRUD** é um gerador automático de código CRUD (Create, Read, Update, Delete) para aplicações Java Spring Boot com JPA/Hibernate. Este projeto utiliza templates Jinja2 para gerar automaticamente todas as camadas de uma aplicação (Entity, Repository, Service, Controller, DTOs e testes) com suporte completo a relacionamentos entre entidades.

## ✨ Funcionalidades

- ✅ **Geração automática de entidades JPA** com anotações otimizadas
- ✅ **Suporte completo a relacionamentos** (OneToMany, ManyToOne, OneToOne, ManyToMany)
- ✅ **DTOs de Request e Response** com validações
- ✅ **Services** com métodos de conversão automática
- ✅ **Controllers REST** com documentação Swagger/OpenAPI
- ✅ **Testes unitários** para Service e Controller
- ✅ **Configurações avançadas** de cascade, fetch type e outros
- ✅ **Validação de entrada** com feedback detalhado
- ✅ **Suporte a BigDecimal** com precisão e validações específicas
- ✅ **Nomes de tabela personalizados** e colunas em maiúsculo
- ✅ **Exception handling** com classes de exceção específicas

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Jinja2** para templates
- **Java 17+** (código gerado)
- **Spring Boot 3.x** (código gerado)
- **Jakarta Persistence (JPA)**
- **Lombok**
- **Bean Validation**
- **Swagger/OpenAPI**

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

O sistema suporta os seguintes tipos de campos:

```
nome:String:100              # String com tamanho máximo
idade:Integer::positive      # Integer com validação positiva
preco:BigDecimal::positive   # BigDecimal com validação positiva e precisão
percentual:Double::positive  # Double com validação positiva
ativo:Boolean               # Boolean simples
nascimento:LocalDate        # Data
criacao:LocalDateTime       # Data e hora
codigo:UUID                 # Identificador único
```

**Novidades:**
- ✅ **BigDecimal**: Suporte completo com validações `@DecimalMin` e `@Digits`
- ✅ **Nome da tabela personalizado**: Solicita nome da tabela após o nome da entidade
- ✅ **Colunas em maiúsculo**: Todos os nomes de colunas são automaticamente convertidos para maiúsculo

### Configuração de Relacionamentos

#### OneToMany (Um para Muitos)
```
pedidos:OneToMany:Pedido:cliente:cascade
```
- **pedidos**: nome do campo na entidade
- **OneToMany**: tipo do relacionamento
- **Pedido**: entidade relacionada
- **cliente**: campo na entidade relacionada (mapped by)
- **cascade**: operações em cascata

#### ManyToOne (Muitos para Um)
```
categoria:ManyToOne:Categoria::not_null
```
- **categoria**: nome do campo
- **ManyToOne**: tipo do relacionamento
- **Categoria**: entidade relacionada
- **not_null**: campo obrigatório

#### OneToOne (Um para Um)
```
endereco:OneToOne:Endereco::cascade,owner
```
- **endereco**: nome do campo
- **OneToOne**: tipo do relacionamento
- **Endereco**: entidade relacionada
- **cascade,owner**: operações em cascata e proprietário do relacionamento

#### ManyToMany (Muitos para Muitos)
```
tags:ManyToMany:Tag::cascade,inverse_field=posts
```
- **tags**: nome do campo
- **ManyToMany**: tipo do relacionamento
- **Tag**: entidade relacionada
- **cascade**: operações em cascata
- **inverse_field=posts**: campo na entidade relacionada

### Opções Avançadas

| Opção | Descrição | Uso |
|-------|-----------|-----|
| `cascade` | Operações em cascata | `categoria:ManyToOne:Categoria::cascade` |
| `not_null` | Campo obrigatório | `categoria:ManyToOne:Categoria::not_null` |
| `owner` | Proprietário do relacionamento | `endereco:OneToOne:Endereco::owner` |
| `inverse_field` | Campo inverso em ManyToMany | `tags:ManyToMany:Tag::inverse_field=posts` |
| `positive` | Validação numérica positiva | `idade:Integer::positive` |

## 📁 Estrutura dos Arquivos Gerados

Para uma entidade `Cliente`, o sistema gera:

```
output/Cliente/
├── Cliente.java              # Entidade JPA
├── ClienteRepository.java    # Interface Repository
├── ClienteRequest.java       # DTO de entrada
├── ClienteResponse.java      # DTO de saída
├── ClienteService.java       # Lógica de negócios
├── ClienteController.java    # Endpoints REST
├── ClienteServiceTest.java   # Testes do Service
└── ClienteControllerTest.java # Testes do Controller
```

## 🔧 Configuração

### config.py
```python
PACKAGE_BASE = "com.erp"        # Pacote base da aplicação
OUTPUT_DIR = "output"           # Diretório de saída
TEMPLATE_DIR = "templates"      # Diretório dos templates
```

## 💡 Exemplos de Uso

### Exemplo 1: Entidade Simples
```
📝 Nome da entidade: Produto
🔧 Campos:
   nome:String:100
   preco:Double::positive
   ativo:Boolean

✅ Sem relacionamentos
```

### Exemplo 2: Entidade com BigDecimal e Relacionamentos
```
📝 Nome da entidade: Produto
🗃️  Nome da tabela: TB_PRODUTOS
🔧 Campos:
   nome:String:100
   preco:BigDecimal::positive
   categoria:String:50
   ativo:Boolean

🔗 Relacionamentos:
   fornecedor:ManyToOne:Fornecedor::not_null
   avaliacoes:OneToMany:Avaliacao:produto:cascade
```

**Resultado:**
- Tabela: `TB_PRODUTOS`
- Colunas: `NOME`, `PRECO`, `CATEGORIA`, `ATIVO`, `FORNECEDOR_ID`
- BigDecimal com precisão: `@Column(precision=19, scale=2)`
- Validações: `@DecimalMin`, `@Digits`, `@Positive`

### Exemplo 3: Sistema Completo
```
📝 Nome da entidade: Pedido
🔧 Campos:
   numero:String:50
   total:Double::positive
   data:LocalDateTime

🔗 Relacionamentos:
   cliente:ManyToOne:Cliente::not_null
   itens:OneToMany:ItemPedido:pedido:cascade
   tags:ManyToMany:Tag::inverse_field=pedidos
```

## 🎨 Funcionalidades dos Templates

### Entity (Cliente.java)
- ✅ Anotações JPA otimizadas
- ✅ Lombok para redução de boilerplate
- ✅ Relacionamentos com configurações apropriadas
- ✅ Métodos auxiliares para relacionamentos
- ✅ Controle de serialização JSON
- ✅ Timestamps automáticos

### Request DTO (ClienteRequest.java)
- ✅ Validações Bean Validation
- ✅ Record classes para imutabilidade
- ✅ Campos para IDs de relacionamentos

### Response DTO (ClienteResponse.java)
- ✅ DTOs aninhados para relacionamentos
- ✅ Factory methods para conversão
- ✅ Métodos summary para referências

### Service (ClienteService.java)
- ✅ Métodos CRUD completos
- ✅ Conversão automática Request ↔ Entity
- ✅ Tratamento de relacionamentos
- ✅ Transações otimizadas

### Controller (ClienteController.java)
- ✅ Endpoints REST padronizados
- ✅ Documentação Swagger/OpenAPI
- ✅ Validações de entrada
- ✅ Códigos de status HTTP apropriados

## 🧪 Testes

Os testes gerados incluem:

- **ServiceTest**: Testa a lógica de negócios
- **ControllerTest**: Testa os endpoints REST
- Mocks apropriados com Mockito
- Cobertura de casos básicos de CRUD

## 📝 Melhorias Implementadas

### ✅ Relacionamentos JPA
- Suporte completo aos 4 tipos de relacionamento
- Configurações avançadas (cascade, fetch, orphanRemoval)
- Anotações Jackson para controle de serialização
- Métodos auxiliares para manipulação de relacionamentos

### ✅ Validações e DTOs
- Request DTOs com campos para relacionamentos
- Response DTOs com objetos aninhados
- Validações Bean Validation automáticas
- Factory methods para conversões

### ✅ Services Aprimorados
- Métodos de conversão Request ↔ Entity
- Tratamento automático de relacionamentos
- Transações otimizadas
- Injeção automática de repositórios relacionados

### ✅ Interface de Usuário
- Prompt interativo melhorado
- Validação de tipos e formatos
- Feedback visual com emojis
- Resumo antes da geração
- Confirmação de operações

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request
