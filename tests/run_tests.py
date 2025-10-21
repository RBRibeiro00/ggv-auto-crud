import unittest
import sys
import os

# Import test modules
from tests.test_validation import TestInputValidation
from tests.test_templates import (
    TestEntityTemplate,
    TestServiceTemplate,
    TestControllerTemplate,
    TestRepositoryTemplate,
    TestMapperTemplate,
    TestRequestTemplate,
    TestResponseTemplate,
)
from tests.test_relationships import (
    TestRelationships,
    TestRelationshipTypes,
    TestRelationshipValidation,
)
from tests.test_edge_cases import TestEdgeCases, TestSpecialScenarios
from tests.test_integration import TestIntegration, TestPerformance


def create_test_suite():
    """Cria a suíte completa de testes"""
    suite = unittest.TestSuite()

    # Testes de validação
    suite.addTest(unittest.makeSuite(TestInputValidation))

    # Testes de templates
    suite.addTest(unittest.makeSuite(TestEntityTemplate))
    suite.addTest(unittest.makeSuite(TestServiceTemplate))
    suite.addTest(unittest.makeSuite(TestControllerTemplate))
    suite.addTest(unittest.makeSuite(TestRepositoryTemplate))
    suite.addTest(unittest.makeSuite(TestMapperTemplate))
    suite.addTest(unittest.makeSuite(TestRequestTemplate))
    suite.addTest(unittest.makeSuite(TestResponseTemplate))

    # Testes de relacionamentos
    suite.addTest(unittest.makeSuite(TestRelationships))
    suite.addTest(unittest.makeSuite(TestRelationshipTypes))
    suite.addTest(unittest.makeSuite(TestRelationshipValidation))

    # Testes de edge cases
    suite.addTest(unittest.makeSuite(TestEdgeCases))
    suite.addTest(unittest.makeSuite(TestSpecialScenarios))

    # Testes de integração
    suite.addTest(unittest.makeSuite(TestIntegration))
    suite.addTest(unittest.makeSuite(TestPerformance))

    return suite


def run_specific_test_category(category):
    """Executa categoria específica de testes"""
    suite = unittest.TestSuite()

    if category == "validation":
        suite.addTest(unittest.makeSuite(TestInputValidation))
    elif category == "templates":
        suite.addTest(unittest.makeSuite(TestEntityTemplate))
        suite.addTest(unittest.makeSuite(TestServiceTemplate))
        suite.addTest(unittest.makeSuite(TestControllerTemplate))
        suite.addTest(unittest.makeSuite(TestRepositoryTemplate))
        suite.addTest(unittest.makeSuite(TestMapperTemplate))
        suite.addTest(unittest.makeSuite(TestRequestTemplate))
        suite.addTest(unittest.makeSuite(TestResponseTemplate))
    elif category == "relationships":
        suite.addTest(unittest.makeSuite(TestRelationships))
        suite.addTest(unittest.makeSuite(TestRelationshipTypes))
        suite.addTest(unittest.makeSuite(TestRelationshipValidation))
    elif category == "edge_cases":
        suite.addTest(unittest.makeSuite(TestEdgeCases))
        suite.addTest(unittest.makeSuite(TestSpecialScenarios))
    elif category == "integration":
        suite.addTest(unittest.makeSuite(TestIntegration))
        suite.addTest(unittest.makeSuite(TestPerformance))
    else:
        print(f"Categoria '{category}' não encontrada!")
        print(
            "Categorias disponíveis: validation, templates, relationships, edge_cases, integration"
        )
        return

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Executar testes do gerador CRUD")
    parser.add_argument(
        "--category",
        "-c",
        choices=[
            "validation",
            "templates",
            "relationships",
            "edge_cases",
            "integration",
        ],
        help="Executar apenas uma categoria específica de testes",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Saída verbosa dos testes"
    )

    args = parser.parse_args()

    if args.category:
        print(f"\n🧪 Executando testes da categoria: {args.category}")
        print("=" * 60)
        result = run_specific_test_category(args.category)
    else:
        print("\n🧪 Executando TODOS os testes do gerador CRUD")
        print("=" * 60)

        # Executar todos os testes
        suite = create_test_suite()
        verbosity = 2 if args.verbose else 1
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)

    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)

    if result.wasSuccessful():
        print("✅ TODOS OS TESTES PASSARAM!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")

    print(f"🏃 Testes executados: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")

    if result.failures:
        print(f"❌ Falhas: {len(result.failures)}")
        for test, traceback in result.failures:
            print(f"   - {test}")

    if result.errors:
        print(f"💥 Erros: {len(result.errors)}")
        for test, traceback in result.errors:
            print(f"   - {test}")

    # Exit code para CI/CD
    exit_code = 0 if result.wasSuccessful() else 1
    sys.exit(exit_code)
