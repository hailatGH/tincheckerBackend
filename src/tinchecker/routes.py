from flask import jsonify, request

from tinchecker import app, db
from tinchecker.models import *


@app.route('/tinchecker', methods=['GET'])
def get_all_tax_payers():
    tax_payers = TaxPayerInfo.query.all()

    if not tax_payers:
        return jsonify({'message': 'No Tax Payer Found!'})

    output = []
    for tax_payer in tax_payers:
        tax_payer_data = {}
        tax_payer_data['tin'] = tax_payer.tin
        tax_payer_data['city'] = tax_payer.city
        tax_payer_data['woreda'] = tax_payer.woreda
        tax_payer_data['district'] = tax_payer.district
        tax_payer_data['region'] = tax_payer.region
        tax_payer_data['street_num'] = tax_payer.street_num
        tax_payer_data['tax_payer_name'] = tax_payer.tax_payer_name
        tax_payer_data['tax_payer_name_amh'] = tax_payer.tax_payer_name_amh
        output.append(tax_payer_data)
    return jsonify({'tax_payers': output})


@app.route('/tinchecker/<tin>', methods=['GET'])
def get_one_tax_payers(tin):
    tax_payer = TaxPayerInfo.query.filter_by(tin=tin).first()

    if not tax_payer:
        return jsonify({'message': 'No Tax Payer Found!'})

    tax_payer_data = {}
    tax_payer_data['tin'] = tax_payer.tin
    tax_payer_data['city'] = tax_payer.city
    tax_payer_data['woreda'] = tax_payer.woreda
    tax_payer_data['district'] = tax_payer.district
    tax_payer_data['region'] = tax_payer.region
    tax_payer_data['street_num'] = tax_payer.street_num
    tax_payer_data['tax_payer_name'] = tax_payer.tax_payer_name
    tax_payer_data['tax_payer_name_amh'] = tax_payer.tax_payer_name_amh

    return jsonify({'tax_payer': tax_payer_data})


@app.route('/tinchecker', methods=['POST'])
def create_tax_payers():
    tax_payer_data = request.get_json()

    new_tax_payer = TaxPayerInfo(
        tin=tax_payer_data['tin'],
        city=tax_payer_data['city'],
        woreda=tax_payer_data['woreda'],
        district=tax_payer_data['district'],
        region=tax_payer_data['region'],
        street_num=tax_payer_data['street_num'],
        tax_payer_name=tax_payer_data['tax_payer_name'],
        tax_payer_name_amh=tax_payer_data['tax_payer_name_amh']
    )

    db.session.add(new_tax_payer)
    db.session.commit()

    return jsonify({'message': 'New Tax Payer created!'})


# @app.route('/tinchecker/<tin>', methods=['PUT'])
# def update_tax_payers(tin):

#     tax_payer = TaxPayerInfo.query.filter_by(tin=tin).first()

#     if not tax_payer:
#         return jsonify({'message': 'No Tax Payer found!'})

#     db.session.commit()

#     return jsonify({'message': 'The Tax Payer info has been updated!'})


@app.route('/tinchecker/<tin>', methods=['DELETE'])
def delete_tax_payers(tin):

    tax_payer = TaxPayerInfo.query.filter_by(tin=tin).first()

    if not tax_payer:
        return jsonify({'message': 'No Tax Payer found!'})

    db.session.delete(tax_payer)
    db.session.commit()

    return jsonify({'message': 'The Tax Payer has been deleted!'})
