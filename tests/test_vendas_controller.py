import unittest
from control import vendas_controller

class TestVendasController(unittest.TestCase):
    def test_listar_vendas(self):
        vendas = vendas_controller.listar_vendas()
        self.assertIsInstance(vendas, list)

    def test_listar_itens_venda(self):
        itens = vendas_controller.listar_itens_venda(1)
        self.assertIsInstance(itens, list)