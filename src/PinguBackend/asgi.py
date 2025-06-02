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

"""
ASGI config for PinguBackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import asyncio
import os
import threading
import django
from django.core.asgi import get_asgi_application
from PinguBackend.environment import SETTINGS_MODULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)
django.setup()  

from channels.routing import ProtocolTypeRouter, URLRouter
from PinguApi.grpc.server import GRPCServer

# Initialize gRPC server
grpc_server = GRPCServer(host="[::]:50051")

# Function to run gRPC server in a separate thread with its own event loop
def run_grpc_server():
    loop = asyncio.new_event_loop()  # New event loop for this thread
    asyncio.set_event_loop(loop)
    loop.run_until_complete(grpc_server.serve_grpc())  # Run async gRPC server

# Start gRPC in a separate thread
grpc_thread = threading.Thread(target=run_grpc_server, daemon=True)
grpc_thread.start()
  
# ASGI application with both HTTP and WebSocket support
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
})