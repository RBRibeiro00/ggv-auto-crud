import unittest
import os
import tempfile
import sys

# Import modules to test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_base import BaseTestCase


class TestEntityTemplate(BaseTestCase):
    """Testes para template entity.java.j2"""

    def test_entity_basic_generation(self):
        """Testa geração básica de entidade"""
        context = self.get_basic_context()
        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar estrutura básica
        self.assertIn("public class Cliente", result)
        self.assertIn("@Entity", result)
        self.assertIn('@Table(name="TB_CLIENTE")', result)
        self.assertIn("@Id", result)
        self.assertIn("@GeneratedValue(strategy = GenerationType.IDENTITY)", result)
        self.assertIn("private Long id;", result)

        # Verificar campos
        self.assertIn("private String nome;", result)
        self.assertIn("private String email;", result)
        self.assertIn('@Column(name="NOME"', result)
        self.assertIn('@Column(name="EMAIL"', result)

        # Verificar annotations Lombok
        self.assertIn("@Builder", result)
        self.assertIn("@Getter", result)
        self.assertIn("@Setter", result)
        self.assertIn("@NoArgsConstructor", result)
        self.assertIn("@AllArgsConstructor", result)

    def test_entity_bigdecimal_field(self):
        """Testa geração de entidade com campo BigDecimal"""
        context = self.get_bigdecimal_context()
        result = self.render_template_to_string("entity.java.j2", context)

        # Verificar BigDecimal
        self.assertIn("private BigDecimal preco;", result)
        self.assertIn('@Column(name="PRECO"', result)
        self.assertIn("precision=19, scale=2", result)

        # Verificar import
        self.assertIn("import java.math.BigDecimal;", result)

    def test_entity_uppercase_columns(self):
        """Testa se nomes de colunas estão em maiúsculo"""
        context = self.get_basic_context()
        result = self.render_template_to_string("entity.java.j2", context)

        self.assertIn('@Column(name="NOME"', result)
        self.assertIn('@Column(name="EMAIL"', result)
        self.assertNotIn('@Column(name="nome"', result)
        self.assertNotIn('@Column(name="email"', result)


class TestServiceTemplate(BaseTestCase):
    """Testes para template service.java.j2"""

    def test_service_basic_generation(self):
        """Testa geração básica de service"""
        context = self.get_basic_context()
        result = self.render_template_to_string("service.java.j2", context)

        # Verificar estrutura básica
        self.assertIn("public class ClienteService", result)
        self.assertIn("@Service", result)
        self.assertIn("@RequiredArgsConstructor", result)
        self.assertIn("@Transactional(readOnly = true)", result)

        # Verificar injeções
        self.assertIn("private final ClienteRepository repository;", result)
        self.assertIn("private final ClienteMapper mapper;", result)

        # Verificar métodos principais
        self.assertIn("public List<Cliente> findAll()", result)
        self.assertIn("public List<ClienteResponse> findAllResponses()", result)
        self.assertIn("public Cliente findById(Long id)", result)
        self.assertIn("public ClienteResponse findResponseById(Long id)", result)
        self.assertIn("public ClienteResponse saveFromRequest", result)
        self.assertIn("public ClienteResponse updateFromRequest", result)
        self.assertIn("public void delete(Long id)", result)

    def test_service_mapstruct_usage(self):
        """Testa se service usa MapStruct corretamente"""
        context = self.get_basic_context()
        result = self.render_template_to_string("service.java.j2", context)

        # Verificar uso do mapper
        self.assertIn("mapper.toResponseList", result)
        self.assertIn("mapper.toEntity", result)
        self.assertIn("mapper.toResponse", result)
        self.assertIn("mapper.updateEntityFromRequest", result)

        # Verificar que não tem métodos de conversão manual
        self.assertNotIn("from{{ entity_name }}", result)
        self.assertNotIn("convertRequestToEntity", result)

    def test_service_error_messages_portuguese(self):
        """Testa se mensagens de erro estão em português"""
        context = self.get_basic_context()
        result = self.render_template_to_string("service.java.j2", context)

        self.assertIn("não foi encontrado", result)
        self.assertIn("Cliente com ID", result)
        self.assertNotIn("not found", result)


class TestControllerTemplate(BaseTestCase):
    """Testes para template controller.java.j2"""

    def test_controller_basic_generation(self):
        """Testa geração básica de controller"""
        context = self.get_basic_context()
        result = self.render_template_to_string("controller.java.j2", context)

        # Verificar estrutura básica
        self.assertIn("public class ClienteController", result)
        self.assertIn("@RestController", result)
        self.assertIn('@RequestMapping("/api/cliente")', result)
        self.assertIn("@RequiredArgsConstructor", result)
        self.assertIn("@Validated", result)

        # Verificar injeção
        self.assertIn("private final ClienteService service;", result)

        # Verificar endpoints
        self.assertIn("@PostMapping", result)
        self.assertIn("@GetMapping", result)
        self.assertIn("@PutMapping", result)
        self.assertIn("@DeleteMapping", result)

    def test_controller_swagger_annotations(self):
        """Testa se annotations Swagger estão presentes"""
        context = self.get_basic_context()
        result = self.render_template_to_string("controller.java.j2", context)

        self.assertIn("@Operation", result)
        self.assertIn("@Tag", result)
        self.assertIn("summary=", result)

    def test_controller_path_variables_long(self):
        """Testa se PathVariable usa Long em vez de UUID"""
        context = self.get_basic_context()
        result = self.render_template_to_string("controller.java.j2", context)

        self.assertIn("@PathVariable Long id", result)
        self.assertNotIn("@PathVariable UUID id", result)
        self.assertNotIn("import java.util.UUID", result)


class TestRepositoryTemplate(BaseTestCase):
    """Testes para template repository.java.j2"""

    def test_repository_basic_generation(self):
        """Testa geração básica de repository"""
        context = self.get_basic_context()
        result = self.render_template_to_string("repository.java.j2", context)

        # Verificar estrutura básica
        self.assertIn("public interface ClienteRepository", result)
        self.assertIn("extends JpaRepository<Cliente, Long>", result)
        self.assertIn("@Repository", result)

        # Verificar que não tem UUID
        self.assertNotIn("UUID", result)


class TestMapperTemplate(BaseTestCase):
    """Testes para template mapper.java.j2"""

    def test_mapper_basic_generation(self):
        """Testa geração básica de mapper"""
        context = self.get_basic_context()
        result = self.render_template_to_string("mapper.java.j2", context)

        # Verificar estrutura básica
        self.assertIn("public interface ClienteMapper", result)
        self.assertIn('@Mapper(componentModel = "spring")', result)

        # Verificar métodos de conversão
        self.assertIn("Cliente toEntity(ClienteRequest request)", result)
        self.assertIn("ClienteResponse toResponse(Cliente entity)", result)
        self.assertIn("List<ClienteResponse> toResponseList", result)
        self.assertIn("void updateEntityFromRequest", result)

        # Verificar mappings
        self.assertIn('@Mapping(target = "id", ignore = true)', result)


class TestRequestTemplate(BaseTestCase):
    """Testes para template request.java.j2"""

    def test_request_basic_generation(self):
        """Testa geração básica de request DTO"""
        context = self.get_basic_context()
        result = self.render_template_to_string("request.java.j2", context)

        # Verificar estrutura record
        self.assertIn("public record ClienteRequest(", result)

        # Verificar validações
        self.assertIn("@NotBlank", result)
        self.assertIn("@Size(max=100)", result)
        self.assertIn("@Size(max=255)", result)

        # Verificar campos
        self.assertIn("String nome", result)
        self.assertIn("String email", result)

    def test_request_bigdecimal_validation(self):
        """Testa validações de BigDecimal"""
        context = self.get_bigdecimal_context()
        result = self.render_template_to_string("request.java.j2", context)

        self.assertIn("@Positive", result)
        self.assertIn("@DecimalMin", result)
        self.assertIn("@Digits", result)
        self.assertIn("BigDecimal preco", result)


class TestResponseTemplate(BaseTestCase):
    """Testes para template response.java.j2"""

    def test_response_basic_generation(self):
        """Testa geração básica de response DTO"""
        context = self.get_basic_context()
        result = self.render_template_to_string("response.java.j2", context)

        # Verificar estrutura record
        self.assertIn("public record ClienteResponse(", result)

        # Verificar campos
        self.assertIn("Long id", result)
        self.assertIn("String nome", result)
        self.assertIn("String email", result)

        # Verificar que factory methods foram removidos
        self.assertIn("MapStruct handled conversions", result)
        self.assertNotIn("public static ClienteResponse from", result)


if __name__ == "__main__":
    unittest.main()
