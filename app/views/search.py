from flask import (
    Blueprint, request
)

from app.models.universities import UniversityInfo
from app.extensions import postgres_db

import traceback
import json

from flask_sqlalchemy import SQLAlchemy

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/universities', methods=["POST"])
def view():
    try:
        return_list = []
        request_json = request.get_json()
        
        query = """ Select  
                        * from university_info
                    Where 
                        name like \'%{}%\' 
                """.format(request_json.get('name', ''),)

        
        if request_json.get('country_codes', False):
            alpha_two_codes = '('
            for each in request_json.get('country_codes'):
                alpha_two_codes += '\'' + str(each) + '\'' ','
            if alpha_two_codes[-1] == ',':
                alpha_two_codes = alpha_two_codes[:-1]
            alpha_two_codes += ')'
            
            query += """AND
                            alpha_two_code in {}""".format(alpha_two_codes)

        if request_json.get('domains', False):
            domains = '\'('
            for each in request_json.get('domains'):
                domains += str(each) + '|'
            if domains[-1] == '|':
                domains = domains[:-1]
            domains += ')\''

            query += """AND
                            domain ~ {}""".format(domains)

        offset = int(request_json.get('offset', '0'))
        limit = int(request_json.get('limit', '10'))
        query += ''' limit {} offset {}'''.format(limit, offset) 
        result = postgres_db.session.execute(query)

        for each in result:
            aux_dict = {}
            aux_dict['id'] = each[0]
            aux_dict['alpha_two_code'] = each[1]
            aux_dict['country'] = each[2]
            aux_dict['domain'] = each[3]
            aux_dict['name'] = each[4]
            aux_dict['web_page'] = each[5]
            return_list.append(aux_dict)
        
        return json.dumps(return_list)

    except:
        traceback.print_exc()
        return 'Something went wrong.'