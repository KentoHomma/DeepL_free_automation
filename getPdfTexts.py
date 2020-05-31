import os
import sys

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


def pdfToText(book_name, page_num):
    """
    pdfをテキストに変換するメソッド。
    最終的に全体、ページごと、テキストボックスごとの文章の三次元リストが返される。
    ついでにmidium/txt/[book_name]フォルダにページごとにtxtとして出力される。
    """ 

    # よく使う変数を予めまとめておく
    BOOK_NAME = book_name
    input_file      = os.path.join("input", (BOOK_NAME + ".pdf"))
    mid_output_root = os.path.join("midium", "txt")
    encoding = "utf-8"

    # 一応作っておく中間ファイルの出力先のパスの指定
    if not os.path.exists(mid_output_root + "/" + BOOK_NAME):
        os.mkdir(mid_output_root + "/" + BOOK_NAME)
    mid_output_path = mid_output_root + "/" + BOOK_NAME
    
    # 一ページごとに綺麗に英文章をとっていく。
    for page_id in range(page_num):
        
        # メソッドを用いてpdf内の1ページ内のテキストボックスを全て取得
        text_boxes = _convert(input_file, page_id)

        # ついでに1ページごとの整形済英文章を中間出力しておくのでファイルを開いておく。
        with open(mid_output_path + "/" + BOOK_NAME + "_" + str(page_id+1) + ".txt", 'wb') as fw:
            
            # pdf内のテキストを何とか翻訳機にかけられるように変換
            # テキストボックスを一つずつ解析していく。
            texts_in_a_page = []
            for box in text_boxes:
                text = box.get_text().strip()
                text = text + " "

                # 一旦単語別箇所を特定＆単語ごとに分けてリストに格納する。
                # 半角スペースに当たるたびappend。
                words = []
                for index, char in enumerate(text):
                    if char == " ":
                        if len(words) == 0:
                            word = text[0:index+1]
                        else:
                            word = text[len("+".join(words)) : index]
                        words.append(word)
                
                # 単語の前後にある改行、タブ、文末の"-"を削除
                # 文字列の数が増減してしまう処理は、単語の位置を特定する処理と一緒にできないためわざわざ分けてる。
                words_modified = []
                for word in words:
                    word = word.replace("- ", "").replace("\n", " ").replace("\t", " ")
                    words_modified.append(word)


                # 単語ごとに別れたテキストボックス内の文を半角スペースで結合し英文章に変換し、
                # １ページごとの英文章を集めたリストに格納。
                text_in_a_textbox = " ".join(words_modified)
                texts_in_a_page.append(text_in_a_textbox)
                
                # 一応英文章の中間ファイルをテキスト出力。変なとこで切れてないか確認できる。
                fw.write(bytes('\n', encoding=encoding))
                fw.write(bytes(text_in_a_textbox, encoding=encoding))
                fw.write(bytes('\n', encoding=encoding))

            
            # ページごとのテキストをジェネレータで返す。
            yield texts_in_a_page
                


def _convert(input_file, page_id):
    """
    pdf内のページをバラして、そのそれぞれのページ内の
    テキストボックスのリストを返すメソッド。
    """

    # Layout Analysisのパラメーターを設定。
    laparams = LAParams()
    laparams.detect_vertical = True
    codec = "utf-8"
    resource_manager = PDFResourceManager()
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)

    with open(input_file, 'rb') as f:
        # PDFPage.get_pages()にファイルオブジェクトを指定して、page_idに該当するPDFPageを取得
            allpages = PDFPage.get_pages(f)
            allpages = list(allpages)
            page = allpages[page_id]
            interpreter.process_page(page)
            content = device.get_result()

            # ページ内のテキストボックスのリストを取得＆座標が左上にあるほど先にソート。
            boxes = _findAndGetBoxes(content)
            boxes.sort(key=lambda b: (-b.y1, b.x0))
    
    return boxes



def _findAndGetBoxes(layout_obj):
    """
    containerを見つけ、containerからテキストボックスを見つけて
    リストにして返すメソッド。
    """

    # LTTextBoxを継承するオブジェクトの場合は1要素のリストを返す。
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]
    # LTContainerを継承するオブジェクトは子要素を含むので、再帰的に探す。
    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(_findAndGetBoxes(child))
        return boxes
    return []  # その他の場合は空リストを返す。
    

if __name__ == "__main__":
    pdfToText()
