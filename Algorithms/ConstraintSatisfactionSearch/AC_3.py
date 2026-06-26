from Core.Utils import *
def ac3_consistency_check(state):
    """Kiểm tra xem trạng thái có rõ ràng là deadlock không"""
    if is_goal(state):
        return True
    
    empties = count_empty_tubes(state)
    
    # Nếu không còn empty tube mà vẫn còn ống chưa thuần
    if empties == 0 and not is_almost_solved(state):
        return False
    
    # Kiểm tra từng màu
    for color in get_all_colors(state):
        blocks = count_color_blocks(state, color)
        
        # Heuristic: Nếu số khối > số empty + 1 → rất nguy hiểm (thường deadlock)
        # Nhưng nới lỏng một chút cho giai đoạn đầu
        if blocks > empties + 2:           # ← Tăng ngưỡng lên +2
            return False
    
    # Kiểm tra ống bị kẹt hoàn toàn (không đổ đi đâu được)
    for i, src_tube in enumerate(state):
        if not src_tube:
            continue
        top_color = src_tube[-1]
        can_pour = False
        
        for j, dst_tube in enumerate(state):
            if i == j:
                continue
            # Có thể đổ vào ống trống hoặc ống cùng top color và còn chỗ
            if len(dst_tube) < 4 and (len(dst_tube) == 0 or dst_tube[-1] == top_color):
                can_pour = True
                break
                
        if not can_pour:
            return False  # ống này bị kẹt cứng
    
    return True

def count_color_blocks(state, color):
    """
    Đếm số khối liên tiếp (maximal consecutive block) của một màu trên toàn board.
    Đây là phiên bản đúng hơn.
    """
    blocks = 0
    for tube in state:
        if not tube:
            continue
        i = 0
        while i < len(tube):
            if tube[i] == color:
                # Bắt đầu một block mới
                blocks += 1
                # Nhảy qua toàn bộ block
                while i < len(tube) and tube[i] == color:
                    i += 1
            else:
                i += 1
    return blocks

def count_empty_tubes(state):
    return sum(1 for tube in state if len(tube) == 0)

def get_all_colors(state):
    colors = set()
    for tube in state:
        colors.update(tube)
    return colors

def is_almost_solved(state):
    for tube in state:
        if tube and len(set(tube)) > 1:
            return False
    return True