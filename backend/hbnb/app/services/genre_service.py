# app/services/genre_service.py
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from app.auth.decorators import admin_required

ns = Namespace('genres', description='Genre operations')

# ---------------- Modèles Swagger ----------------
genre_create_model = ns.model('GenreCreate', {
    'name': fields.String(required=True, description='Nom', example='Action'),
    'description': fields.String(description='Description', example='Combats et aventures')
})

genre_update_model = ns.model('GenreUpdate', {
    'name': fields.String(description='Nom', example='Fantasy'),
    'description': fields.String(description='Description', example='Mondes imaginaires et magie')
})


@ns.route('/')
class GenreList(Resource):
    def get(self):
        """Retourne tous les genres"""
        genres = current_app.facade.get_genres()
        return [g.to_dict() for g in genres], 200

    @admin_required
    @ns.expect(genre_create_model)
    def post(self):
        """Crée un nouveau genre (admin seulement)"""
        data = request.get_json(silent=True)
        if not data:
            return {"error": "No input data provided"}, 400
        new_genre = current_app.facade.create_genre(data)
        return new_genre.to_dict(), 201


@ns.route('/<string:genre_id>')
class GenreResource(Resource):
    def get(self, genre_id):
        """Retourne un genre par ID"""
        genres = current_app.facade.get_genres()
        item = next((g.to_dict() for g in genres if g.id == genre_id), None)
        if not item:
            return {"error": "Genre not found"}, 404
        return item, 200

    @admin_required
    @ns.expect(genre_update_model)
    def put(self, genre_id):
        """Met à jour un genre (admin seulement)"""
        data = request.get_json(silent=True)
        if not data:
            return {"error": "No input data provided"}, 400
        updated = current_app.facade.update_genre(genre_id, data)
        if not updated:
            return {"error": "Genre not found"}, 404
        return updated.to_dict(), 200

    @admin_required
    def delete(self, genre_id):
        """Supprime un genre (admin seulement)"""
        success = current_app.facade.delete_genre(genre_id)
        if not success:
            return {"error": "Genre not found"}, 404
        return {"message": "Genre deleted"}, 200
