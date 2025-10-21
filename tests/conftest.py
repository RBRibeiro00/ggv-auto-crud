import pytest
import os
import tempfile
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from unittest.mock import patch, MagicMock

# Import main functions
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import render_template, prompt_fields, prompt_relationships
from config import TEMPLATE_DIR, OUTPUT_DIR, PACKAGE_BASE


@pytest.fixture
def temp_output_dir():
    """Cria um diretório temporário para testes de output"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def jinja_env():
    """Fixture para environment Jinja2"""
    return Environment(loader=FileSystemLoader(TEMPLATE_DIR))


@pytest.fixture
def basic_context():
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


@pytest.fixture
def bigdecimal_context():
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


@pytest.fixture
def relationship_context():
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
                "cascade": "PERSIST,MERGE",
            },
            {
                "name": "itens",
                "type": "OneToMany",
                "target": "ItemPedido",
                "cascade": "ALL",
            },
        ],
    }
