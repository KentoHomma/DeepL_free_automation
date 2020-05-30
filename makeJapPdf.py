from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
 
def makeJapPdf(book_name, page_num):
    # 1ページずつtxtファイルからPDFを作っていく。
    #for page_id in range(page_num):
    page_id = 4
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    
    fname = book_name + "_" + str(page_id) + '.pdf'
    with open("../../Downloads" + "/" + book_name + "/" + book_name + "_" + str(page_id) + ".txt") as f:
        
        rows  = f.readlines()

        paper = canvas.Canvas(fname)             # 白紙のキャンバスを用意
        paper.saveState()                       # 初期化
        paper.setFont('HeiseiMin-W3', 9)      # フォントを設定
            
        # 横wと縦hの用紙サイズを設定
        w = 250 * mm
        h = 400 * mm
        paper.setPageSize((w, h))

        for index, x in enumerate(rows):
            x = "".join(x)
            paper.drawString(10, h-((index+1) * 12), x)
  
        paper.save()

if __name__ == "__main__":
    makeJapPdf("intermediate_poker", 4)