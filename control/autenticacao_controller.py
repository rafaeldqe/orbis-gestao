from model.usuario_model import validar_login

def autenticar(usuario, senha):
    resultado = validar_login(usuario, senha)
    if resultado:
        nome, tipo = resultado
        return {'nome': nome, 'tipo': tipo}
    else:
        return None
