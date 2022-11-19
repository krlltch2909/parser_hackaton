def get_indexes(objects: list, current_page: int, page_size: int) -> tuple[int, int]:
    """
    Возвращает начальный и конечный индекс для итерации по списку
    с учетом размера выборки
    """
    start_index = (current_page - 1) * page_size
    end_index = start_index
    if (start_index + page_size - 1) > len(objects) - 1:
        end_index = len(objects) - 1
    elif (start_index + page_size - 1) <= len(objects) - 1:
        end_index += page_size -1

    return start_index, end_index
