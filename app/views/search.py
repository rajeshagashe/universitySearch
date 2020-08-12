from flask import (
    Blueprint, request
)

from app.models.universities import UniversityInfo
from app.extensions import postgres_db

import traceback
import json

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/universities', methods=["POST"])
def view():
    try:
        return_list = []
        request_json = request.get_json()

        name = request_json.get('name', '') 
        alpha_two_codes = request_json.get('country_codes', []) 
        domains = request_json.get('domains', [])
        offset = int(request_json.get('offset', '0'))
        limit = int(request_json.get('limit', '10'))
        
        search = "%{}%".format(name)
        response = UniversityInfo.query.filter(UniversityInfo.name.like(search))   
        
        if domains:
            response = response.filter(UniversityInfo.sub_domain.in_(set(domains)))

        if alpha_two_codes:
            response = response.filter(UniversityInfo.alpha_two_code.in_(set(alpha_two_codes)))

        response = response.offset(offset).limit(limit)

        for each in response.all():
            return_list.append(each.to_json())
        
        return json.dumps(return_list)

    except:
        traceback.print_exc()
        return 'Something went wrong.'