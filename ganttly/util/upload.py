import os

def UploadFile(f, file_id):
    dest = 'C:/Users/Brendan/BitNami DjangoStack projects/COMP30005/ganttly/uploads/'

    with open(dest + str(file_id) + os.path.splitext(f.name)[1], 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

