import os
import time
from selenium import webdriver


def EngToJap(book_name, page_num, device, eng_texts_list):
    """
    ■DeepLをブラウザで呼び出して自動で入力してダウンロードしていく処理。

    本当はDeepLで翻訳後の日本語文章のテキストを文字列として持って色々したかったが、
    それが出来ない仕様になってるっぽいので、仕方なく自動クリックで逐一ダウンロードボタンを押している。
    なのでダウンロードはページごとの.txtファイルに限定されており、ダウンロード先もデバイスや人によって違う。
    今回はとりあえずwindowsとmacのデフォルトのダウンロードフォルダに指定して処理を進めている。
    """
    # 端末ごとに使うコマンド３種類を変数に入れておく。
    if device == "M":
        make_directory_command  = 'cd ~/Downloads ; mkdir '+ book_name
        change_fname_command    = 'cd ~/Downloads ; mv DeepL_*.txt ' # 変換後のファイル名は後回し
        move_file_to_directory  = 'cd ~/Downloads ; mv '+ book_name +'_*.txt '+ book_name 
    elif device == "W":
        make_directory_command  = 'cd ~/Downloads ; md '+ book_name
        change_fname_command    = 'cd ~/Downloads ; move DeepL_*.txt ' #変換後のファイル名は後回し
        move_file_to_directory  = 'cd ~/Downloads ; move '+ book_name +'_*.txt '+ book_name 

    # 翻訳版txtファイルの出力先ディレクトリを作る。
    os.system(make_directory_command)

    # webdriverを呼び出してDeepLに接続。
    URL = "https://www.deepl.com/translator"
    driver = webdriver.Chrome("/Users/honma/Desktop/DeepLSel/chromedriver")
    driver.get(URL)
    time.sleep(3)

    # cookie利用の忠告を閉じる。これが残ってると謎の不具合が出る。
    driver.find_element_by_class_name('dl_cookie_footer__close_btn').click()
    time.sleep(3)
    
    # PDF内の1ページごとに処理をしていく。
    for page_id in range(page_num):
        
        #テキストボックスごとの文章を取り出して文末に改行をいれる。
        texts_ready_for_deepL = ""
        for text_box in eng_texts_list[page_id]:
            texts_ready_for_deepL += text_box + "\n"

        
        # 入力欄に1ページごとのテキストを入力。ちなみに上限は5000字。
        driver.find_element_by_class_name('lmt__source_textarea').send_keys(texts_ready_for_deepL)
        time.sleep(9)

        # ダウンロードボタンをクリック。
        driver.find_element_by_class_name('lmt__target_toolbar__save').click()
        time.sleep(3)

        # 入力欄をまっさらにして次のページの処理に備える。
        driver.find_element_by_class_name('lmt__source_textarea').clear()
        time.sleep(3)
        
        # 端末ごとのデフォルトのダウンロード先にアクセスしファイル名を良い感じに改変
        os.system(change_fname_command + book_name + "_" + str(page_id) +'.txt')
        os.system(move_file_to_directory)



if __name__ == "__main__":
    JapToEng()