import streamlit as st
import boto3
import os
import tempfile

st.set_page_config(page_title="AWS Services")

services=['Launch Instance','Start Instances','Stop Instances', 'Terminate Instances', 'S3 Upload', 'S3 Delete']
instancesList = ['dwrtfq1984wye7hgf', 'odwsutfhyr934287wyoth', 'woisufhtdgr934287qwy']


def list_s3_buckets():
    # Create an S3 client
    s3 = boto3.client('s3')
    try:
        # Get a list of all S3 buckets
        response = s3.list_buckets()

        # Extract bucket names from the response
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]

        return bucket_names
    except Exception as e:
        return f"Error listing S3 buckets: {e}"


def upload_to_s3(file_path, bucket_name, object_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file to the specified bucket
        s3.upload_file(file_path, bucket_name, object_name)
        return f"File uploaded successfully to s3://{bucket_name}/{object_name}"
    except Exception as e:
        return f"Error uploading file: {e}"

# Replace these values with your own
file_path = 'path/to/your/file.txt'
bucket_name = 'your-bucket-name'
object_name = 'file.txt'

# Call the function to upload the file
# upload_to_s3(file_path, bucket_name, object_name)

# print(list_s3_buckets())


service = st.selectbox(
    'Choose any Service',
     services)

if 'start_instances' not in st.session_state:
    st.session_state.start_instances = []


# Launch Instances
if service == 'Launch Instance':
    numbers = st.selectbox(
        'Enter the number of Instances',
        [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    
    launch = st.button('Launch')

# Start Instances
elif service == 'Start Instances':
    start_instances_list = []
    for instance in instancesList:
        check = st.checkbox(instance)
        if check:
            start_instances_list.append(instance)
    
    start_instances_list

    start = st.button('Start')
    
    # st.session_state.start_instances.append(start_instances_list)
    # st.session_state

# Stop Instances
elif service == 'Stop Instances':
    stop_instances_list = []
    for instance in instancesList:
        check = st.checkbox(instance)
        if check:
            stop_instances_list.append(instance)
    
    stop_instances_list

    stop = st.button('Stop')

# Terminate Instances
elif service == 'Terminate Instances':
    terminate_instances_list = []
    for instance in instancesList:
        check = st.checkbox(instance)
        if check:
            terminate_instances_list.append(instance)
    
    terminate_instances_list

    terminate = st.button('Terminate')


# Upload file to S3 Bucket
elif service == 'S3 Upload':
    bucket_list = list_s3_buckets()
    check = st.radio("Choose a Bucket", bucket_list)
    file = st.file_uploader("Upload a file")
    object = st.text_input("Enter the object name")
    pressed = st.button("Upload")
    if pressed:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file.read())
        file_path = temp_file.name
        temp_file.close()

        feedback = upload_to_s3(file_path, check, object)
        st.write(feedback)

elif service == 'S3 Delete':
    bucket_list = list_s3_buckets()
    check = st.radio("Choose a Bucket", bucket_list)
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=check)

    # Check if objects are present in the bucket
    if 'Contents' in response:
        # Extract file names from the response
        file_list = [obj['Key'] for obj in response['Contents']]
        
        # Print the list of file names
        selected_file = st.radio("Choose a file:", file_list)
        pressed = st.button("Delete")
        if pressed:
            try:
                response = s3.delete_object(Bucket=check, Key=selected_file)
                st.write(f'File {selected_file} deleted successfully.')
            except Exception as e:
                print(f'Error deleting file: {e}')

    else:
        st.write('No objects found in the bucket.')


