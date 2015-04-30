#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lxml.html
import xlwt
import sys
import os


#  bottom | left | middle | right | top
#  May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
horz_alignment = {
    'bottom': xlwt.Alignment.VERT_BOTTOM,
    'center': xlwt.Alignment.HORZ_CENTER,
    'left': xlwt.Alignment.HORZ_LEFT,
    'right': xlwt.Alignment.HORZ_RIGHT,
}
# <td valign="top | middle | bottom | baseline">
# May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
vert_alignment = {
    'bottom': xlwt.Alignment.VERT_BOTTOM,
    'center': xlwt.Alignment.VERT_CENTER,
    'top': xlwt.Alignment.VERT_TOP,
}

class Html2exc(object):

    def __init__(self):
        self.list = []
        self.workbook = xlwt.Workbook()
        self.start_row = 0
        self.start_col = 0

    def create_new_sheet(self, name_sheet):
        self.worksheet = self.workbook.add_sheet(name_sheet, cell_overwrite_ok=False)

    def append_html_table(self, html_string, start_row=0, start_col=0):
        for row_i, row in enumerate(html_string.xpath('//tr|//th')):
            row_i += start_row
            vali = row.get('valign', None)
            ali = row.get('align', None)
            for col_i, col in enumerate(row.xpath('./td')):
                col_i += start_col
                colspan = int(col.get('colspan', 0))
                rowspan = int(col.get('rowspan', 0))

                if rowspan:
                    rowspan -= 1
                if colspan:
                    colspan -= 1

                if not vali:
                    vali = col.get('valign', None)
                if not ali:
                    ali = col.get('align', None)

                alignment = xlwt.Alignment()
                alignment.horz = horz_alignment.get(ali, xlwt.Alignment.HORZ_GENERAL)
                alignment.vert = vert_alignment.get(vali, xlwt.Alignment.VERT_TOP)

                borders = xlwt.Borders()
                borders.left = xlwt.Borders.DASHED
                # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
                borders.right = xlwt.Borders.MEDIUM
                borders.top = xlwt.Borders.MEDIUM
                borders.bottom = xlwt.Borders.MEDIUM
                borders.left_colour = 0x40
                borders.right_colour = 0x40
                borders.top_colour = 0x40
                borders.bottom_colour = 0x40

                style = xlwt.XFStyle()
                style.alignment = alignment
                style.borders = borders

                col_data = col.text_content()
                while (row_i, col_i) in self.list:
                    col_i += 1
                self.worksheet.write_merge(row_i, row_i+rowspan, col_i, col_i+colspan, col_data, style)
                for i in range(0, rowspan+1, 1):
                    for j in range(0, colspan+1, 1):
                        self.list.append((row_i+i, col_i+j))
                #start_row = row_i

    def save_wb(self, name):
        self.workbook.save(name)

def main():

    htmlfilename = sys.argv[1]
    if len(sys.argv) > 2:
        xlsfilename = sys.argv[2]
    else:
        if htmlfilename.endswith(".htm"):
            xlsfilename = htmlfilename.replace(".htm", ".xls")
        elif htmlfilename.endswith(".html"):
            xlsfilename = htmlfilename.replace(".html", ".xls")
        else:
            xlsfilename = htmlfilename + ".xls"

    doc = lxml.html.parse('1.html')
    cur_html = Html2exc()
    cur_html.create_new_sheet(htmlfilename)
    cur_html.append_html_table(doc)
    cur_html.save_wb(xlsfilename)


if __name__ == '__main__':
    main()