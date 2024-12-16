from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

# Configurando a aplicação Flask e o banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\valde\PycharmProjects\PythonProject\task_irma\produtos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

# Modelo da entidade Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)

def produto_para_json(produto):
    return {
        "id": produto.id,
        "nome": produto.nome,
        "descricao": produto.descricao
    }

# Rota para CRUD de produtos
class ProdutoResource(Resource):
    def get(self, produto_id=None):
        if produto_id:
            produto = Produto.query.get(produto_id)
            if produto:
                return produto_para_json(produto), 200
            return {"message": "Produto não encontrado"}, 404

        produtos = Produto.query.all()
        return [produto_para_json(produto) for produto in produtos], 200

    def post(self):
        dados = request.json
        novo_produto = Produto(
            nome=dados.get('nome'),
            descricao=dados.get('descricao')
        )
        db.session.add(novo_produto)
        db.session.commit()
        return produto_para_json(novo_produto), 201

    def put(self, produto_id):
        produto = Produto.query.get(produto_id)
        if not produto:
            return {"message": "Produto não encontrado"}, 404

        dados = request.json
        produto.nome = dados.get('nome', produto.nome)
        produto.descricao = dados.get('descricao', produto.descricao)
        db.session.commit()
        return produto_para_json(produto), 200

    def delete(self, produto_id):
        produto = Produto.query.get(produto_id)
        if not produto:
            return {"message": "Produto não encontrado"}, 404

        db.session.delete(produto)
        db.session.commit()
        return {"message": "Produto deletado com sucesso"}, 200

# Adicionando as rotas na API
api.add_resource(ProdutoResource, '/produtos', '/produtos/<int:produto_id>')

# Inicializando o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
