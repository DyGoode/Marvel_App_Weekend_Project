from flask import Blueprint, request, jsonify
from marvel_combat_mania.helpers import token_required
from marvel_combat_mania.models import db, MarvelCharacter, marvel_character_schema, marvel_characters_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value'}

@api.route('/marvel_characters', methods = ['POST'])
@token_required
def create_marvel_character(current_user_token):
    name = request.json['name']
    alias = request.json['alias'] 
    powers = request.json['powers']
    history = request.json['history']
    allegiance = request.json['allegiance']
    user_token = current_user_token.token

    print(f'User Token: {current_user_token.token}')

    marvel_character = MarvelCharacter(name, alias, powers, history, allegiance, user_token=user_token)

    db.session.add(marvel_character)
    db.session.commit()

    response = marvel_character_schema.dump(marvel_character)
    return jsonify(response)


@api.route('/marvel_characters', methods = ['GET'])
@token_required
def get_marvel_characters(current_user_token):
    owner = current_user_token.token 
    marvel_characters = MarvelCharacter.query.filter_by(user_token=owner).all()
    response = marvel_characters_schema.dump(marvel_characters)
    return jsonify(response)


@api.route('/marvel_characters/<id>', methods = ['GET'])
@token_required
def get_marvel_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        marvel_character = MarvelCharacter.query.get(id)
        response = marvel_character_schema.dump(marvel_character)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


@api.route('/marvel_characters/<id>', methods = ['POST', 'PUT'])
@token_required
def update_marvel_character(current_user_token, id):
    marvel_character = MarvelCharacter.query.get(id)
    marvel_character.name = request.json['name']
    marvel_character.alias = request.json['alias'] 
    marvel_character.powers = request.json['powers']
    marvel_character.history = request.json['history']
    marvel_character.allegiance = request.json['allegiance']
    marvel_character.user_token = current_user_token.token

    db.session.commit()
    response = marvel_character_schema.dump(marvel_character)
    return jsonify(response)



@api.route('/marvel_characters/<id>', methods = ['DELETE'])
@token_required
def delete_marvel_character(current_user_token, id):
    marvel_character = MarvelCharacter.query.get(id)
    
    db.session.delete(marvel_character)
    db.session.commit()
    response = marvel_character_schema.dump(marvel_character)
    return jsonify(response)