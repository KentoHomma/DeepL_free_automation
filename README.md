# DeepL_free_automation
SeleniumでDeepLの無料デモを使う自動翻訳CUIアプリ。

## 動作確認済環境
- python3.7.3
- MacOS Catalina 10.15.4　/ Windows10
- GoogleChrome ver 83.0.4103.61 64bit

## 各種部品インストール
■osX(※bash)
- python3 -m venv hoge(仮想環境名)
- source hoge/bin/activate
- pip install -r requirements.txt

■Windows(※Powershell)
- python -m venv hoge
- hoge/Scripts/activate
- pip install -r requirements.txt

## chromedriverのインストール
- https://chromedriver.chromium.org/downloads からOSとchromeのバージョンに合ったchromedriverをダウンロード。
- windowsの場合は【chromedriver.exe】をAuto_DeepL直下に配置
- Macの場合は　　【chromedriver】をAuto_DeepL直下に配置

## 使い方
- inputディレクトリに翻訳したいpdfファイルを置く
- 「python main.py {拡張子抜きのpdfファイル名} {MまたはW}」を実行
- 例：端末はMacで/input/doraemon.pdfを翻訳したい場合は「pyton main.py doraemon M」
- 各ページの邦訳版テキストファイルを、端末のデフォルトの保存先に出力してくれます

## 注意！！！！！！！！！
■Windowsの場合はAuto_DeepLをデスクトップに設置して実行してください。もし別の場所に配置したかったらgetJapTexts.py内のコマンド操作を自分で合わせてください。
 
■もしselenium.common.exceptions.ElementClickInterceptedException:〜のエラーが出たら...
- 端末のダウンロードフォルダに作られた中途半端なフォルダやファイルを消してもう一回実行。
- それでもダメならgetJapTexts.pyのSLEEP_TIMEをちょっと長くたり短くしたりして何度か実行。
