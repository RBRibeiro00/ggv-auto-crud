import unittest
import os
import sys

# Import modules to test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_base import BaseTestCase


class TestRelationships(BaseTestCase):
    """Testes para relacionamentos entre entidades"""

    def test_entity_many_to_one_relationship(self):
        """Testa relacionamento ManyToOne na entidade"""
        context = self.get_relationship_context()
        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar anotações JPA
        self.assertIn("@ManyToOne", result)
        self.assertIn("@JoinColumn", result)
        self.assertIn('name="CLIENTE_ID"', result)

        # Verificar campo
        self.assertIn("private Cliente cliente;", result)

        # Verificar JSON annotations
        self.assertIn("@JsonBackReference", result)

    def test_entity_one_to_many_relationship(self):
        """Testa relacionamento OneToMany na entidade"""
        context = self.get_relationship_context()
        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar anotações JPA
        self.assertIn("@OneToMany", result)
        self.assertIn('mappedBy="pedido"', result)
        self.assertIn("cascade = CascadeType.ALL", result)

        # Verificar campo
        self.assertIn("private List<ItemPedido> itens", result)

        # Verificar inicialização
        self.assertIn("new ArrayList<>()", result)

        # Verificar JSON annotations
        self.assertIn("@JsonManagedReference", result)

    def test_request_with_relationships(self):
        """Testa DTO Request com relacionamentos"""
        context = self.get_relationship_context()
        result = self.render_template_to_string("request.java.j2", context)

        # Verificar campos para relacionamentos
        self.assertIn("UUID clienteId", result)  # ManyToOne
        self.assertIn("List<UUID> itensIds", result)  # OneToMany

    def test_response_with_relationships(self):
        """Testa DTO Response com relacionamentos"""
        context = self.get_relationship_context()
        result = self.render_template_to_string("response.java.j2", context)

        # Verificar DTOs summary
        self.assertIn("record ClienteSummaryResponse(Long id, String nome)", result)
        self.assertIn("record ItemPedidoSummaryResponse(Long id, String nome)", result)

        # Verificar campos na response
        self.assertIn("ClienteSummaryResponse cliente", result)
        self.assertIn("List<ItemPedidoSummaryResponse> itens", result)

    def test_service_with_relationships(self):
        """Testa Service com processamento de relacionamentos"""
        context = self.get_relationship_context()
        result = self.render_template_to_string("service.java.j2", context)

        # Verificar injeções de repositórios
        self.assertIn("private final ClienteRepository clienteRepository;", result)
        self.assertIn(
            "private final ItemPedidoRepository itempedidoRepository;", result
        )

        # Verificar método processRelationships
        self.assertIn("private void processRelationships", result)
        self.assertIn("request.clienteId()", result)
        self.assertIn("request.itensIds()", result)

        # Verificar busca de entidades relacionadas
        self.assertIn("clienteRepository.findById", result)
        self.assertIn("itempedidoRepository.findAllById", result)

    def test_mapper_with_relationships(self):
        """Testa Mapper com relacionamentos"""
        context = self.get_relationship_context()
        result = self.render_template_to_string("mapper.java.j2", context)

        # Verificar mappings para relacionamentos
        self.assertIn('@Mapping(target = "cliente", ignore = true)', result)
        self.assertIn('@Mapping(target = "itens", ignore = true)', result)

        # Verificar métodos customizados
        self.assertIn('@Named("clienteToClienteSummary")', result)
        self.assertIn('@Named("itempedidoListToItemPedidoSummaryList")', result)

        # Verificar implementações default
        self.assertIn("default ClienteSummaryResponse clienteToClienteSummary", result)
        self.assertIn("default List<ItemPedidoSummaryResponse>", result)


class TestRelationshipTypes(BaseTestCase):
    """Testes para diferentes tipos de relacionamentos"""

    def get_many_to_many_context(self):
        """Context para relacionamento ManyToMany"""
        return {
            "entity_name": "Produto",
            "table_name": "TB_PRODUTO",
            "package_base": "com.example",
            "fields": [
                {"name": "nome", "type": "String", "length": 100, "not_null": True}
            ],
            "relationships": [
                {
                    "name": "categorias",
                    "type": "ManyToMany",
                    "target": "Categoria",
                    "cascade": "PERSIST,MERGE",
                }
            ],
        }

    def get_one_to_one_context(self):
        """Context para relacionamento OneToOne"""
        return {
            "entity_name": "Usuario",
            "table_name": "TB_USUARIO",
            "package_base": "com.example",
            "fields": [
                {"name": "login", "type": "String", "length": 50, "not_null": True}
            ],
            "relationships": [
                {
                    "name": "perfil",
                    "type": "OneToOne",
                    "target": "Perfil",
                    "cascade": "ALL",
                }
            ],
        }

    def test_many_to_many_relationship(self):
        """Testa relacionamento ManyToMany"""
        context = self.get_many_to_many_context()
        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar anotações JPA
        self.assertIn("@ManyToMany", result)
        self.assertIn("@JoinTable", result)
        self.assertIn("joinColumns = @JoinColumn", result)
        self.assertIn("inverseJoinColumns = @JoinColumn", result)

        # Verificar tipo Set
        self.assertIn("private Set<Categoria> categorias", result)
        self.assertIn("new HashSet<>()", result)

        # Verificar métodos helper
        self.assertIn("public void addCategoria", result)
        self.assertIn("public void removeCategoria", result)

    def test_one_to_one_relationship(self):
        """Testa relacionamento OneToOne"""
        context = self.get_one_to_one_context()
        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar anotações JPA
        self.assertIn("@OneToOne", result)
        self.assertIn("@JoinColumn", result)
        self.assertIn("cascade = CascadeType.ALL", result)

        # Verificar campo
        self.assertIn("private Perfil perfil;", result)

    def test_cascade_options(self):
        """Testa diferentes opções de cascade"""
        # Teste CASCADE ALL
        context = self.get_one_to_one_context()
        result = self.render_template_to_string("entity.java.j2", context)
        self.assertIn("cascade = CascadeType.ALL", result)

        # Teste CASCADE PERSIST,MERGE
        context = self.get_many_to_many_context()
        result = self.render_template_to_string("entity.java.j2", context)
        self.assertIn("cascade = {CascadeType.PERSIST, CascadeType.MERGE}", result)

    def test_service_many_to_many_processing(self):
        """Testa processamento de relacionamento ManyToMany no service"""
        context = self.get_many_to_many_context()
        result = self.render_template_to_string("service.java.j2", context)

        # Verificar uso de HashSet para ManyToMany
        self.assertIn("new java.util.HashSet<>", result)
        self.assertIn("request.categoriasIds()", result)
        self.assertIn("categoriaRepository.findAllById", result)


class TestRelationshipValidation(BaseTestCase):
    """Testes para validação de relacionamentos"""

    def test_required_relationship_validation(self):
        """Testa validação de relacionamento obrigatório"""
        context = {
            "entity_name": "Pedido",
            "table_name": "TB_PEDIDO",
            "package_base": "com.example",
            "fields": [],
            "relationships": [
                {
                    "name": "cliente",
                    "type": "ManyToOne",
                    "target": "Cliente",
                    "cascade": "PERSIST,MERGE",
                    "not_null": True,
                }
            ],
        }

        result = self.render_template_to_string("request.java.j2", context)
        self.assertIn("@NotNull", result)
        self.assertIn("UUID clienteId", result)

    def test_optional_relationship(self):
        """Testa relacionamento opcional"""
        context = {
            "entity_name": "Produto",
            "table_name": "TB_PRODUTO",
            "package_base": "com.example",
            "fields": [],
            "relationships": [
                {
                    "name": "categoria",
                    "type": "ManyToOne",
                    "target": "Categoria",
                    "cascade": "PERSIST,MERGE",
                    "required": False,
                }
            ],
        }

        result = self.render_template_to_string("entity.java.j2", context)
        # Relacionamento opcional não deve ter nullable=false
        self.assertNotIn("nullable=false", result)


if __name__ == "__main__":
    unittest.main()
