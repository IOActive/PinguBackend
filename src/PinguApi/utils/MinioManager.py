from minio import Minio
from django.conf import settings

class MinioManger():
    
    def __init__ (self):
        self.client = Minio(
            endpoint=settings.MINIO_HOST,
            access_key=settings.ACCESS_KEY,
            secret_key=settings.SECRET_KEY,
            secure=False
        )
        
    def crearteBucket(self, bucketName):
        self.client.make_bucket(bucketName)
        
    def uploadFile(self, bucketName, fileName, filePath):
        self.client.fput_object(bucketName, fileName, filePath)
        
    def downloadFile(self, bucketName, fileName, filePath):
        self.client.fget_object(bucketName, fileName, filePath)
        
    def deleteFile(self, bucketName, fileName):
        self.client.remove_object(bucketName, fileName)
        
    def deleteBucket(self, bucketName):
        self.client.remove_bucket(bucketName)
    
    def listBuckets(self):
        return self.client.list_buckets()
    
    def listObjects(self, bucketName, recursive=False):
        return self.client.list_objects(bucketName, recursive=recursive)
    
    def get_object(self, bucketName, fileName):
        return self.client.get_object(bucketName, fileName)
    
    def put_object(self, bucketName, name, data, size):
        return self.client.put_object(bucket_name=bucketName, object_name=name, data=data, length=size)
    
    def remove_object(self, bucketName, fileName):
        return self.client.remove_object(bucketName, fileName)
        
        