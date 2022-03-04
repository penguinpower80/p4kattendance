from io import TextIOWrapper

from django.shortcuts import render

from attendance.forms.importfiles import ImportFileForm
from attendance.utility import handle_uploaded_file


def importfiles(request):
    form = ImportFileForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            #https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
            handle_uploaded_file(request.POST.get('filetype'), TextIOWrapper(request.FILES['file'].file, encoding=request.encoding) )
            return render(request, 'attendance/import.html', {'form': form})
        else:
            return render(request, 'attendance/import.html', {'form':form})
    else:
        return render(request, 'attendance/import.html', {'form':form})
