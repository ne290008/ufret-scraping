from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

from pychord import ChordProgression

from argparse import ArgumentParser
from glob import glob
from os import makedirs, path
from subprocess import check_output
from tqdm import tqdm
from time import sleep


def get_html(data_id):
    """htmlのデータを取得し、BeautifulSoupオブジェクトを返す"""

    try:
        html = urlopen(f'https://www.ufret.jp/song.php?data={data_id}')
    except HTTPError as e:
        # ufretの場合はデータ番号が存在しなくてもページは表示される、ただし中身は空になっている
        # よって、基本的に例外は起きないはず
        print(e)
        return None

    return BeautifulSoup(html.read(), 'html.parser')


def get_chord_prog(bs, transpose=0):
    """コード進行取得、移調する（オプション）"""

    cp = ChordProgression([elem.text.replace('♭', 'b').replace('maj', 'M') for elem in bs.select('span ruby rt') if elem.text not in ('N.C', 'N.C.')])
    cp.transpose(transpose)

    return ' '.join([str(c) for c in cp])


def get_title(bs, artist=False):
    """タイトル取得、アーティスト名を取得する（オプション）"""

    title, artist_name = bs.find('h1').text.split()
    if artist:
        return f'{title}/{artist_name}'
    else:
        return title


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--title', '-t', action='store_true', help='output title')
    parser.add_argument('--artist', '-a', action='store_true', help='output artist name with title')

    args = parser.parse_args()
    f_title = args.title
    f_artist = args.artist

    ifiles = glob('params/*.txt')
    makedirs('./result', exist_ok=True)
    if f_title:
        makedirs('./result/title', exist_ok=True)

    line_count = 0
    for ifile in ifiles:
        line_count += int(check_output(['wc', '-l', ifile]).decode().split()[0])

    pbar = tqdm(total=line_count)
    for ifile in ifiles:
        chord_prog = []
        title = []

        with open(ifile, mode='r') as f:
            lines = [s.strip() for s in f.readlines()]

        for line in lines:
            ll = line.split()
            data = None
            trans = 0
            if len(ll) == 1:
                data = int(ll[0])
            elif len(ll) == 2:
                data = int(ll[0])
                trans = int(ll[1])

            if data:
                sleep(1)
                bs = get_html(data)
                chord_prog.append(get_chord_prog(bs, trans))
                title.append(get_title(bs, f_artist))
            else:
                chord_prog.append('')
                title.append('')
            pbar.update(1)

        with open('./result/'+path.basename(ifile), mode='w') as f:
            f.write('\n'.join(chord_prog))

        if f_title:
            with open('./result/title/'+path.splitext(path.basename(ifile))[0]+'-title'+path.splitext(path.basename(ifile))[1], mode='w') as f:
                f.write('\n'.join(title))
    pbar.close()
    print('Completed!')
