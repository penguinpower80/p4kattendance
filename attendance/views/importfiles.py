from io import TextIOWrapper

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from attendance.forms.importfiles import ImportFileForm
from attendance.utility import handle_uploaded_file

@user_passes_test(lambda u: u.is_superuser)
def importfiles(request):
    form = ImportFileForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            #https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
            result = handle_uploaded_file(request.POST.get('filetype'), TextIOWrapper(request.FILES['file'].file, encoding=request.encoding) )
            result['form'] = form
            result['type'] = request.POST.get('filetype')
            return render(request, 'attendance/import.html', result)
        else:
            return render(request, 'attendance/import.html', {'form':form})
    else:
        return render(request, 'attendance/import.html', {'form':form})
