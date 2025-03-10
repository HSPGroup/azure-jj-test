import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient
import os

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="mycontainer",
                  connection="jjazuretest_STORAGE") 
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob\n"
                f"Name: {myblob.name}\n"
                f"Blob Size: {myblob.length} bytes")
    
    # Extract file name from the full path
    file_name = os.path.basename(myblob.name)
    logging.info(f"File name: {file_name}")
    
    # Get blob tags
    try:
        # Get connection string from app settings
        connection_string = os.environ["jjazuretest_STORAGE"]
        
        # Create the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get container name from the blob path
        container_name = "mycontainer"
        
        # Get a reference to the blob
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(myblob.name)
        
        # Get the blob tags
        tags = blob_client.get_blob_tags()
        
        # Print tags to terminal
        if tags:
            logging.info("Blob tags:")
            for key, value in tags.items():
                logging.info(f"    {key}: {value}")
        else:
            logging.info("No tags found for this blob")
            
    except Exception as e:
        logging.error(f"Error retrieving blob tags: {str(e)}")