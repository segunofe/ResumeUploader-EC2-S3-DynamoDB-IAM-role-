from flask import Flask, request, render_template  # import Flask for the web app
import boto3 # boto3 is python tool (SDK) to interact with AWS services like S3, DynamoDB, 
import datetime  # to get current date and time
import uuid  # Ensures every record is uniquely identifiable

              # Helps DynamoDB use it as a Primary Key to retrieve or prevent duplicates

app = Flask(__name__)

# AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Constants
BUCKET_NAME = 'new-resume123'  # Replace with your S3 bucket
TABLE_NAME = 'applicants'      # Replace with your DynamoDB table name

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    email = request.form['email']
    resume = request.files['resume']

    if resume:
        # Generate unique filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # This line gets the current date and time, and formats it into a specific string format.Y4digit, m00-12, d00-31, H00-23, M00-59, S00-59
        filename = f"{name.replace(' ', '_')}_{timestamp}_{resume.filename}"  # name of applicant, replace space between name with _, time the resume was uploaded and 

        # Upload to S3
        s3.upload_fileobj(resume, BUCKET_NAME, filename)  # Take this file object called resume and upload it to the bucket named BUCKET_NAME, and save it with the name filename.
                                                            # upload_fileobj is a method used to upload file-like objects, not a file path
        # Save to DynamoDB
        table = dynamodb.Table(TABLE_NAME)  # is how your Python code knows which DynamoDB table to talk to. Since inside a database, you can have different tables
        
        # the below code shows that we used this "table" object to insert a new item (record) into your DynamoDB table — basically, it's saving applicant data.
        table.put_item(Item={
            'id': str(uuid.uuid4()),  # uuid.uuid4() generates a random universally unique identifier (UUID).
            'name': name,
            'email': email,
            'resume_filename': filename,
            'uploaded_at': timestamp
        })



        return f"Thank you {name}, your resume has been uploaded successfully!"

    return "Upload failed. Please try again."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

