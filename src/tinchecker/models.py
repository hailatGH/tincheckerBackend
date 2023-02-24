from tinchecker import db


class TaxPayerInfo(db.Model):
    tin = db.Column(db.String(255), primary_key=True)
    city = db.Column(db.String(255))
    woreda = db.Column(db.String(255))
    district = db.Column(db.String(255))
    region = db.Column(db.String(255))
    street_num = db.Column(db.String(255))
    tax_center_num = db.Column(db.String(255))
    telephone_num = db.Column(db.String(255))
    tax_payer_name = db.Column(db.String(255))
    tax_payer_name_amh = db.Column(db.String(255))
