import sys
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

from getPdfTexts import pdfToText
from getJapTexts import EngToJap

"""
■使い方
①inputディレクトリに翻訳したいpdfファイルを置く。
②CLIで「python main.py 【拡張子抜きのpdfファイル名】 【MまたはW】」を実行。
　例：「pyton main.py doraemon M」→ 端末はMacで/input/doraemon.pdfを翻訳したい。
③ページごとの邦訳を端末￥で設定されている保存先に出力してくれます。

■注意
selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <div class="lmt__target_toolbar__save" dl-test="translator-target-toolbar-download">...</div> is not clickable at point (1112, 570). Other element would receive the click: <div>...</div>
もし↑のエラーが出たらgetJapTexts.pyのSLEEP_TIMEをテキトーにちょっといじってください。おそらく解消されます。
"""

def main():
    # 入力値を受け取って円すうにいれる
    BOOK_NAME = sys.argv[1]
    DEVICE    = sys.argv[2]

    # 入力値のバリデーション✖️２
    assert len(sys.argv) == 3," 入力形式が違います。以下に倣ってください："+ "\n" + \
    "python main.py [拡張子抜きのpdfファイル名] [MまたはW]" + "\n" + \
    "例: python3 main.py doraemon W" + "\n"
    assert (DEVICE == "W" or DEVICE == "M"), "デバイスの指定は「M」か「W」で入力してください。" + "\n"

    # よく使う変数を予めまとめておく。
    input_pdf = "./input/" + BOOK_NAME + ".pdf"
    page_num = _getPageNum(input_pdf)

    # 1. pdfをページごとにテキスト化し、
    # 全体、ページごと、テキストボックスごとの三次元リストに変換
    # また、確認用の中間ファイルとして、ページごとの英文章テキストファイルを出力。
    print("①：PDFからテキストを抽出しています...")
    eng_texts_gen = pdfToText(BOOK_NAME, page_num)
    eng_texts_list = list(eng_texts_gen)
    print("②：PDFからテキストを抽出しました！ 上手く出来てるかは、/midium/txt/"+ BOOK_NAME +"で確認出来ます。")

    # 2. そのテキストを使ってselenium + deepLで翻訳して出力
    # macなら~/Downloads、windowsなら~/Downloadsに保存される。
    print("③：テキストをページごとに翻訳＆出力しています...")
    EngToJap(BOOK_NAME, page_num, DEVICE, eng_texts_list)
    print("④：全ての処理が完了しました！ 端末のダウンロードフォルダを確認してください。")



def _getPageNum(input_path):
    # pdf内のページ数を取得
    with open(input_path, 'rb') as f:
        f_object = PdfFileReader(f)
        page_num = f_object.getNumPages()
            
        return page_num


if __name__ == "__main__":
    main()