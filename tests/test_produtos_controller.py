import unittest
from control import produtos_controller

class TestProdutosController(unittest.TestCase):
    def test_buscar_produto_por_id(self):
        produto = produtos_controller.buscar_produto_por_id(1)
        self.assertIsInstance(produto, tuple)

    def test_listar_todos(self):
        produtos = produtos_controller.listar_todos()
        self.assertIsInstance(produtos, list)

    def test_buscar_produto_por_nome(self):
        resultado = produtos_controller.buscar_produto_por_nome("Teste")
        self.assertIsInstance(resultado, list)