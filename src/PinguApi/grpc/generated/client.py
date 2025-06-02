import grpc
import sync_folder_to_pb2, sync_folder_to_pb2_grpc

def run():
    # Establish connection to gRPC server
    channel = grpc.insecure_channel('localhost:50051')
    stub = sync_folder_to_pb2_grpc.StorageServiceStub(channel)

    # Prepare the files you want to sync
    files_to_sync = [
        sync_folder_to_pb2.File(
            filename="file1.txt",
            project_id="project1",
            fuzz_target_id="target1",
            data=b"file content here"
        ),
        sync_folder_to_pb2.File(
            filename="file2.txt",
            project_id="project1",
            fuzz_target_id="target2",
            data=b"more content here"
        )
    ]

    # Iterate over files and send them one by one
    for file_chunk in files_to_sync:
        response = stub.SyncFolderTo(iter([file_chunk]))
        for status in response:
            print(f"File {status.filename} upload success: {status.success}, message: {status.message}")

if __name__ == '__main__':
    run()
