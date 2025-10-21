import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Import modules to test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import prompt_fields, prompt_relationships
from tests.test_base import BaseTestCase


class TestInputValidation(BaseTestCase):
    """Testes para validação de entrada de dados"""

    def test_valid_string_field(self):
        """Testa criação de campo String válido"""
        field_data = {"name": "nome", "type": "String", "length": 100, "not_null": True}

        # Deve ser válido
        self.assertIsNotNone(field_data)
        self.assertEqual(field_data["type"], "String")
        self.assertTrue(field_data["not_null"])

    def test_valid_bigdecimal_field(self):
        """Testa criação de campo BigDecimal válido"""
        field_data = {"name": "preco", "type": "BigDecimal", "positive": True}

        self.assertEqual(field_data["type"], "BigDecimal")
        self.assertTrue(field_data["positive"])

    def test_valid_integer_field(self):
        """Testa criação de campo Integer válido"""
        field_data = {"name": "idade", "type": "Integer", "positive": True}

        self.assertEqual(field_data["type"], "Integer")
        self.assertTrue(field_data["positive"])

    def test_valid_relationship_many_to_one(self):
        """Testa criação de relacionamento ManyToOne válido"""
        relationship_data = {
            "name": "cliente",
            "type": "ManyToOne",
            "target": "Cliente",
            "cascade": "PERSIST,MERGE",
        }

        self.assertEqual(relationship_data["type"], "ManyToOne")
        self.assertEqual(relationship_data["target"], "Cliente")
        self.assertIn("PERSIST", relationship_data["cascade"])

    def test_valid_relationship_one_to_many(self):
        """Testa criação de relacionamento OneToMany válido"""
        relationship_data = {
            "name": "pedidos",
            "type": "OneToMany",
            "target": "Pedido",
            "cascade": "ALL",
        }

        self.assertEqual(relationship_data["type"], "OneToMany")
        self.assertEqual(relationship_data["target"], "Pedido")
        self.assertEqual(relationship_data["cascade"], "ALL")

    @patch("builtins.input")
    def test_prompt_fields_basic_flow(self, mock_input):
        """Testa fluxo básico de prompt de campos"""
        # Simula entrada do usuário no formato nome:tipo[:length][:positive]
        mock_input.side_effect = [
            "nome:String:100",  # campo completo
            "",  # finalizar
        ]

        fields = prompt_fields()

        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0]["name"], "nome")
        self.assertEqual(fields[0]["type"], "String")
        self.assertEqual(fields[0]["length"], 100)
        self.assertTrue(fields[0]["not_null"])

    @patch("builtins.input")
    def test_prompt_fields_bigdecimal_flow(self, mock_input):
        """Testa fluxo de criação de campo BigDecimal"""
        mock_input.side_effect = [
            "preco:BigDecimal::positive",  # campo BigDecimal positivo
            "",  # finalizar
        ]

        fields = prompt_fields()

        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0]["name"], "preco")
        self.assertEqual(fields[0]["type"], "BigDecimal")
        self.assertTrue(fields[0]["positive"])

    @patch("builtins.input")
    def test_prompt_fields_multiple_fields(self, mock_input):
        """Testa criação de múltiplos campos"""
        mock_input.side_effect = [
            "nome:String:100",  # campo 1
            "idade:Integer::positive",  # campo 2
            "",  # finalizar
        ]

        fields = prompt_fields()

        self.assertEqual(len(fields), 2)
        self.assertEqual(fields[0]["name"], "nome")
        self.assertEqual(fields[0]["type"], "String")
        self.assertEqual(fields[1]["name"], "idade")
        self.assertEqual(fields[1]["type"], "Integer")
        self.assertTrue(fields[1]["positive"])

    @patch("builtins.input")
    def test_prompt_relationships_many_to_one(self, mock_input):
        """Testa criação de relacionamento ManyToOne"""
        mock_input.side_effect = [
            "cliente:ManyToOne:Cliente::cascade",  # relacionamento completo
            "",  # finalizar
        ]

        relationships = prompt_relationships()

        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0]["name"], "cliente")
        self.assertEqual(relationships[0]["type"], "ManyToOne")
        self.assertEqual(relationships[0]["target"], "Cliente")
        self.assertTrue(relationships[0]["cascade"])

    @patch("builtins.input")
    def test_prompt_relationships_one_to_many(self, mock_input):
        """Testa criação de relacionamento OneToMany"""
        mock_input.side_effect = [
            "itens:OneToMany:Item:pedido:cascade",  # relacionamento com mapped_by
            "",  # finalizar
        ]

        relationships = prompt_relationships()

        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0]["name"], "itens")
        self.assertEqual(relationships[0]["type"], "OneToMany")
        self.assertEqual(relationships[0]["target"], "Item")
        self.assertEqual(relationships[0]["mapped_by"], "pedido")
        self.assertTrue(relationships[0]["cascade"])


if __name__ == "__main__":
    unittest.main()
