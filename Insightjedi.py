from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.exceptions import *    # i will create one app called api which will have all the common functionality 
from api import utils as api_utils

from . models import Document

class UserDocuments(APIView):
  """
  This API to get, upload and delete the Documents
  """
  def get(self,request):
    """
    This get method to fetch the documents
    """
    if request.user and not request.user.is_authenticated:
      raise GenericException(status_type=STATUS_TYPE["APP"],
                             exception_code=NONRETRYABLE_CODE["BAD_REQEUST"],
                             detail="You're not logged In")
    get_documents = Document.objects.filter(owner=request.user.id).all()
    if get_documents:
      serialized_documents = product_loan_serializers.GetFullfillmentDocuments(\
            get_documents,
            many=True).data
      return api_utils.response(serialized_documents)
    return api_utils.response({"message":"No Document Found",status=True, "status_code":200})
    
  def post(self, request):
    """
    Uploading fullfill documents for an loan applications
    :params 
    return
    """
    if request.user and not request.user.is_authenticated:
      raise GenericException(status_type=STATUS_TYPE["APP"],
                             exception_code=NONRETRYABLE_CODE["BAD_REQEUST"],
                             detail="You're not logged In")
    document_serializer = document_serializers.CustomDocumentSerializer(data = request.data)
    if not document_serializer.is_valid():
        raise GenericException(status_type=STATUS_TYPE["APP"], exception_code=NONRETRYABLE_CODE["BAD_REQUEST"],
                     detail=document_serializer.errors, request=request)
    # Saving uploaded document details
    upload_document = document_serializer.save()    

    return api_utils.response({\
            'status': True, 'message': 'Sucessfully Uploaded Document.', 'title': document_serializer.title,
            'document_url': S3_BUCKET_URL + document_serializer.document_key, 
            'document_id': document_serializer.id})

  def delete(self, request):
      """
      Deleting documents 
      parms - document_id
      return
      """
      if request.user and not request.user.is_authenticated:
      raise GenericException(status_type=STATUS_TYPE["APP"],
                             exception_code=NONRETRYABLE_CODE["BAD_REQEUST"],
                             detail="You're not logged In")
      document_id = request.data.get("document_id")
      if document_id:
        document = Document.objects.filter(id = document_id).first()
        if not document:
            raise GenericException(status_type=STATUS_TYPE["APP"], exception_code=NONRETRYABLE_CODE["BAD_REQUEST"],
                       detail="Document Not availabe to delete!", request=request)
        document.delete()
        return api_utils.response({'status': True,
                                   'message': 'Sucessfully Deleted Document!'})
      return api_utils.response({'status': False,
                                 'message':'document_id is missing'})





