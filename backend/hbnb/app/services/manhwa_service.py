# app/services/manhwa_service.py
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

ns = Namespace('manhwas', description='Manhwa operations')

# ---------------- Modèles Swagger ----------------
manhwa_create_model = ns.model('ManhwaCreate', {
    'title': fields.String(required=True, description='Titre', example='Solo Leveling'),
    'description': fields.String(description='Synopsis', example='Un chasseur de rang E devient le plus fort'),
    'author': fields.String(description='Auteur', example='Chugong'),
    'status': fields.String(description='Statut', example='completed'),
    'cover_image': fields.String(description='URL de la couverture', example='https://example.com/cover.jpg')
})

manhwa_update_model = ns.model('ManhwaUpdate', {
    'title': fields.String(description='Titre', example='Solo Leveling'),
    'description': fields.String(description='Synopsis', example='Nouveau synopsis'),
    'author': fields.String(description='Auteur', example='Chugong'),
    'status': fields.String(description='Statut', example='ongoing'),
    'cover_image': fields.String(description='URL de la couverture', example='https://example.com/cover2.jpg')
})


@ns.route('/')
class ManhwaList(Resource):
    def get(self):
        """Retourne tous les manhwas (public)"""
        manhwas = current_app.facade.get_manhwas()
        return [m.to_dict() for m in manhwas], 200

    @jwt_required()
    @ns.expect(manhwa_create_model)
    def post(self):
        """Crée un nouveau manhwa (authentifié)"""
        data = request.get_json(silent=True)
        if not data:
            return {"error": "No input data provided"}, 400
        if 'title' not in data:
            return {"error": "title is required"}, 400
        user_id = get_jwt_identity()
        data['owner_id'] = user_id
        new_manhwa = current_app.facade.create_manhwa(data)
        return new_manhwa.to_dict(), 201


@ns.route('/<string:manhwa_id>')
class ManhwaResource(Resource):
    def get(self, manhwa_id):
        """Retourne un manhwa par ID (public)"""
        manhwa = current_app.facade.get_manhwa(manhwa_id)
        if not manhwa:
            return {"error": "Manhwa not found"}, 404
        return manhwa.to_dict(), 200

    @jwt_required()
    @ns.expect(manhwa_update_model)
    def put(self, manhwa_id):
        """Met à jour un manhwa existant (propriétaire ou admin)"""
        manhwa = current_app.facade.get_manhwa(manhwa_id)
        if not manhwa:
            return {"error": "Manhwa not found"}, 404
        user_id = get_jwt_identity()
        current_user = current_app.facade.get_user(user_id)
        if not current_user.is_admin and manhwa.owner_id != user_id:
            return {"error": "Forbidden: not the owner"}, 403
        data = request.get_json(silent=True)
        if not data:
            return {"error": "No input data provided"}, 400
        updated_manhwa = current_app.facade.update_manhwa(manhwa_id, data)
        return updated_manhwa.to_dict(), 200

    @jwt_required()
    def delete(self, manhwa_id):
        """Supprime un manhwa existant (propriétaire ou admin)"""
        manhwa = current_app.facade.get_manhwa(manhwa_id)
        if not manhwa:
            return {"error": "Manhwa not found"}, 404
        user_id = get_jwt_identity()
        current_user = current_app.facade.get_user(user_id)
        if not current_user.is_admin and manhwa.owner_id != user_id:
            return {"error": "Forbidden: not the owner"}, 403
        success = current_app.facade.delete_manhwa(manhwa_id)
        if not success:
            return {"error": "Manhwa could not be deleted"}, 400
        return {"message": "Manhwa deleted"}, 200
