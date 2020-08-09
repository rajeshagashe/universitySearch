from app.extensions import postgres_db
import datetime

class UniversityInfo(postgres_db.Model):
    id = postgres_db.Column(postgres_db.Integer, primary_key=True)
    alpha_two_code = postgres_db.Column(postgres_db.String())
    country = postgres_db.Column(postgres_db.String())
    domain = postgres_db.Column(postgres_db.String())
    name = postgres_db.Column(postgres_db.String())
    web_page = postgres_db.Column(postgres_db.String())

    enabled = postgres_db.Column(postgres_db.Boolean, default = True)
    deleted = postgres_db.Column(postgres_db.Boolean, default = False)
    created_at = postgres_db.Column(postgres_db.DateTime, default=datetime.datetime.now)
    updated_at = postgres_db.Column(postgres_db.DateTime, default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        """Triggered when the document is saved, updates the fields"""
        print('_____________________________________________')
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        super().save()