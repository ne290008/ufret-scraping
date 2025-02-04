# ufret-scraping

[U-フレット](https://www.ufret.jp)からコード進行を取得する。

## Usage
### 関連パッケージのインストール
```
$ pip install -r requirements.txt
```

### 取得するデータについて
`params`フォルダ内のテキストファイルにデータ番号、トランスポーズ（capo）を記述し、main.pyを実行する。記述例は以下の通り。

```
00001 0
00002
00003 +4
00004 -2
```

記述方法については以下の注意事項も参照されたし。

### 注意事項
- トランスポーズは記述しなくても良い。記述しない場合は0とみなされる。
- 1行に1曲記述する。
- テキストファイルであればファイル名はなんでも良い（つまり拡張子が`.txt`のファイルならなんでも良い）。
- テキストファイルは複数あっても良い。複数ある場合は全てのファイルのデータに対してスクレイピングを実行する。

### 実行時のオプション
|オプション|動作|
|---|---|
|-t (--title)|曲名も一緒に取得する|
|-a (--artist)|曲名と共にアーティスト名も取得する|

※[-t]オプションが指定されていない場合、[-a]オプションを指定しても取得されない。詳細は以下の動作例を参照されたし。

### 動作例
|コマンド|`result/title/hoge-title.txt`の出力|
|---|---|
|`python main.py -t`|`曲名`|
|`python main.py -t -a`|`曲名/アーティスト名`|
|`python main.py -a`|出力なし（ファイル自体が作成されない）|


## 実行結果
取得したコード進行は`result`フォルダに出力される。ファイル名は`params`フォルダのファイル名がそのまま使用される。なお、N.C（N.C.）は取得しないため、` C | N.C. | C `のようなコード進行は取得後のテキストファイルでは`C C`となる。

## コードの表記について
スクレイピングにて取得する際に表記を以下のように統一している。

|U-フレットでの表記|取得後の表記|備考|
|---|---|---|
|\# |\# |半角英数シャープ（そのまま）|
|♭  |b  |小文字B|
|maj|M  |大文字M|
|N.C (N.C.)|（無し）|取得しない|
