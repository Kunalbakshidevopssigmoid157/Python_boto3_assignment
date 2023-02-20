
from operator import truediv
from django.shortcuts import render,HttpResponse
import io
import boto3
import pathlib
import json as j
import logging
import botocore.exceptions
import collections
from botocore.exceptions import ClientError

# Create your views here.
def  index(request):
   return render(request,'index.html')

def  askUser(request):
    return render(request,'CreateBucketAsk.html')

def askOperations(request):
    return render(request,'AskOperation.html')

def  createBucket(request):
   return render(request,'CreateNewBucket.html',{'result':"User"})
   


def  useraws(request):
    return render(request,'OwnawsAccount.html')

def operationBucket(request):
    return render(request,"AskOperationBucket.html")



def updateOperationBucket(request):
    
    return render(request,"updateNameBucket.html")

def deleteOperation(request):
    return render(request,"DeletingOperation.html")

def read_json():
    f = open("/home/sigmoid/Desktop/python/python_ass1/pyton_assapp/UserCredential.json","r")
    id1 = j.load(f)
    return id1

def userlogging(Access_key,Secret_key,AWS_region):
    try:
        resource1
        resource1 = boto3.client(
        's3',
        
        aws_access_key_id=Access_key,
        aws_secret_access_key=Secret_key,
        #aws_session_token=SESSION_TOKEN,
        region_name=AWS_region,
    
             )
        location = {'LocationConstraint': AWS_region}
        bucket = resource1.create_bucket(
        Bucket="default",
       CreateBucketConfiguration=location)
        return "ValidCredentials"
        
    except Exception as e:

        return type(e).__name__()
        
    
def checkValidAccount(request):
    if 'own_user_credentials' in request.POST:
        dictUser = {
            "Access_key":request.POST['User_Access_Key'],
            "Secret_key":request.POST['User_Secret_Access_Key']
        }
        with open("/home/sigmoid/Desktop/python/python_ass1/pyton_assapp/UserCredential.json", "w") as outfile:
            j.dump(dictUser, outfile)
        return render(request,'AskOperation.html')
        

def statusCreateOperation(request):
    if 'user_create__bucket' in request.POST:
        try:
            bucket_name=request.POST['UserBucketCreateName']
            AWS_region = request.POST['UserBucketCreateAWSRegion'] 
            dict1= read_json()
            resource1 = boto3.client(
        's3',
        
        aws_access_key_id=dict1['Access_key'],
        aws_secret_access_key=dict1['Secret_key'],
        #aws_session_token=SESSION_TOKEN,
        region_name=AWS_region,
    
             )
            location = {'LocationConstraint': AWS_region}
            bucket = resource1.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)
            response1 = resource1.list_buckets()
            res={
                'cateogry':"Bucket",
                'operationcateogry':"Create",
                'output':"Created"
            }
            return render(request,"StatusOperation.html",{'result':res})
        except Exception as e:
            res={
                'cateogry':"Bucket",
                'operationcateogry':"Create",
                'output':type(e).__name__
            }
    return render(request,"StatusOperation.html",{'result':res})
           
       

def statusDeleteOperation(request):
    
       
    if 'delete__bucket' in request.POST :
            bucket_name=request.POST['name_of_bucket']
            dict1= read_json()
            try :
                resource1 = boto3.client('s3',aws_access_key_id=dict1["Access_key"],aws_secret_access_key=dict1["Secret_key"],   #aws_session_token=SESSION_TOKEN
             )
                response = resource1.list_buckets()
                response1 = resource1.list_buckets()
                res1=[]
                for bucket in response1['Buckets']:
                    res1.append(bucket.Name)
                frequency = collections.Counter(bucket_name)
                Object=resource1.Bucket(bucket_name)
                res2=[]
                for obj in Object.objects.all():
                    res2.append(obj.key)
                if frequency>0 and len(res2)==0: 
                    resource1.delete_bucket(Bucket=bucket_name)
                    res={
                    'cateogry':"Bucket",
                    'cateogryoperation':"Delete",
                    'output':"Deleted"
                    }
                #return render(request,"deleteStatus.html",{'result':res})
                elif frequency>0 and len(res2)>0:
                    for s3_object in Object.objects.all():
                        s3_object.delete()
                    for s3_object_ver in Object.object_versions.all():
                        s3_object_ver.delete()
                    resource1.delete_bucket(Bucket=bucket_name)
                    res={
                    'cateogry':"Bucket",
                    'cateogryoperation':"Delete",
                    'output':"Deleted"
                    }
                #return render(request,"deleteStatus.html",{'result':res})
                else:
                    res={
                    'cateogry':"Bucket",
                    'cateogryoperation':"Delete",
                    'output':"No such bucket is present "
                    }
                
            except Exception as e:
                res={
                    'cateogry':"Bucket",
                    'cateogryoperation':"Delete",
                    'output':type(e).__name__
                    }
    return render(request,"deleteStatus.html",{'result':res})
    
def statusListingOperation(request):
     
    if 'display_content' in request.POST:
        res = {
        'bucket':[]
        }
        AWS_REGION = "ap-south-1"
        dict1= read_json()
        try: 
            resource1 = boto3.client(
                's3',
                aws_access_key_id=dict1["Access_key"],
                aws_secret_access_key=dict1["Secret_key"],
        
    #aws_session_token=SESSION_TOKEN
             )
            response = resource1.list_buckets()
            for bucket in response['Buckets']:
                res['bucket'].append(bucket)
        except Exception as e:
            res={
                    'bucket':type(e).__name__
                }
    return render(request,'DisplayContent.html',{'result':res})
                


def uploadingFilesOperation(request):
    return render(request,"uploadingFiles.html")


def statusUploadOperation(request):
    
    if 'user_upload__files' in request.POST:
        bucket_name= request.POST['UserBucketName']
        AWS_region = request.POST['UserAWSregion']
        upFile = request.POST['UploadFileName']
        BASE_DIR = pathlib.Path(__file__).parent.resolve()
        dict1= read_json()
        
        try: 
            resource1 = boto3.client(
        's3',
        
        aws_access_key_id=dict1["Access_key"],
        aws_secret_access_key=dict1["Secret_key"],
        #aws_session_token=SESSION_TOKEN,
        region_name=AWS_region,
    
             )
            message=""
            object_name= None
            if object_name is None:
                object_name = upFile
                resource1.upload_file(f"{BASE_DIR}/{upFile}", bucket_name, object_name, ExtraArgs=None) 
                message="Uploaded"
        except Exception as e:
            message=type(e).__name__
        res={
            'cateogry':"Upload the File",
            'output':message
            }
        return render(request,'statusUploadFiles.html',{'result':res})
    
    
def BucketListingOperation(request):
    res=[]
    if 'ContentBucket' in request.POST:
        bucket_name = request.POST['ParticularBucket']
        AWS_region = request.POST['ParticularBucketAWSregion']
        dict1= read_json()
        try:
            resource1 = boto3.resource(
        's3',
        aws_access_key_id=dict1["Access_key"],
        aws_secret_access_key=dict1["Secret_key"],
        #aws_session_token=SESSION_TOKEN,
        #region_name='AWS_region',
    
             )
            Object=resource1.Bucket(bucket_name)
            for obj in Object.objects.all():
                res.append(obj.key)
                
        except Exception as e:
            res = type(e).__name__
    return render(request,'DisplayContentBucket.html',{'result':res})

def deleteFile(request):
    if 'DeleteFile' in request.POST:
        bucket_name= request.POST['ParticularBucket']
        
        upFile = request.POST['ParticularFile']
   
        dict1= read_json()
        try:
            resource1 = boto3.resource(
        's3',
        
        aws_access_key_id=dict1["Access_key"],
        aws_secret_access_key=dict1["Secret_key"],
        #aws_session_token=SESSION_TOKEN,
        region_name='us-east-1',
    
             )
            Object=resource1.Bucket(bucket_name)
            res1=[]
            for obj in Object.objects.all():
                res1.append(obj.key)
            frequency = collections.Counter(upFile)
            if frequency>0:
                s3_object = resource1.Object(bucket_name, upFile)
                s3_object.delete()
                res={
            'cateogry':"Delete the File",
            'output':"Deleted"
            }
            else:
                res={
            'cateogry':"Delete the File",
            'output':"No suc ffile is present"
            }
        except Exception as e:
            res=  type(e).__name__
        return render(request,'deletingFile.html',{'result':res})


def copyingFiles(request):
    if 'CopyFiles' in request.POST:
        source_name= request.POST['SbucketName']
        destination_name = request.POST['DbucketName']
        upFile = request.POST['ParticularFile']
   
        dict1= read_json()
        try:
            resource1 = boto3.resource(
        's3',
        
        aws_access_key_id=dict1["Access_key"],
        aws_secret_access_key=dict1["Secret_key"],
        #aws_session_token=SESSION_TOKEN,
        region_name='us-east-1',
    
             )
            copy_source = {
            'Bucket': source_name,
            'Key': upFile
            }
            Object=resource1.Bucket(destination_name)
            Object.copy(copy_source, upFile) 
            res={
            'cateogry':"Copying the File",
            'output':"Copied"
            }
        except Exception as e:
            res={
            'cateogry':"Copying the File",
            'output':type(e).__name__
            }
    return render(request,'copyingFiles.html',{'result':res})
    
def movingFiles(request):
    if 'MoveFiles' in request.POST:
        source_name= request.POST['SbucketName']
        destination_name = request.POST['DbucketName']
        upFile = request.POST['ParticularFile']
   
        dict1= read_json()
        try:
             resource1 = boto3.resource(
        's3',
        
        aws_access_key_id=dict1["Access_key"],
        aws_secret_access_key=dict1["Secret_key"],
        #aws_session_token=SESSION_TOKEN,
        region_name='us-east-1',
    
             )
             copy_source = {
            'Bucket': source_name,
            'Key': upFile
            }
             Object=resource1.Bucket(destination_name)
             Object.copy(copy_source, upFile)
             Object = resource1.Object(source_name, upFile)
             Object.delete()
             res={
            'cateogry':"Move the File",
            'output':"Move"
            }
        except Exception as e: 
            res={
            'cateogry':"Move the File",
            'output': type(e).__name__
            }
    return render(request,'copyingFiles.html',{'result':res})