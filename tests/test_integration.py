import unittest
import os
import tempfile
import shutil
import sys
from unittest.mock import patch, MagicMock

# Import modules to test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main, render_template
from tests.test_base import BaseTestCase


class TestIntegration(BaseTestCase):
    """Testes de integração do workflow completo"""

    def setUp(self):
        super().setUp()
        # Criar diretório temporário para output
        self.temp_output = tempfile.mkdtemp()

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.temp_output)

    @patch("main.OUTPUT_DIR")
    @patch("builtins.input")
    def test_complete_workflow_basic_entity(self, mock_input, mock_output_dir):
        """Testa workflow completo para entidade básica"""
        mock_output_dir.return_value = self.temp_output

        # Simular entrada do usuário
        mock_input.side_effect = [
            "Cliente",  # nome da entidade
            "TB_CLIENTE",  # nome da tabela
            "nome:String:100",  # campo 1
            "email:String:255",  # campo 2
            "",  # finalizar campos
            "",  # finalizar relacionamentos
            "s",  # confirmar geração
        ]

        # Executar main
        with patch("main.OUTPUT_DIR", self.temp_output):
            main()

        # Verificar se arquivos foram criados
        cliente_dir = os.path.join(self.temp_output, "Cliente")
        self.assertTrue(os.path.exists(cliente_dir))

        expected_files = [
            "Cliente.java",
            "ClienteRepository.java",
            "ClienteRequest.java",
            "ClienteResponse.java",
            "ClienteMapper.java",
            "ClienteService.java",
            "ClienteController.java",
            "ClienteServiceTest.java",
            "ClienteControllerTest.java",
        ]

        for file_name in expected_files:
            file_path = os.path.join(cliente_dir, file_name)
            self.assertTrue(
                os.path.exists(file_path), f"Arquivo {file_name} não foi criado"
            )

            # Verificar se arquivo não está vazio
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertGreater(len(content), 0, f"Arquivo {file_name} está vazio")

    @patch("main.OUTPUT_DIR")
    @patch("builtins.input")
    def test_complete_workflow_with_relationships(self, mock_input, mock_output_dir):
        """Testa workflow completo com relacionamentos"""
        mock_output_dir.return_value = self.temp_output

        mock_input.side_effect = [
            "Pedido",  # nome da entidade
            "TB_PEDIDO",  # nome da tabela
            "numero:String:50",  # campo com formato novo
            "",  # terminar campos
            "cliente:ManyToOne:Cliente::cascade",  # relacionamento 1
            "itens:OneToMany:Item:pedido:cascade",  # relacionamento 2
            "",  # terminar relacionamentos
            "s",  # confirmar geração
        ]

        with patch("main.OUTPUT_DIR", self.temp_output):
            main()

        # Verificar arquivo de entidade
        entity_file = os.path.join(self.temp_output, "Pedido", "Pedido.java")
        self.assertTrue(os.path.exists(entity_file))

        with open(entity_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Verificar relacionamentos
            self.assertIn("@ManyToOne", content)
            self.assertIn("@OneToMany", content)
            self.assertIn("private Cliente cliente", content)
            self.assertIn("private List<Item> itens", content)

    def test_file_generation_consistency(self):
        """Testa consistência entre arquivos gerados"""
        context = {
            "entity_name": "Produto",
            "table_name": "TB_PRODUTO",
            "package_base": "com.example",
            "fields": [
                {"name": "nome", "type": "String", "length": 100, "not_null": True},
                {"name": "preco", "type": "BigDecimal", "positive": True},
            ],
            "relationships": [],
        }

        # Gerar todos os templates
        templates = [
            "entity.java.j2",
            "repository.java.j2",
            "service.java.j2",
            "controller.java.j2",
            "request.java.j2",
            "response.java.j2",
            "mapper.java.j2",
        ]

        generated_contents = {}
        for template in templates:
            content = self.render_template_to_string(template, context)
            generated_contents[template] = content

        # Verificar consistências entre arquivos

        # 1. Imports consistentes
        entity_content = generated_contents["entity.java.j2"]
        service_content = generated_contents["service.java.j2"]

        # Service deve importar Entity
        self.assertIn("import com.example.domain.Produto", service_content)

        # 2. Nomes de classes consistentes
        self.assertIn("public class Produto", entity_content)
        self.assertIn("public class ProdutoService", service_content)
        self.assertIn(
            "public interface ProdutoRepository",
            generated_contents["repository.java.j2"],
        )

        # 3. Tipos de campos consistentes
        request_content = generated_contents["request.java.j2"]
        response_content = generated_contents["response.java.j2"]

        # BigDecimal deve aparecer em todos
        self.assertIn("BigDecimal preco", entity_content)
        self.assertIn("BigDecimal preco", request_content)
        self.assertIn("BigDecimal preco", response_content)

        # 4. Validações consistentes
        self.assertIn("@Positive", request_content)
        self.assertIn("precision=19, scale=2", entity_content)

    def test_error_handling_template_not_found(self):
        """Testa tratamento de erro quando template não existe"""
        context = self.get_basic_context()

        with self.assertRaises(Exception):
            self.render_template_to_string("inexistente.j2", context)

    def test_directory_creation(self):
        """Testa criação de diretórios para output"""
        context = self.get_basic_context()
        output_path = os.path.join(self.temp_dir, "TestEntity", "TestEntity.java")

        # Diretório não existe ainda
        self.assertFalse(os.path.exists(os.path.dirname(output_path)))

        # render_template deve criar o diretório
        render_template("entity.java.j2", context, output_path)

        # Agora deve existir
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(os.path.isfile(output_path))


class TestPerformance(BaseTestCase):
    """Testes de performance básicos"""

    def test_large_entity_generation(self):
        """Testa geração de entidade com muitos campos"""
        import time

        # Criar entidade com 50 campos
        fields = []
        for i in range(50):
            fields.append(
                {"name": f"campo{i}", "type": "String", "length": 100, "not_null": True}
            )

        context = {
            "entity_name": "EntidadeGrande",
            "table_name": "TB_ENTIDADE_GRANDE",
            "package_base": "com.example",
            "fields": fields,
            "relationships": [],
        }

        start_time = time.time()
        result = self.render_template_to_string("entity.java.j2", context)
        end_time = time.time()

        # Deve gerar em menos de 1 segundo
        self.assertLess(end_time - start_time, 1.0)

        # Verificar se todos os campos foram gerados
        for i in range(50):
            self.assertIn(f"private String campo{i};", result)

    def test_multiple_relationships_performance(self):
        """Testa geração com muitos relacionamentos"""
        import time

        # Criar 20 relacionamentos
        relationships = []
        for i in range(20):
            relationships.append(
                {
                    "name": f"rel{i}",
                    "type": "ManyToOne",
                    "target": f"Entity{i}",
                    "cascade": "PERSIST,MERGE",
                }
            )

        context = {
            "entity_name": "EntidadeComRelacionamentos",
            "table_name": "TB_ENTIDADE_REL",
            "package_base": "com.example",
            "fields": [
                {"name": "nome", "type": "String", "length": 100, "not_null": True}
            ],
            "relationships": relationships,
        }

        start_time = time.time()
        result = self.render_template_to_string("entity.java.j2", context)
        end_time = time.time()

        # Deve gerar em menos de 2 segundos
        self.assertLess(end_time - start_time, 2.0)

        # Verificar relacionamentos
        for i in range(20):
            self.assertIn(f"private Entity{i} rel{i};", result)


if __name__ == "__main__":
    unittest.main()
