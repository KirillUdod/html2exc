from openpyxl.styles import Alignment, Font, Border, Side, PatternFill
from openpyxl.workbook import Workbook
from lxml.html import document_fromstring, HTMLParser

# Value must be one of set(['hair', 'medium', 'dashDot', 'dotted', 'mediumDashDot', 'dashed',
# 'mediumDashed', 'mediumDashDotDot', 'dashDotDot', 'slantDashDot', 'double', None, 'thick', 'thin'])
_BORDER_STYLE = {
    '0': None,
    '1': 'thin',
    '2': 'medium',
    '3': 'thick',
}

_TEXT_SIZE = {
    './h1': 32,
    './h2': 24,
    './h3': 18,
    './h4': 16,
    './h5': 14,
    './h6': 11,
}

BORDER_COLOR = '000000'
WHITE_COLOR = '#FFFFFF'


class Html2Excel(object):
    def __init__(self):
        self.list = []
        self.start_row = 0
        self.start_col = 0
        self.worksheet = None
        self.workbook = Workbook(encoding='utf8')
        self.worksheet = self.workbook .active

    def use_existing_wb(self, name_workbook):
        # TODO
        self.workbook = copy(open_workbook(name_workbook, formatting_info=True, encoding_override='utf8'))
        self.worksheet = self.workbook.get_sheet(0)

    def create_new_sheet(self, name_sheet):
        # TODO
        self.worksheet = self.workbook.add_sheet(name_sheet, cell_overwrite_ok=False)

    def set_col_width(self, cols_width):
        # TODO
        for col_i in cols_width.keys():
            self.worksheet.col(col_i).width = int(cols_width.get(col_i)) * 20

    def append_html_table(self, html_file, start_row=0, start_col=0):
        html_string = document_fromstring(open(html_file, 'rb').read(), HTMLParser(encoding='utf8'))

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
                    #
                    # pattern = xlwt.Pattern()
                    # pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    # pattern.pattern_fore_colour = _BG_COLOR.get(str(row.get('bgcolor', col.get('bgcolor'))).lower(), 1)
                    #
                    # style = xlwt.XFStyle()
                    #
                    # style.font = font
                    # style.alignment = alignment
                    # style.borders = borders
                    # style.pattern = pattern
                    # style.alignment.wrap = 1

                    col_data = col.text_content().encode("utf8")

                    while (row_i, col_i) in self.list:
                        col_i += 1

                    cell = self.worksheet.cell(row=row_i, column=col_i)
                    cell.value = col_data
                    cell.alignment = Alignment(
                        horizontal=row.get('align', col.get('align')) or 'left',
                        vertical=row.get('valign', col.get('valign')) or 'top',
                        shrink_to_fit=True, wrap_text=True
                    )

                    cell.border = Border(
                        left=Side(border_style=_BORDER_STYLE.get(table_el.get('border') or None),
                                  color=BORDER_COLOR),
                        right=Side(border_style=_BORDER_STYLE.get(table_el.get('border') or None),
                                   color=BORDER_COLOR),
                        top=Side(border_style=_BORDER_STYLE.get(table_el.get('border') or None),
                                 color=BORDER_COLOR),
                        bottom=Side(border_style=_BORDER_STYLE.get(table_el.get('border') or None),
                                    color=BORDER_COLOR),
                    )

                    cell.fill = PatternFill(
                        fill_type='solid',
                        start_color=str(row.get('bgcolor', col.get('bgcolor', WHITE_COLOR)))[1:],
                        end_color=str(row.get('bgcolor', col.get('bgcolor', WHITE_COLOR)))[1:]
                    )

                    if col.xpath('./b'):
                        cell.font = Font(
                            bold=True
                        )

                    for col_font in col.xpath('./font'):
                        cell.font = Font(
                            color=str(col_font.get('color'))[1:]
                        )

                    for font_size in _TEXT_SIZE.keys():
                        if col.xpath(font_size):
                            cell.font = Font(
                                bold=True,
                                size=_TEXT_SIZE.get(font_size)
                            )

                    if rowspan or colspan:
                        self.worksheet.merge_cells(start_row=row_i, end_row=row_i+rowspan, start_column=col_i,
                                                   end_column=col_i+colspan)

                    self.list.extend((row_i+i, col_i+j) for i in range(0, rowspan+1, 1) for j in range(0, colspan+1, 1))

            start_row = row_i + 1

        return row_i, col_i

    def save_wb(self, name):
        self.workbook.save(name)


if __name__ == '__main__':
    # html_filename = sys.argv[1]
    html_filename = '1.html'
    # xls_filename = sys.argv[2] if len(sys.argv) > 2 else (html_filename + ".xls")
    xls_filename = '1.xls'

    # converter = Html2Excel()
    # converter.create_new_sheet('1')
    # last_row, last_col = converter.append_html_table('1.html', 0, 1)
    # converter.append_html_table('2.html', last_row + 2, 1)
    # converter.save_wb(xls_filename)

    cols_width = {1: 220, 3: 300}

    converter = Html2Excel()
    # converter.use_existing_wb(xls_filename)
    # converter.set_col_width(cols_width)
    # converter.create_new_sheet('1')
    converter.append_html_table('1.html', 3, 2)
    converter.save_wb(xls_filename)