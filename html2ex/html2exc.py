#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  bottom | left | middle | right | top
#  May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
horz_alignment = {
    'bottom' : 'VERT_BOTTOM',
    'center' : 'HORZ_CENTER',
    'left' : 'HORZ_LEFT',
    'right' : 'HORZ_RIGHT',
}
# <td valign="top | middle | bottom | baseline">
# May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
vert_alignment = {
    'bottom' : 'VERT_BOTTOM',
    'center' : 'VERT_CENTER',
    'top' : 'VERT_TOP',
}

def main():
    import lxml.html
    import xlrd, xlwt
    from pprint import pprint
    import sys
    import os

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
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('main', cell_overwrite_ok=False)
    new_row = 0
    for table_el in doc.xpath('//table'):
        for row_i, row in enumerate(table_el.xpath('./tr|./th')):
            row_i += new_row
            val = row.get('valign', None)
            ali = row.get('align', None)
            for col_i, col in enumerate(row.xpath('./td')):
                colspan = int(col.get('colspan', 0))
                rowspan = int(col.get('rowspan', 0))
                if colspan > 1: colspan -= 1
                if rowspan > 1: rowspan -= 1

                style = xlwt.XFStyle()
                if val is None:
                    val = col.get('valign', None)
                if ali is None:
                    ali = col.get('align', None)

                alignment = xlwt.Alignment()
                cur_horz_ali = horz_alignment.get(ali)
                if cur_horz_ali is not None:
                    alignment.horz = getattr(xlwt.Alignment, cur_horz_ali)
#                    alignment.horz = xlwt.Alignment.HORZ_CENTER

                cur_vert_ali = vert_alignment.get(ali)
                if cur_vert_ali is not None:
                    alignment.vert = getattr(xlwt.Alignment, cur_vert_ali)
#                    alignment.vert = xlwt.Alignment.VERT_CENTER
                col_data = col.text_content()
                style = xlwt.XFStyle()
                style.alignment = alignment
                while True:
                    try:
                        worksheet.write_merge(row_i, row_i+rowspan, col_i, col_i+colspan, col_data, style)
                    except:
                        col_i += 1
                    else:
                        break
                workbook.save(xlsfilename)
        else:
            new_row = row_i + 1



if __name__ == '__main__':
    main()