from flask_restx import Namespace, Resource, fields
from flask import request
from backend.app.controllers import PagamentoController

api = Namespace('pagamentos', description='Operações relacionadas a pagamentos')

pagamento_model = api.model('Pagamento', {
    'forma_pagamento': fields.String(required=True, description='Forma de pagamento (ex: Cartão, Pix, Boleto)')
})

pagamento_response = api.clone('PagamentoResponse', pagamento_model, {
    'id': fields.String(required=True, description='ID do pagamento')
})

@api.route('/')
class PagamentoList(Resource):
    @api.marshal_list_with(pagamento_response)
    def get(self):
        return PagamentoController.listar_pagamentos()[0]

    @api.expect(pagamento_model)
    @api.response(201, 'Pagamento criado com sucesso!')
    def post(self):
        data = request.get_json()
        return PagamentoController.criar_pagamento(data)

@api.route('/<string:id_pagamento>')
@api.param('id_pagamento', 'ID do pagamento')
class PagamentoResource(Resource):
    @api.marshal_with(pagamento_response)
    def get(self, id_pagamento):
        return PagamentoController.buscar_pagamento_por_id(id_pagamento)[0]

    @api.expect(pagamento_model)
    def put(self, id_pagamento):
        data = request.get_json()
        return PagamentoController.atualizar_pagamento(id_pagamento, data)

    def delete(self, id_pagamento):
        return PagamentoController.deletar_pagamento(id_pagamento)