#coding:utf8
import lxml.html
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
 
 
#  bottom | left | middle | right | top
#  May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL,
#  HORZ_DISTRIBUTED
_HORZ_ALIGNMENT = {
    'bottom': xlwt.Alignment.VERT_BOTTOM,
    'center': xlwt.Alignment.HORZ_CENTER,
    'left': xlwt.Alignment.HORZ_LEFT,
    'right': xlwt.Alignment.HORZ_RIGHT,
}
 
# <td valign="top | middle | bottom | baseline">
# May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
_VERT_ALIGNMENT = {
    'bottom': xlwt.Alignment.VERT_BOTTOM,
    'center': xlwt.Alignment.VERT_CENTER,
    'middle': xlwt.Alignment.VERT_CENTER,
    'top': xlwt.Alignment.VERT_TOP,
}

# May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan,
# 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal,
# 22 = Light Gray, 23 = Dark Gray

_BG_COLOR = {
    '#000000': 0,   # black
    '#ffffff': 1,   # white
    '#ff0000': 2,   # red
    '#00ff00': 3,   # green
    '#0000ff': 4,   # blue
    '#ffff00': 5,   # yellow
    '#ff00ff': 6,   # magenta
    '#00ffff': 7,   # cyan
    '#800000': 16,  # maroon
    '#008000': 17,  # dark green
    '#0000a0': 18,  # dark blue
}
# May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED,
# MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED
_BORDER_STYLE = {
    '0': xlwt.Borders.NO_LINE,
    '1': xlwt.Borders.THIN,
    '2': xlwt.Borders.MEDIUM,
    '3': xlwt.Borders.THICK,
}

BORDER_COLOR = 0x40
 
 
class Html2Excel(object):
    def __init__(self):
        self.list = []
        self.start_row = 0
        self.start_col = 0
        self.worksheet = None
        self.workbook = xlwt.Workbook()

    def use_existing_wb(self, name_workbook):
            self.workbook = copy(open_workbook(name_workbook, formatting_info=True))
            self.worksheet = self.workbook.get_sheet(0)

    def create_new_sheet(self, name_sheet):
        self.worksheet = self.workbook.add_sheet(name_sheet, cell_overwrite_ok=False)

    def append_html_table(self, html_file, start_row=0, start_col=0):
        html_string = lxml.html.parse(html_file)

        for table_el in html_string.xpath('//table'):

            row_i = start_row
            col_i = start_col

            for row_i, row in enumerate(table_el.xpath('./tr'), start=start_row):
                for col_i, col in enumerate(row.xpath('./td|./th'), start=start_col):
                    colspan = int(col.get('colspan', 0))
                    rowspan = int(col.get('rowspan', 0))

                    if rowspan:
                        rowspan -= 1
                    if colspan:
                        colspan -= 1

                    alignment = xlwt.Alignment()
                    alignment.horz = _HORZ_ALIGNMENT.get(row.get('align', col.get('align')), xlwt.Alignment.HORZ_GENERAL)
                    alignment.vert = _VERT_ALIGNMENT.get(row.get('valign', col.get('valign')), xlwt.Alignment.VERT_TOP)

                    borders = xlwt.Borders()
                    borders.left = _BORDER_STYLE.get(table_el.get('border', xlwt.Borders.DASHED))
                    borders.right = _BORDER_STYLE.get(table_el.get('border', xlwt.Borders.MEDIUM))
                    borders.top = _BORDER_STYLE.get(table_el.get('border', xlwt.Borders.MEDIUM))
                    borders.bottom = _BORDER_STYLE.get(table_el.get('border', xlwt.Borders.MEDIUM))
                    borders.left_colour = BORDER_COLOR
                    borders.right_colour = BORDER_COLOR
                    borders.top_colour = BORDER_COLOR
                    borders.bottom_colour = BORDER_COLOR

                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = _BG_COLOR.get(str(row.get('bgcolor', col.get('bgcolor'))).lower(), 1)

                    style = xlwt.XFStyle()
                    style.alignment = alignment
                    style.borders = borders
                    style.pattern = pattern

                    col_data = col.text_content()

                    while (row_i, col_i) in self.list:
                        col_i += 1

                    self.worksheet.write_merge(row_i, row_i+rowspan, col_i, col_i+colspan, col_data, style)
                    self.list.extend((row_i+i, col_i+j) for i in range(0, rowspan+1, 1) for j in range(0, colspan+1, 1))
            start_row = row_i + 1
        return row_i, col_i
 
    def save_wb(self, name):
        self.workbook.save(name)
 
 
if __name__ == '__main__':
    # html_filename = sys.argv[1]
    html_filename = '1.html'
    # xls_filename = sys.argv[2] if len(sys.argv) > 2 else (html_filename + ".xls")
    xls_filename = '2.xls'
 
    # converter = Html2Excel()
    # converter.create_new_sheet('1')
    # last_row, last_col = converter.append_html_table('1.html', 0, 1)
    # converter.append_html_table('2.html', last_row + 2, 1)
    # converter.save_wb(xls_filename)

    converter = Html2Excel()
    converter.use_existing_wb(xls_filename)
    converter.append_html_table('1.html', 3, 1)
    converter.save_wb(xls_filename)