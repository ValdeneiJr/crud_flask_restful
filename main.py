from flask import Flask, request, jsonify
from flask_restful import Api, Resource

from Repository import ProdutoRepository
from DataBaseConfig import get_db
from Model import Produto
from Auxiliar import produto_para_json

app = Flask(__name__)
api = Api(app)

# Rota para CRUD de produtos
class ProdutoResource(Resource):
    def get(self, produto_id=None):
        with next(get_db()) as db:
            if produto_id:
                produto = ProdutoRepository.find_by_id(db, produto_id)
                if produto:
                    return produto_para_json(produto), 200
                return {"message": "Produto não encontrado"}, 404

            produtos = ProdutoRepository.find_all(db)
            return [produto_para_json(produto) for produto in produtos], 200

    def post(self):
        with next(get_db()) as db:
            dados = request.json
            novo_produto = Produto(
                nome=dados.get('nome'),
                descricao=dados.get('descricao')
            )
            ProdutoRepository.save(db, novo_produto)
            return produto_para_json(novo_produto), 201

    def put(self, produto_id):
        with next(get_db()) as db:
            produto = ProdutoRepository.find_by_id(db, produto_id)
            if not produto:
                return {"message": "Produto não encontrado"}, 404

            dados = request.json
            produto.nome = dados.get('nome', produto.nome)
            produto.descricao = dados.get('descricao', produto.descricao)
            ProdutoRepository.save(db, produto)
            return produto_para_json(produto), 200

    def delete(self, produto_id):
        with next(get_db()) as db:
            produto = ProdutoRepository.find_by_id(db, produto_id)
            if not produto:
                return {"message": "Produto não encontrado"}, 404

            ProdutoRepository.delete_by_id(db, produto_id)
            return {"message": "Produto deletado com sucesso"}, 200

api.add_resource(ProdutoResource, '/produtos', '/produtos/<int:produto_id>')

if __name__ == '__main__':
    app.run(debug=True)
