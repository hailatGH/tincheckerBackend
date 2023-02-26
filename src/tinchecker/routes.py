# Community library imports
from flask import jsonify
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup


# Local imports
from tinchecker import app, db
from tinchecker.models import *


# Constants
URL = "http://www.erca.gov.et:8008/wserca/index.jsf?tin="


# API Routes
@app.route('/tinchecker/<tin>', methods=['GET'])
def get_all_tax_payers(tin):
    
    if tin:
        tax_payers = TaxPayerInfo.query.filter(TaxPayerInfo.tin.contains(tin))

    if not tax_payers:
        return jsonify({'message': 'No Tax Payer Found!'})
    
    if tax_payers.count() == 0:
        output = []
        tax_payer_data = {}
        dict = {
            "id": "null",
            "CITYNAME": "null",
            "KEBELEDESC": "null",
            "LOCALITYDESC": "null",
            "PARISHNAME": "null",
            "STREETNO": "null",
            "TAXCENTRENO": "null",
            "TELPHONE": "null",
            "TPNAME": "null",
            "TPNAME_F": "null",
            "TPNAME_S": "null"
        }

        remote_tax_payer_data = list(ET.fromstring(BeautifulSoup(requests.get(URL + tin).text, 'lxml').body.text.strip()))

        for data in remote_tax_payer_data:
            dict[data.tag] = data.text

        print(dict)

        new_tax_payer = TaxPayerInfo(
            tin=dict['id'],
            city=dict["CITYNAME"],
            woreda=dict["KEBELEDESC"],
            district=dict["LOCALITYDESC"],
            region=dict["PARISHNAME"],
            street_num=dict["STREETNO"],
            tax_center_num=dict["TAXCENTRENO"],
            telephone_num=dict["TELPHONE"],
            tax_payer_name=dict["TPNAME"],
            tax_payer_name_amh=dict["TPNAME_S"]
        )
        db.session.add(new_tax_payer)
        db.session.commit()
        
        tax_payer = TaxPayerInfo.query.filter_by(tin=tin).first()

        tax_payer_data['tin'] = tax_payer.tin
        tax_payer_data['city'] = tax_payer.city
        tax_payer_data['woreda'] = tax_payer.woreda
        tax_payer_data['district'] = tax_payer.district
        tax_payer_data['region'] = tax_payer.region
        tax_payer_data['street_num'] = tax_payer.street_num
        tax_payer_data['tax_center_num'] = tax_payer.tax_center_num,
        tax_payer_data['telephone_num'] = tax_payer.telephone_num,
        tax_payer_data['tax_payer_name'] = tax_payer.tax_payer_name
        tax_payer_data['tax_payer_name_amh'] = tax_payer.tax_payer_name_amh
        output.append(tax_payer_data)

        return jsonify({'tax_payer': output})

    output = []
    for tax_payer in tax_payers:
        tax_payer_data = {}

        tax_payer_data['tin'] = tax_payer.tin
        tax_payer_data['city'] = tax_payer.city
        tax_payer_data['woreda'] = tax_payer.woreda
        tax_payer_data['district'] = tax_payer.district
        tax_payer_data['region'] = tax_payer.region
        tax_payer_data['street_num'] = tax_payer.street_num
        tax_payer_data['tax_center_num']= tax_payer.tax_center_num,
        tax_payer_data['telephone_num']= tax_payer.telephone_num,
        tax_payer_data['tax_payer_name'] = tax_payer.tax_payer_name
        tax_payer_data['tax_payer_name_amh'] = tax_payer.tax_payer_name_amh    
        output.append(tax_payer_data)

    return jsonify({'tax_payers': output})


# Custom Functions









# @app.route('/tinchecker', methods=['GET'])
# def get_all_tax_payers():
#     tax_payers = TaxPayerInfo.query.all()

#     if not tax_payers:
#         return jsonify({'message': 'No Tax Payer Found!'})

#     output = []
#     for tax_payer in tax_payers:
#         tax_payer_data = {}
#         tax_payer_data['tin'] = tax_payer.tin
#         tax_payer_data['city'] = tax_payer.city
#         tax_payer_data['woreda'] = tax_payer.woreda
#         tax_payer_data['district'] = tax_payer.district
#         tax_payer_data['region'] = tax_payer.region
#         tax_payer_data['street_num'] = tax_payer.street_num
#         tax_payer_data['tax_payer_name'] = tax_payer.tax_payer_name
#         tax_payer_data['tax_payer_name_amh'] = tax_payer.tax_payer_name_amh
#         output.append(tax_payer_data)
#     return jsonify({'tax_payers': output})


# @app.route('/tinchecker/<tin>', methods=['GET'])
# def get_one_tax_payers(tin):
#     tax_payer = TaxPayerInfo.query.filter_by(tin=tin).first()

#     if not tax_payer:
#         return jsonify({'message': 'No Tax Payer Found!'})

#     tax_payer_data = {}
#     tax_payer_data['tin'] = tax_payer.tin
#     tax_payer_data['city'] = tax_payer.city
#     tax_payer_data['woreda'] = tax_payer.woreda
#     tax_payer_data['district'] = tax_payer.district
#     tax_payer_data['region'] = tax_payer.region
#     tax_payer_data['street_num'] = tax_payer.street_num
#     tax_payer_data['tax_payer_name'] = tax_payer.tax_payer_name
#     tax_payer_data['tax_payer_name_amh'] = tax_payer.tax_payer_name_amh

#     return jsonify({'tax_payer': tax_payer_data})


# @app.route('/tinchecker', methods=['POST'])
# def create_tax_payers():
#     tax_payer_data = request.get_json()

#     new_tax_payer = TaxPayerInfo(
#         tin=tax_payer_data['tin'],
#         city=tax_payer_data['city'],
#         woreda=tax_payer_data['woreda'],
#         district=tax_payer_data['district'],
#         region=tax_payer_data['region'],
#         street_num=tax_payer_data['street_num'],
#         tax_payer_name=tax_payer_data['tax_payer_name'],
#         tax_payer_name_amh=tax_payer_data['tax_payer_name_amh']
#     )

#     db.session.add(new_tax_payer)
#     db.session.commit()

#     return jsonify({'message': 'New Tax Payer created!'})


# @app.route('/tinchecker/<tin>', methods=['DELETE'])
# def delete_tax_payers(tin):

#     tax_payer = TaxPayerInfo.query.filter_by(tin=tin).first()

#     if not tax_payer:
#         return jsonify({'message': 'No Tax Payer found!'})

#     db.session.delete(tax_payer)
#     db.session.commit()

#     return jsonify({'message': 'The Tax Payer has been deleted!'})
