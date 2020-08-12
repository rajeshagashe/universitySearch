# to do - manage http status codes
from flask import (
    Blueprint, request
)

from app.models.universities import UniversityInfo
from app.extensions import postgres_db

import traceback
import datetime
import json

crud_blueprint = Blueprint('crud', __name__)

@crud_blueprint.route('/create', methods=["POST"])
def create():
    try:
        entry = UniversityInfo()
        request_json = request.get_json()
        
        entry.alpha_two_code = request_json['alpha_two_code']
        entry.country = request_json['country']
        entry.domain = request_json['domain']
        entry.sub_domain = get_sub_domain(entry.domain)
        entry.name = request_json['name']
        entry.web_page = request_json['web_page']
                
        postgres_db.session.add(entry)
        postgres_db.session.commit()

        return json.dumps([entry.to_json()])
    except:
        postgres_db.session.rollback()
        traceback.print_exc()
        return "Something went wrong"
        
@crud_blueprint.route('/read', methods=["GET"])
@crud_blueprint.route('/read/<int:record_id>', methods=["GET"])
def read(record_id=None):
    try:
        if not record_id:
            row = UniversityInfo.query.all()
            response = list()
            for i in row:
                response.append(i.to_json()) 
            postgres_db.session.commit()
            return json.dumps(response)
        else:
            row = UniversityInfo.query.get(record_id)
        
        return json.dumps([row.to_json()])
    except:
        traceback.print_exc()
        return "Something went wrong"

@crud_blueprint.route('/update/<int:record_id>', methods=["PATCH"])
def update(record_id):
    try:
        request_json = request.get_json()
        request_json['updated_at'] = datetime.datetime.now()
        if request_json.get('domain', False):
            domain = request_json.get('domain')
            request_json['sub_domain'] = get_sub_domain(domain)

        if request_json.get("id", False):
            request_json.pop("id") # id must not be updated.
        row = UniversityInfo.query.filter_by(id=record_id)
        row.update(request_json)
        postgres_db.session.commit()

        return json.dumps([row.first().to_json()])
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

        return json.dumps([return_dict])
    except:
        postgres_db.session.rollback()
        traceback.print_exc()
        return "Something went wrong"



def get_sub_domain(domain):
    sub_domain = '.' + domain.split('.')[-1]
    return sub_domain