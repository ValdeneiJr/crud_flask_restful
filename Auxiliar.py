def produto_para_json(produto):
    return {
        "id": produto.id,
        "nome": produto.nome,
        "descricao": produto.descricao
    }