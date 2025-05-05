import unittest
from control import contas_receber_controller

class TestContasReceberController(unittest.TestCase):
    def test_listar_contas(self):
        contas = contas_receber_controller.listar_contas()
        self.assertIsInstance(contas, list)