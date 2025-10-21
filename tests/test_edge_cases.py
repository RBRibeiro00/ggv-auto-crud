import unittest
import os
import sys

# Import modules to test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_base import BaseTestCase


class TestEdgeCases(BaseTestCase):
    """Testes para casos extremos e edge cases"""

    def test_entity_without_fields(self):
        """Testa entidade sem campos (apenas ID)"""
        context = {
            "entity_name": "Categoria",
            "table_name": "TB_CATEGORIA",
            "package_base": "com.example",
            "fields": [],
            "relationships": [],
        }

        result = self.render_template_to_string("entity.java.j2", context)

        # Deve ter pelo menos ID
        self.assertIn("private Long id;", result)
        self.assertIn("@Id", result)
        self.assertIn("@GeneratedValue", result)

        # Não deve ter campos extras
        self.assertNotIn("private String", result)
        self.assertNotIn("private Integer", result)

    def test_entity_with_special_characters_in_name(self):
        """Testa entidade com caracteres especiais no nome"""
        context = {
            "entity_name": "ItemPedido",
            "table_name": "TB_ITEM_PEDIDO",
            "package_base": "com.example",
            "fields": [
                {"name": "nomeItem", "type": "String", "length": 100, "not_null": True}
            ],
            "relationships": [],
        }

        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar nome da classe
        self.assertIn("public class ItemPedido", result)
        self.assertIn('@Table(name="TB_ITEM_PEDIDO")', result)

        # Verificar campo com camelCase
        self.assertIn("private String nomeItem;", result)
        self.assertIn('@Column(name="NOMEITEM"', result)

    def test_field_with_maximum_length(self):
        """Testa campo com comprimento máximo"""
        context = {
            "entity_name": "Texto",
            "table_name": "TB_TEXTO",
            "package_base": "com.example",
            "fields": [
                {
                    "name": "conteudo",
                    "type": "String",
                    "length": 65535,
                    "not_null": True,
                }
            ],
            "relationships": [],
        }

        result = self.render_template_to_string("entity.java.j2", context)

        self.assertIn('@Column(name="CONTEUDO", length=65535', result)

        # Verificar no request também
        result_request = self.render_template_to_string("request.java.j2", context)
        self.assertIn("@Size(max=65535)", result_request)

    def test_all_field_types(self):
        """Testa entidade com todos os tipos de campos suportados"""
        context = {
            "entity_name": "TodosTipos",
            "table_name": "TB_TODOS_TIPOS",
            "package_base": "com.example",
            "fields": [
                {"name": "texto", "type": "String", "length": 100, "not_null": True},
                {"name": "inteiro", "type": "Integer", "positive": True},
                {"name": "longo", "type": "Long", "positive": True},
                {"name": "decimal", "type": "Double"},
                {"name": "flutuante", "type": "Float"},
                {"name": "dinheiro", "type": "BigDecimal", "positive": True},
                {"name": "ativo", "type": "Boolean"},
                {"name": "data", "type": "LocalDate"},
                {"name": "timestamp", "type": "LocalDateTime"},
            ],
            "relationships": [],
        }

        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar todos os tipos
        self.assertIn("private String texto;", result)
        self.assertIn("private Integer inteiro;", result)
        self.assertIn("private Long longo;", result)
        self.assertIn("private Double decimal;", result)
        self.assertIn("private Float flutuante;", result)
        self.assertIn("private BigDecimal dinheiro;", result)
        self.assertIn("private Boolean ativo;", result)
        self.assertIn("private LocalDate data;", result)
        self.assertIn("private LocalDateTime timestamp;", result)

        # Verificar imports necessários
        self.assertIn("import java.math.BigDecimal;", result)
        self.assertIn("import java.time.LocalDate;", result)
        self.assertIn("import java.time.LocalDateTime;", result)

    def test_entity_with_multiple_relationships(self):
        """Testa entidade com múltiplos relacionamentos"""
        context = {
            "entity_name": "Pedido",
            "table_name": "TB_PEDIDO",
            "package_base": "com.example",
            "fields": [
                {"name": "numero", "type": "String", "length": 50, "not_null": True}
            ],
            "relationships": [
                {
                    "name": "cliente",
                    "type": "ManyToOne",
                    "target": "Cliente",
                    "cascade": "PERSIST,MERGE",
                },
                {
                    "name": "vendedor",
                    "type": "ManyToOne",
                    "target": "Vendedor",
                    "cascade": "PERSIST,MERGE",
                },
                {
                    "name": "itens",
                    "type": "OneToMany",
                    "target": "Item",
                    "cascade": "ALL",
                },
                {
                    "name": "cupons",
                    "type": "ManyToMany",
                    "target": "Cupom",
                    "cascade": "PERSIST,MERGE",
                },
            ],
        }

        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar todos os relacionamentos
        self.assertIn("private Cliente cliente;", result)
        self.assertIn("private Vendedor vendedor;", result)
        self.assertIn("private List<Item> itens", result)
        self.assertIn("private Set<Cupom> cupons", result)

        # Verificar anotações
        self.assertIn("@ManyToOne", result)
        self.assertIn("@OneToMany", result)
        self.assertIn("@ManyToMany", result)

    def test_request_validation_edge_cases(self):
        """Testa validações extremas no request"""
        context = {
            "entity_name": "ValidacaoExtrema",
            "table_name": "TB_VALIDACAO_EXTREMA",
            "package_base": "com.example",
            "fields": [
                {
                    "name": "textoMinimo",
                    "type": "String",
                    "length": 1,
                    "not_null": True,
                },
                {"name": "numeroPositivo", "type": "Integer", "positive": True},
                {"name": "decimalPreciso", "type": "BigDecimal", "positive": True},
                {
                    "name": "textoOpcional",
                    "type": "String",
                    "length": 50,
                    "not_null": False,
                },
            ],
            "relationships": [],
        }

        result = self.render_template_to_string("request.java.j2", context)

        # Verificar validações específicas
        self.assertIn("@Size(max=1)", result)  # texto mínimo
        self.assertIn("@Positive", result)  # número positivo
        self.assertIn("@DecimalMin", result)  # BigDecimal
        self.assertIn("@Digits", result)  # BigDecimal precision

        # Campo opcional não deve ter @NotBlank
        texto_opcional_index = result.find("textoOpcional")
        not_blank_before_opcional = result.rfind("@NotBlank", 0, texto_opcional_index)
        not_blank_after_opcional = result.find("@NotBlank", texto_opcional_index)

        # Se @NotBlank aparece após textoOpcional, não é para este campo
        if not_blank_after_opcional != -1:
            # Verificar se é para outro campo
            next_field = result.find("String", texto_opcional_index + 10)
            self.assertGreater(next_field, not_blank_after_opcional)

    def test_empty_relationships_list(self):
        """Testa entidade com lista vazia de relacionamentos"""
        context = self.get_basic_context()
        context["relationships"] = []

        result = self.render_template_to_string("entity.java.j2", context)

        # Não deve ter imports de relacionamentos
        self.assertNotIn("@ManyToOne", result)
        self.assertNotIn("@OneToMany", result)
        self.assertNotIn("@ManyToMany", result)
        self.assertNotIn("@OneToOne", result)
        self.assertNotIn("@JoinColumn", result)

    def test_service_with_no_relationships(self):
        """Testa service sem relacionamentos"""
        context = self.get_basic_context()
        context["relationships"] = []

        result = self.render_template_to_string("service.java.j2", context)

        # Método processRelationships deve estar vazio ou comentado
        self.assertIn("processRelationships", result)

        # Não deve ter injeções de outros repositórios
        repository_count = result.count("Repository")
        self.assertEqual(repository_count, 2)  # Apenas ClienteRepository e no import


class TestSpecialScenarios(BaseTestCase):
    """Testes para cenários especiais de uso"""

    def test_portuguese_strings_consistency(self):
        """Testa consistência das strings em português"""
        context = self.get_basic_context()

        # Testar service
        result_service = self.render_template_to_string("service.java.j2", context)
        self.assertIn("não foi encontrado", result_service)
        self.assertNotIn("not found", result_service)

        # Testar controller
        result_controller = self.render_template_to_string(
            "controller.java.j2", context
        )
        self.assertIn("Criar um novo", result_controller)
        self.assertIn("Buscar", result_controller)
        self.assertIn("Listar todos", result_controller)
        self.assertIn("Atualizar", result_controller)
        self.assertIn("Deletar", result_controller)

    def test_table_name_uppercase(self):
        """Testa se nome da tabela fica em maiúsculo"""
        context = {
            "entity_name": "Produto",
            "table_name": "tb_produto_especial",  # minúsculo
            "package_base": "com.example",
            "fields": [],
            "relationships": [],
        }

        result = self.render_template_to_string("entity.java.j2", context)

        # Deve converter para maiúsculo
        self.assertIn('@Table(name="TB_PRODUTO_ESPECIAL")', result)
        self.assertNotIn('@Table(name="tb_produto_especial")', result)

    def test_column_names_uppercase(self):
        """Testa se nomes de colunas ficam em maiúsculo"""
        context = {
            "entity_name": "Teste",
            "table_name": "TB_TESTE",
            "package_base": "com.example",
            "fields": [
                {
                    "name": "nomeCompleto",
                    "type": "String",
                    "length": 100,
                    "not_null": True,
                },
                {
                    "name": "email_corporativo",
                    "type": "String",
                    "length": 255,
                    "not_null": True,
                },
            ],
            "relationships": [],
        }

        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar colunas em maiúsculo
        self.assertIn('@Column(name="NOMECOMPLETO"', result)
        self.assertIn('@Column(name="EMAIL_CORPORATIVO"', result)

        # Não deve ter minúsculo
        self.assertNotIn('@Column(name="nomeCompleto"', result)
        self.assertNotIn('@Column(name="email_corporativo"', result)


if __name__ == "__main__":
    unittest.main()
