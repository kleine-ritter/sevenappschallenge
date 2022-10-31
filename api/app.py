from flask import Flask
import pymysql
from sqlalchemy import create_engine
import pandas as pd

#Creating the connection engine
app = Flask(__name__)

user = 'root'
passw = 'mysql'
host =  'localhost'
port = 3306 
schema = 'seven_apps'
database = 'seven_apps'

mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database, echo=False)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/avg-funding-by-person/<person_id>')
def avgFundingByPerson(person_id):
    
    sql = f'''   SELECT p.PERSON_ID, AVG(c.KNOWN_TOTAL_FUNDING) as avg_total_funding
                FROM people p
                INNER JOIN companies c
                ON UPPER(p.COMPANY_NAME) = UPPER(c.NAME)
                WHERE p.PERSON_ID = '{person_id}' '''
    
    
    results = pd.read_sql(sql=sql, con=mydb).to_json()

    return results

@app.route('/companies-by-person/<person_id>')
def companiesByPerson(person_id):

    sql = f'''  SELECT c.NAME
                FROM people p
                INNER JOIN companies c
                ON UPPER(p.COMPANY_NAME) = UPPER(c.NAME)
                WHERE p.PERSON_ID = '{person_id}' '''

    results = pd.read_sql(sql=sql, con=mydb).to_json()

    return results

@app.route('/investors-by-company/<company_linkedin_name>')
def investorsByCompany(company_linkedin_name):
    sql = f'''  SELECT NAME, COMPANY_LINKEDIN_NAMES, DESCRIPTION 
                FROM seven_apps.companies 
                where COMPANY_LINKEDIN_NAMES LIKE '%%{company_linkedin_name}%%';'''

    results = pd.read_sql(sql=sql, con=mydb).to_json()

    return results