from django.contrib import admin
from django.urls import path
from pyton_assapp import views


app_name = "practise"

urlpatterns = [
    path('',views.index,name="index"),
    path('CreateBucketAsk',views.askUser),
    path('CreateNewBucket',views.createBucket),
    path('OwnawsAccount',views.useraws),
    path('AskOperationBucket',views.operationBucket),
    path('StatusOperation',views.statusCreateOperation),
    path('DeletingOperation',views.deleteOperation),
    path('deleteStatus',views.statusDeleteOperation),
    path('DisplayContent',views.statusListingOperation),
    path('uploadingFiles',views.uploadingFilesOperation),
    path('statusUploadFiles',views.statusUploadOperation),
    path('DisplayContentBucket',views.BucketListingOperation),
    path('deletingFiles',views.deleteFile),
    path('copyingFiles',views.copyingFiles),
    path('moveFiles',views.movingFiles),
    path('AskOperation',views.checkValidAccount)
     

    
]