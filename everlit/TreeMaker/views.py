from django.shortcuts import render
from django.http import HttpResponseRedirect
import EverLit_Local.Litread as Litread
import EverLit_Local.Everscribe as Everscribe
import os, datetime
from evernote.api.client import EvernoteClient

# Create your views here.

def tree_maker_main(request):
    return render(request, 'TreeMaker.html')


def info_file(request):
    if request.method == 'POST':
        wos = request.FILES.get('wos', None)
        temp_note = request.FILES.get('temp_note', None)
        temp_cate = request.FILES.get('temp_cate', None)
        temp_single_cate = request.FILES.get('temp_single_cate', None)

        login_method = request.POST['login_method']
        dev_token = request.POST['dev_token']

        if (wos is not None) and (temp_note is not None) and (temp_cate is not None) and (temp_single_cate is not None):
            wos = str(wos.read(), encoding='utf-8')
            temp_note = str(temp_note.read(), encoding='utf-8')
            temp_cate = str(temp_cate.read(), encoding='utf-8')
            temp_single_cate = str(temp_single_cate.read(), encoding='utf-8')

            info = {
                'token': dev_token,
                'wos': wos,
                'temp_note': temp_note,
                'temp_cate': temp_cate,
                'temp_single_cate': temp_single_cate
            }

            for key in info.keys():
                path = 'TreeMaker/static/info/{}_{}.txt'.format(key, datetime.date.today())
                with open(path, 'w') as file_object:
                    file_object.write(info[key])
        else:
            return render(request, 'error.html')
    return render(request, 'TreeMaker.html', context={'result': '文件已收悉，可创建笔记'})


def create_note_cate(request):
    info = {
        'token': None,
        'wos': None,
        'temp_note': None,
        'temp_cate': None,
        'temp_single_cate': None
    }
    for key in info.keys():
        path = 'TreeMaker/static/info/{}_{}.txt'.format(key, datetime.date.today())
        if key == 'wos':
            info[key] = Litread.tab_win_utf_read(path)
        elif key == 'token':
            with open(path, 'r') as file_object:
                info[key] = file_object.read()
        else:
            info[key] = Everscribe.template_read(path)

    sandbox = False
    china = True
    client = EvernoteClient(token=info['token'], sandbox=sandbox, china=china)
    new_notes = Everscribe.create_notes_online(client, info['wos'], info['temp_note'])
    created_catelog = Everscribe.create_catalog_online(new_notes, client, info['temp_cate'], info['temp_single_cate'])

    return render(request, 'TreeMaker.html', context={'result': '笔记创建完成，', 'hint': '重置工具'})


def back_your_home(request):
    return HttpResponseRedirect('/treemaker/info_file/')





