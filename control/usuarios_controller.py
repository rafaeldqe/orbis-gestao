from model.usuario_model import listar_todos, inserir_usuario, editar_usuario, desativar_usuario

def obter_usuarios():
    return listar_todos()

def adicionar_usuario(nome, usuario, senha, tipo):
    inserir_usuario(nome, usuario, senha, tipo)

def atualizar_usuario(id, nome, usuario, tipo):
    editar_usuario(id, nome, usuario, tipo)

def desativar_usuario_por_id(id):
    desativar_usuario(id)

def autenticar_usuario(usuario, senha):
    """
    Verifica se há um usuário ativo com login e senha correspondentes.
    """
    usuarios = listar_todos()
    for u in usuarios:
        # u[2] = usuario | u[3] = senha | u[5] = ativo (1 ou 0)
        if u[2].strip().lower() == usuario.strip().lower() and u[3] == senha and u[5] == 1:
            return True
    return False
