import os
import grpc
from PinguApi.grpc.generated import sync_folder_to_pb2, sync_folder_to_pb2_grpc
from PinguApi.submodels.fuzz_target import FuzzTarget
from PinguApi.submodels.project import Project

class StorageService(sync_folder_to_pb2_grpc.StorageServiceServicer):
    def SyncFolderTo(self, request_iterator, context):
        pass
        """
        Receives a stream of complete files from the client.
        """
        """ for request in request_iterator:
            filename = request.filename
            project_id = request.project_id
            fuzz_target_id = request.fuzz_target_id
            file_data = request.data
            is_last_file = request.is_last_file
            
            try:
                project = Project.objects.get(id=project_id)
            except Exception:
                yield sync_folder_to_pb2.SyncStatus(success=False, message="Project not found")
                continue
            
            try:
                fuzz_target = FuzzTarget.objects.get(id=fuzz_target_id, project_id=project.id)
            except Exception:
                yield sync_folder_to_pb2.SyncStatus(success=False, message="Fuzz target not found")
                continue
            
            storage_file_path = f"{fuzz_target.fuzzer}/{project_id}_{fuzz_target.binary}/{filename}"

            try: 
                result = stream_upload.apply(args=[storage_file_path, is_last_file]).get()                    

                yield sync_folder_to_pb2.SyncStatus(
                    filename=filename,
                    success=True,
                    message="File uploaded successfully"
                )
            except Exception as e:
                yield sync_folder_to_pb2.SyncStatus(
                    filename=filename,
                    success=False,
                    message=f"Failed: {str(e)}"
                )
 """

