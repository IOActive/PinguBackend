# Copyright 2024 IOActive
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from minio import Minio
from django.conf import settings

class MinioManger():
    
    def __init__ (self):
        self.client = Minio(
            endpoint=settings.MINIO_HOST,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
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
        
        