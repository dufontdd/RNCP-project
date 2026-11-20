# app/services/review_service.py
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

ns = Namespace('reviews', description='Operations related to reviews')

# ---------------- Modèles Swagger ----------------
review_create_model = ns.model('ReviewCreate', {
    'text': fields.String(required=True, description='Texte de la review', example='Super manhwa !'),
    'rating': fields.Integer(description='Note de 1 à 5', example=5),
    'manhwa_id': fields.String(required=True, description='ID du manhwa', example='aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')
})

review_update_model = ns.model('ReviewUpdate', {
    'text': fields.String(description='Texte de la review', example='Vraiment top !'),
    'rating': fields.Integer(description='Note de 1 à 5', example=4)
})

@ns.route('/')
class ReviewList(Resource):
    def get(self):
        """Retourne toutes les reviews (public)"""
        reviews = current_app.facade.get_reviews()
        return [r.to_dict() for r in reviews], 200

    @jwt_required()
    @ns.expect(review_create_model)
    def post(self):
        """Crée une nouvelle review (authentifié)"""
        data = request.get_json(silent=True)
        if not data:
            return {"error": "No input data provided"}, 400
        required_fields = ['text', 'manhwa_id']
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400
        if 'rating' in data and data['rating'] is not None:
            if not isinstance(data['rating'], int) or not 1 <= data['rating'] <= 5:
                return {"error": "rating must be an integer between 1 and 5"}, 400
        user_id = get_jwt_identity()
        data['user_id'] = user_id
        manhwa = current_app.facade.get_manhwa(data['manhwa_id'])
        if not manhwa:
            return {"error": "Manhwa not found"}, 404
        existing_review = current_app.facade.get_review_by_user_and_manhwa(user_id, data['manhwa_id'])
        if existing_review:
            return {"error": "You have already reviewed this manhwa"}, 400
        review = current_app.facade.create_review(data)
        return review.to_dict(), 201

@ns.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Récupère une review par son ID (public)"""
        review = current_app.facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @jwt_required()
    @ns.expect(review_update_model)
    def put(self, review_id):
        """Met à jour une review existante (auteur ou admin)"""
        review = current_app.facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        user_id = get_jwt_identity()
        current_user = current_app.facade.get_user(user_id)
        if not current_user.is_admin and review.user_id != user_id:
            return {"error": "Forbidden: not the author"}, 403
        data = request.get_json(silent=True)
        if not data:
            return {"error": "No input data provided"}, 400
        if 'rating' in data and data['rating'] is not None:
            if not isinstance(data['rating'], int) or not 1 <= data['rating'] <= 5:
                return {"error": "rating must be an integer between 1 and 5"}, 400
        review = current_app.facade.update_review(review_id, data)
        return review.to_dict(), 200

    @jwt_required()
    def delete(self, review_id):
        """Supprime une review existante (auteur ou admin)"""
        review = current_app.facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        user_id = get_jwt_identity()
        current_user = current_app.facade.get_user(user_id)
        if not current_user.is_admin and review.user_id != user_id:
            return {"error": "Forbidden: not the author"}, 403
        current_app.facade.delete_review(review_id)
        return {"message": "Review deleted"}, 200
