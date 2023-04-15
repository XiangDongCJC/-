import requests
import time
import re
from msedge.selenium_tools import EdgeOptions,Edge
from lxml import etree
import os
if __name__ == '__main__':

    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39'
    }
    print(
        '-------------------------------------------------------' + '下载的音乐默认保存在F:/网易下载音乐' + '-------------------------------------------------------')
    print(
        '-------------------------------------------------------' + '你可以在网易云音乐的网页版找到你想要的歌曲或者歌单,把它的URL复制过来' + '-------------------------------------------------------')
    print(
        '-------------------------------------------------------' + '将复制的URL输入在此处' + '-------------------------------------------------------')
    while(1):
        url = input('请输入URL:')
        if 'song' in url:  #单首歌

            name = input('歌曲的名称:')  #这里我想弄成自动获取url对应的歌曲名称---还有待研究
            if not os.path.exists(f'F:/网易下载音乐'):
                os.mkdir(f'F:/网易下载音乐')

            #将id提取出来，再将其拼接到新的外链接上
            song_id = url.split('/')[-1]
            id = song_id[8:]
            new_url = f'http://music.163.com/song/media/outer/url?id={id}.mp3'
            response = requests.get(url=new_url,headers=head).content

            #储存
            with open(f'F:/网易下载音乐/{name}.mp3','wb') as fp:
                fp.write(response)
            print(name,'下载完成！！！')

        else:  #歌单

            #将id提取出来，再将其拼接到可以查到歌单里的每个歌曲的id的外链接上
            play_id = url.split('/')[-1][12:]
            new_url = 'https://music.163.com/playlist?id=' + play_id
            new_response = requests.get(url=new_url,headers=head).text

            #提取出id和歌名，并建立字典用来存放数据
            id_name_dict = {}
            er = '<a href="/song\?id=(\d*?)">(.*?)</a>'
            id_list = re.findall(er,new_response)
            print('歌曲id'+ '\t' + '\t'+'\t' +'\t'+'\t'+'\t'+ '歌曲名称')
            for id in id_list:
                id = list(id)
                print(id[0] + '\t' + '\t'+'\t' +'\t'+'\t'+'\t'+ id[1])
                id_name_dict[id[0]] = id[1]
            print(id_name_dict)
            print(
                '-------------------------------------------------------' + '如果需要批量下载请用空格分开' + '-------------------------------------------------------')

            input_name = input('请输入你歌曲id:')
            input_list= input_name.split(' ')
            for new_id in input_list:
                if new_id == ' ':
                    continue
                else:
                    new_url1 = f'http://music.163.com/song/media/outer/url?id={new_id}.mp3'
                    response = requests.get(url=new_url1, headers=head).content

                    # 储存
                    with open(f'F:/网易下载音乐/{id_name_dict[new_id]}.mp3', 'wb') as fp:
                        fp.write(response)
                    print(id_name_dict[new_id], '下载完成！！！')
                    time.sleep(2)





