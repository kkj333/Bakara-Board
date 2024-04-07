
def make_bord(result_list:list[str], new_arrays:list[list[str]]) -> None:
    x = 0
    y = 0
    for index, item in enumerate(result_list):
        # 初期設定
        if index == 0: 
            new_arrays[x][y] = item
            
        if index >= 1:
            x += 1
            if new_arrays[0][y] == item or item == 'D':
                new_arrays[x][y] = item              
            else:
                x = 0
                y += 1
                new_arrays[x][y] = item
    return new_arrays
