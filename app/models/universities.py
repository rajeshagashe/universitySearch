from app.extensions import postgres_db
import datetime

class UniversityInfo(postgres_db.Model):
    id = postgres_db.Column(postgres_db.Integer, primary_key=True)
    alpha_two_code = postgres_db.Column(postgres_db.String())
    country = postgres_db.Column(postgres_db.String())
    domain = postgres_db.Column(postgres_db.String())
    sub_domain = postgres_db.Column(postgres_db.String())
    name = postgres_db.Column(postgres_db.String())
    web_page = postgres_db.Column(postgres_db.String())

    enabled = postgres_db.Column(postgres_db.Boolean, default = True)
    deleted = postgres_db.Column(postgres_db.Boolean, default = False)
    created_at = postgres_db.Column(postgres_db.DateTime, default=datetime.datetime.now)
    updated_at = postgres_db.Column(postgres_db.DateTime, default=datetime.datetime.now)

    def to_json(self):
        return_dict = {}
        return_dict['id'] = self.id
        return_dict['alpha_two_code'] = self.alpha_two_code
        return_dict['country'] = self.country
        return_dict['domain'] = self.domain
        return_dict['name'] = self.name
        return_dict['web_page'] = self.web_page

        return return_dict
