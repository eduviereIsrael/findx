from ast import Pass
from nturl2path import url2pathname
from flask import render_template,request,redirect,url_for, send_file
from application import app
from bs4 import BeautifulSoup
import requests
import pandas as pd

docs = ''
business_name = ''

def url_setting(x):
    result = ''
    for i in x:
        if i == ' ':
            i = '-'
        result += i
    return result

def fetch_details(url):
    business_res = []
    website = requests.get(url)
    website_data = BeautifulSoup(website.text, 'html.parser')
    business_res_div = website_data.find_all(['div'], class_='with_img')

    base_url = 'https://www.businesslist.com.ng'

    data = []

    for item in business_res_div:
        found_name = item.find(['a'])
        res_source = found_name['href']
        # print(base_url+res_source)
        item_url = base_url+res_source
        item_page = requests.get(item_url)
        item_data = BeautifulSoup(item_page.text, "html.parser")
        item_name = item_data.find(id='company_name')
        item_address_div = item_data.find(class_='location')
        item_address = item_address_div.get_text()
        item_contact_div = item_data.find(class_='phone')
        item_contact = item_contact_div.get_text()
        data.append({'name': item_name.string, 'address': item_address, 'number': item_contact})
        print('---------------------------------------------------')
        print(data)
        # print(item_address_div)
        print('---------------------------------------------------')
        business_res.append(found_name.string)
    return data

@app.route('/home')
@app.route('/')
def home():
    req_method = request.method
    return render_template('index.html', req_method = req_method)


@app.route('/search', methods = ['POST'])
def result():
    f_business = request.form['business'].lower()

    f_location = request.form['location'].lower()

    business = url_setting(f_business)

    location = url_setting(f_location)

    url = f'https://www.businesslist.com.ng/category/{business}/city:{location}'
    alt_url =  f'https://www.businesslist.com.ng/companies/{business}/city:{location}'

    if not location:
        url = f'https://www.businesslist.com.ng/category/{business}'
        alt_url = f'https://www.businesslist.com.ng/companies/{business}'

    if not business:
        url = f'https://www.businesslist.com.ng/location/{location}'
        alt_url = f'https://www.businesslist.com.ng/location/{location}'

    result = fetch_details(url)
    if not result:
        result = fetch_details(alt_url)

    if not result:
        result = False
    names = []
    address = []
    contact = []

    if result:
        for i in result:
            names.append(i['name'])
            address.append(i['address'])
            contact.append(i['number'])

    docs = pd.DataFrame({"Name": names, "Address": address, "Contact": contact})

    docs.to_csv(f'application/results.csv', index=False, encoding='utf-8')
    
    return render_template('result.html', data = [result, f_business])

@app.route('/download')
def download():
    return send_file('results.csv', as_attachment=True)
