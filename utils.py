def in_rect(x: int, y: int, width: int, height: int, point: tuple[int, int]):
    p_x, p_y = point
    return x <= p_x and p_x <= x + width and y <= p_y and p_y <= y + height 