import unittest
import tempfile
import shutil
import os
from pathlib import Path

# Import main functions
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import render_template
from config import TEMPLATE_DIR, PACKAGE_BASE


class BaseTestCase(unittest.TestCase):
    """Classe base para testes"""

    def setUp(self):
        """Setup comum para todos os testes"""
        self.temp_dir = tempfile.mkdtemp()
        self.maxDiff = None  # Para ver diffs completos

    def tearDown(self):
        """Cleanup após testes"""
        shutil.rmtree(self.temp_dir)

    def get_basic_context(self):
        """Context básico para testes"""
        return {
            "entity_name": "Cliente",
            "table_name": "TB_CLIENTE",
            "package_base": PACKAGE_BASE,
            "fields": [
                {"name": "nome", "type": "String", "length": 100, "not_null": True},
                {"name": "email", "type": "String", "length": 255, "not_null": True},
            ],
            "relationships": [],
        }

    def get_bigdecimal_context(self):
        """Context com BigDecimal para testes"""
        return {
            "entity_name": "Produto",
            "table_name": "TB_PRODUTO",
            "package_base": PACKAGE_BASE,
            "fields": [
                {"name": "nome", "type": "String", "length": 100, "not_null": True},
                {"name": "preco", "type": "BigDecimal", "positive": True},
            ],
            "relationships": [],
        }

    def get_relationship_context(self):
        """Context com relacionamentos para testes"""
        return {
            "entity_name": "Pedido",
            "table_name": "TB_PEDIDO",
            "package_base": PACKAGE_BASE,
            "fields": [
                {"name": "numero", "type": "String", "length": 50, "not_null": True}
            ],
            "relationships": [
                {
                    "name": "cliente",
                    "type": "ManyToOne",
                    "target": "Cliente",
                    "cascade": True,
                    "not_null": False,
                },
                {
                    "name": "itens",
                    "type": "OneToMany",
                    "target": "ItemPedido",
                    "cascade": True,
                    "mapped_by": "pedido",
                },
            ],
        }

    def render_template_to_string(self, template_name, context):
        """Helper para renderizar template como string"""
        from jinja2 import Environment, FileSystemLoader

        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        template = env.get_template(template_name)
        return template.render(context)
