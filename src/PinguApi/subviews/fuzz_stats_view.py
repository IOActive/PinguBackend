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
import json
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import generics
from rest_framework.exceptions import NotAcceptable, ValidationError, NotFound, APIException

from PinguApi.serializers.fuzzer_stats_serializer import FuzzerStatsSerializer
from PinguApi.tasks import download_and_update_stats
from src.PinguApi.utilities.dates_parser import parse_date
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi
from src.PinguApi.handlers.fuzzer_stats import build_results, get_date


   
class Fuzz_Stats_List_Load_APIView(generics.mixins.ListModelMixin,
                               generics.mixins.CreateModelMixin,
                      generics.GenericAPIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication, JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = FuzzerStatsSerializer



    def get(self, request, *args, **kwargs):
        data = request.query_params
        if 'load_stats' in data:
            if 'since' in data:
                date = parse_date(data['since'])
                if date is not None:
                    try:
                        download_and_update_stats.apply(args=[date]).get()
                        response = Response({'success': True, 'detail': 'Stats updated successfully'})
                        response.status_code = 200
                        return response
                    except Exception as e:
                        raise APIException(detail=f"Failed to update stats {e}", code=500)
                else:
                    NotAcceptable(detail="Invalid date format", code=406)
        else:
            NotAcceptable(detail="This endpoint is only used to force the stats loading")
    
    
    def post(self, request, *args, **kwargs):
        
        fuzz_target_id = request.data['fuzz_target']
        
        if not fuzz_target_id:
            raise NotAcceptable(detail="Missing required fields", code=406)
        
        try:
            start_date = get_date(request.data['start_date'], 7)
            end_date = get_date(request.data['end_date'], 1)
            group_by = request.data['group_by']
            interval = request.data['interval']
        except Exception as e:
            raise NotAcceptable(detail='missing parameter', code=406)
            
        try:
            results = build_results(fuzz_target_id, group_by, start_date, end_date, interval)
            response = Response({'success': True, 'detail': results})
            response.status_code = 200
            return response
        except Exception as e:
            raise APIException(detail="Failed to fetch the fuzzer stats", code=500)