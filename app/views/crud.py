from flask import (
    Blueprint, request
)

from app.models.universities import UniversityInfo
from app.extensions import postgres_db

import traceback
import datetime

crud_blueprint = Blueprint('crud', __name__)

@crud_blueprint.route('/create', methods=["POST"])
def create():
    try:
        entry = UniversityInfo()
        request_json = request.get_json()
        
        entry.alpha_two_code = request_json['alpha_two_code']
        entry.country = request_json['country']
        entry.domain = request_json['domain']
        entry.name = request_json['name']
        entry.web_page = request_json['web_page']
                
        postgres_db.session.add(entry)
        postgres_db.session.commit()

        return entry.to_json()
    except:
        postgres_db.session.rollback()
        traceback.print_exc()
        return "Something went wrong"
        
@crud_blueprint.route('/read/<int:record_id>', methods=["GET"])
def read(record_id):
    try:
        row = UniversityInfo.query.get(record_id)
        postgres_db.session.commit()
        
        return row.to_json()
    except:
        postgres_db.session.rollback()
        traceback.print_exc()
        return "Something went wrong"

@crud_blueprint.route('/update/<int:record_id>', methods=["PATCH"])
def update(record_id):
    try:
        request_json = request.get_json()
        request_json['updated_at'] = datetime.datetime.now()
        row = UniversityInfo.query.filter_by(id=record_id)
        row.update(request_json)
        postgres_db.session.commit()

        return row.first().to_json()
    except:
        postgres_db.session.rollback()
        traceback.print_exc()
        return "Something went wrong"

@crud_blueprint.route('/delete/<int:record_id>', methods=["DELETE"])
def delete(record_id):
    try:
        row = UniversityInfo.query.filter_by(id=record_id)
        return_dict = row.first().to_json()
        row.delete()
        postgres_db.session.commit()

        return return_dict
    except:
        postgres_db.session.rollback()
        traceback.print_exc()
        return "Something went wrong"



