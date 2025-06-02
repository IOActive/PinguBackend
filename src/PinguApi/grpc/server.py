import asyncio
import grpc
from starlette.types import ASGIApp, Scope, Receive, Send
from PinguApi.grpc.generated import sync_folder_to_pb2_grpc
from PinguApi.grpc.services import StorageService

class GRPCServer(ASGIApp):
    """ASGI wrapper for running gRPC server inside Django ASGI app."""
    
    def __init__(self, host="[::]:50051"):
        self.host = host
        self.server = None

    async def serve_grpc(self):
        """Start the gRPC server."""
        self.server = grpc.aio.server()
        sync_folder_to_pb2_grpc.add_StorageServiceServicer_to_server(StorageService(), self.server)
        self.server.add_insecure_port(self.host)

        await self.server.start()
        print(f"🔥 gRPC server started on {self.host}")
        await self.server.wait_for_termination()

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """Handle ASGI requests (needed for ASGI compatibility)."""
        if self.server is None:
            asyncio.create_task(self.serve_grpc())

        # Return 404 for direct HTTP calls to gRPC
        response = b"gRPC server running. Use a gRPC client."
        headers = [(b"content-type", b"text/plain")]
        await send({
            "type": "http.response.body",
            "body": response,
        })
