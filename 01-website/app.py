from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import csv
#import psycopg2

app = Flask(__name__)


@app.route('/')
def return_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def return_pages(page_name):
    return render_template(page_name)


# Write to txt func
def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        message_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file = database.write(f'\n{email} | {subject} | {message} | {message_time} ')
    

# Write to csv func
def write_to_csv(data):
    with open('database_csv.csv', newline='', mode='a') as database_csv:
        email = data['email']
        subject = data['subject']
        message = data['message']
        message_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        csv_writer = csv.writer(database_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message,message_time])

## Write to database func
#def write_to_db(data):
    ## Database connection parameters
    #db_config = {
        #'dbname': 'mypg-db',
        #'user': 'kika',
        #'password': 'securepswd',
        #'host': 'host-host-bc',
        #'port': '5432'  # Default port is 5432
    #}
    
    #try:
        ## Connect to the PostgreSQL database
        #conn = psycopg2.connect(**db_config)
        #cursor = conn.cursor()
        
        ## Extract data
        #email = data['email']
        #subject = data['subject']
        #message = data['message']
        #time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        ## SQL query to insert data
        #insert_query = """
        #INSERT INTO your_table_name (email, subject, message, time)
        #VALUES (%s, %s, %s, %s); # To prevent SQL injection
        #"""
        
        ## Execute the query and commit the transaction
        #cursor.execute(insert_query, (email, subject, message, time))
        #conn.commit()
        
    #except Exception as error:
    #    print(f"Error: {error}")
    #finally:
        ## Close the cursor and connection
        #cursor.close()
        #conn.close()


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_file(data)
            write_to_csv(data)
            ## Database write
            #write_to_db(data)     
            return redirect('/thankyou.html')
        except:
            return 'Something went wrong with writing the data'
    else: 
        return 'Something went wrong. Try again.'
