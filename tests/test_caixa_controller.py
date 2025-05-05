import unittest
from control import caixa_controller

class TestCaixaController(unittest.TestCase):
    def test_listar_aberturas(self):
        caixas = caixa_controller.listar_aberturas()
        self.assertIsInstance(caixas, list)