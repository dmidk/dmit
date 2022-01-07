#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============
Prerequisites
=============
To use the S3 utility (part of the dmitio class) one needs to set the following environment variables:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
If one is using AWS S3, the following environment variables are also required:
  - AWS_DEFAULT_REGION
If one is using a local S3 server, the following environment variables are also required:
  - AWS_S3_HOST

For bash an example could be (values are random and will not work!):
  - export AWS_ACCESS_KEY_ID="AJIEPXNW32N3A23APW3C"
  - export AWS_SECRET_ACCESS_KEY="XOnfa5HA+gwGEcC3ajklQ3kxlr3qXRR3s3k2xMaA"
  - export AWS_DEFAULT_REGION="eu-central-1"
  - export AWS_S3_BUCKET="my-bucket-name"

"""
import sys
import os
import json
import sys
import os
import boto3
import traceback
from typing import Union
sys.path.insert(0, os.path.abspath('./dmitio/'))
#from .arguments import arguments

def read_json(infile:str):
    """Reads data from a json file

    Parameters
    ----------
    infile : str
        Full path to json input file

    Returns
    -------
    data : dict
        dict with data
    """
    with open(infile, 'r') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = []
    return data


def save_json(datadict:dict, outfile:str) -> None:
    """Saves dict to a json file

    Parameters
    ----------
    datadict : dict
        json object (dict)
    outfile : str
        Full path to json output file
    """
    with open(outfile,'w') as f:
        json.dump(datadict,f)
    return


class s3:
    """Example of how to use the s3 class

Examples
--------
>>> #First call the s3 class:
>>> S3 = dmitio.s3()
>>> # (Optional) Get the s3 client (Low Level API)
>>> # Only useful if you want to do something else with the s3 client
>>> s3client = S3.s3_client
>>> # (Optional) Get the s3 resource (High Level API)
>>> # Only useful if you want to do something else with the s3 resource
>>> s3resource = S3.s3_resource
>>> # List the files in the bucket
>>> content = S3.list('my-bucket', 'path/to/files')
>>> # Upload a file to the bucket
>>> S3.upload('my-bucket', 'path/to/bucket-file', 'path/to/local-file')
>>> # Upload a file object to the bucket
>>> with open('/some/file', 'rb') as data:
>>>     S3.upload_object('my-bucket', 'path/to/bucket-file', data)
>>> # Download a file from the bucket
>>> S3.download('my-bucket', 'path/to/bucket-file', 'path/to/local-file')
>>> # Download a file object from the bucket to memory
>>> with open('/some/file', 'wb') as data:
>>>     S3.download_object('my-bucket', 'path/to/bucket-file', data)
>>> # Get bucket resource identifier
>>> bucket = s3resource.Bucket(name="kah")
>>> # Get S3 object identifier
>>> obj = s3resource.Object(bucket_name='my-bucket', key="/path/to/bucket-file")
>>> response = obj.get()
>>> file_content = response['Body'].read()
>>> with open('/some/file', 'wb') as f:
>>>     f.write(file_content)
    """

    def __init__(self, cert:Union[str,bool]='/etc/ipa/ca.crt') -> None:

        # hostname for AWS service = 's3-%s.amazonaws.com' % os.environ['AWS_DEFAULT_REGION']
        try:
            host = os.environ['AWS_S3_HOST'] 
            #bucket = os.environ['AWS_BUCKET']
        except KeyError:
            raise KeyError('Please set AWS_S3_HOST environment variable')
     
        self.s3_client = boto3.client('s3', 
                            endpoint_url=host,
                            aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],
                            verify=cert)

        self.s3_resource = boto3.resource('s3', 
                            endpoint_url=host, 
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], 
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                            verify=cert)

        return

    
    def get_s3_client(self) -> boto3.client:
        """Get s3 client. Useful to use the client directly
        if you want to do something else with the s3 client

        Returns
        -------
        boto3.client
            s3 client
        """
        return self.s3_client


    def get_s3_resource(self) -> boto3.resource:
        """Get s3 resource. Useful to use the resource directly
        if you want to do something else with the s3 resource

        Returns
        -------
        boto3.resource
            s3 resource
        """
        return self.s3_resource


    def burrito(self, description, job:callable) -> bool:
        """Utility for s3 transfer status

        Parameters
        ----------
        description : str
            job descrition
        job : callable
            job to run

        Returns
        -------
        bool
            Returns True if the job was successful, False otherwise
        """

        print(description, 'start', flush=True)
        try:
            job()
            print(description, 'done', flush=True)
            return True
        except:
            print(description, 'failed', flush=True)
            traceback.print_exc()
            return False


    def list(self, bucket:str, prefix:str) -> list:
        """List files in s3 bucket

        Parameters
        ----------
        bucket : str
            Name of bucket
        prefix : str
            "path" in bucket

        Returns
        -------
        list
            list of files in bucket

        Examples
        --------
        >>> s3.list('bucketname','prefix')
        """

        object_response = self.s3_client.list_objects_v2(Bucket=bucket,
                                            Delimiter='/',
                                            EncodingType='url',
                                            Prefix=prefix
                                            )

        if object_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Contents' in object_response:
                return [obj['Key'] for obj in object_response['Contents']]
            else:
                return []
        else:
            print('Listing failed')
            return


    def upload(self, bucket:str, key:str, path:str) -> bool:
        """Upload a file to s3 bucket

        Parameters
        ----------
        bucket : str
            Name of bucket
        key : str
            Filename in bucket
        path : str
            Local filename

        Returns
        -------
        bool
            Whether the transfer was successful (True) or failed (False)
        
        Examples
        --------
        >>> s3.upload('bucketname','key','path')
        """
        return self.burrito('put {}'.format(path), lambda: self.s3_client.upload_file(path, bucket, key))


    def upload_object(self, bucket:str, key:str, data) -> bool:
        """Upload a file to s3 bucket

        Parameters
        ----------
        bucket : str
            Name of bucket
        key : str
            Filename in bucket
        data : file-like object
            A file-like object to upload. At a minimum, it must implement the read method, and must return bytes.

        Returns
        -------
        bool
            Whether the transfer was successful (True) or failed (False)
        
        Examples
        --------
        >>> with open('testfile', 'rb') as data:
        >>>     s3.upload_object('bucket', 'key', data)
        """
        return self.burrito('put {}'.format(key), lambda: self.s3_client.upload_fileobj(data, bucket, key))


    def download(self, bucket:str, key:str, path:str) -> bool:
        """Download a file from s3 bucket

        Parameters
        ----------
        bucket : str
            Name of bucket
        key : str
            Filename in bucket
        path : str
            Local filename

        Returns
        -------
        bool
            Whether the transfer was successful (True) or failed (False)
        
        Examples
        --------
        >>> s3.download('bucketname','key','path')
        """
        return self.burrito('get {}'.format(key), lambda: self.s3_client.download_file(bucket, key, path))


    def download_object(self, bucket:str, key:str, data) -> bool:
        """Download a file object from s3 bucket

        Parameters
        ----------
        bucket : str
            Name of bucket
        key : str
            Filename in bucket
        data : file-like object
            A file-like object to upload. At a minimum, it must implement the write method, and must return bytes.

        Returns
        -------
        bool
            Whether the transfer was successful (True) or failed (False)
        
        Examples
        --------
        >>> with open('testfile', 'wb') as data:
        >>>     s3.download_object('bucket', 'key', data)
        """
        return self.burrito('get {}'.format(key), lambda: self.s3_client.download_fileobj(bucket, key, data))