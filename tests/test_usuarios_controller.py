import unittest
from control import usuarios_controller

class TestUsuariosController(unittest.TestCase):
    def test_obter_usuarios(self):
        usuarios = usuarios_controller.obter_usuarios()
        self.assertIsInstance(usuarios, list)

    def test_autenticar_usuario_invalido(self):
        resultado = usuarios_controller.autenticar_usuario("fake", "123")
        self.assertFalse(resultado)