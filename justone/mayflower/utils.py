from math import ceil


def get_pagination(items_total, current_page, items_on_page):
    total_pages = int(ceil(items_total / float(items_on_page)))
    pagination_width = 2
    first_page = current_page - pagination_width
    last_page = current_page + pagination_width

    if first_page < 1:
        last_page += -(first_page - 1)
        first_page = 1
        if last_page > total_pages:
            last_page = total_pages

    if last_page > total_pages:
        first_page -= (last_page - total_pages)
        last_page = total_pages
        if first_page < 1:
            first_page = 1

    return {
        'pages': range(first_page, last_page + 1),
        'prev_page': 1 if current_page < 3 else current_page - 1,
        'next_page': total_pages if current_page > total_pages - 2 else current_page + 1
    }