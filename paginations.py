import math



def pagination(page_size, page, count):
    if page_size:
        page_size = int(page_size)
    else:
        page_size = 0
    if page:
        page = int(page)
    else:
        page = 0
    
    if page_size and page:
        offset = page_size * (page-1)
        query = f"LIMIT {page_size} OFFSET {offset}"
    else:
        if page_size != 0 and page == 0:
            query = f"LIMIT {page_size}"
        else:
            query = ""
    
    # next previous

    if page_size == 0:
        total_page = 1
    else:
        total_page = math.ceil(count/page_size)
    if page > 1 and page < total_page:
        next_page = page + 1
        previous_page = page - 1
    elif page == 1 and total_page == 1:
        next_page = 0
        previous_page = 0
    elif page == 1 and total_page > 1:
        next_page = page + 1
        previous_page = 0
    elif page == total_page and total_page > 1:
        next_page = 0
        previous_page = page - 1
    else:
        next_page = 0
        previous_page = 0

    data = {
        'query' : query,
        'page_size': page_size,
        'page': page,
        'next_page': next_page,
        'previous_page': previous_page
    }
    return data
