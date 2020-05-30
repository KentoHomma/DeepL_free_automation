# DeepL_free_automation
SeleniumでDeepLの無料デモを使う乞食自動翻訳CLIアプリ。

### 動作確認済環境
- python3.7.3
- MacOS Catalina 10.15.4　/ Windows10
- GoogleChrome ver 83.0.4103.61 64bit

### 各種部品インストール
- python3 -m venv hoge(仮想環境名)
- python3 source hoge/bin/activate
- pip install -r requirements.txt

### 使い方
- inputディレクトリに翻訳したいpdfファイルを置く
- 「python main.py {拡張子抜きのpdfファイル名} {MまたはW}」を実行
- 　例：端末はMacで/input/doraemon.pdfを翻訳→→→「pyton main.py doraemon M」
- 各ページの邦訳版テキストファイルを、端末のデフォルトの保存先に出力してくれます

### 注意
■もし以下のエラーが出たらgetJapTexts.pyのSLEEP_TIMEをテキトーにちょっといじってください。おそらく解消されます。
selenium.common.exceptions.ElementClickInterceptedException:〜

■もしwebdriverが動かなかったら以下のリンクからダウンロードして、execファイルをDeepLSel直下に配置してください。
https://chromedriver.chromium.org/downloads
