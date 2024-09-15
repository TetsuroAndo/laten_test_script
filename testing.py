import subprocess
from collections import Counter
import random
import time

def is_valid(grid, row, col, num):
    for x in range(col):
        if grid[row][x] == num:
            return False
    for x in range(row):
        if grid[x][col] == num:
            return False
    return True

def generate_latin_square(N):
    grid = [[0 for _ in range(N)] for _ in range(N)]
    
    def backtrack(row, col):
        if row == N:
            return grid
        if col == N:
            return backtrack(row + 1, 0)
        numbers = list(range(1, N + 1))
        random.shuffle(numbers)  # ランダムな順序で数字を試す
        for num in numbers:
            if is_valid(grid, row, col, num):
                grid[row][col] = num
                if backtrack(row, col + 1):
                    return grid
                grid[row][col] = 0
        return None

    return backtrack(0, 0)

def format_for_rush01(grid):
    N = len(grid)
    clues = []
    
    for col in range(N):
        clues.append(len([x for x in range(N) if all(grid[i][col] < grid[x][col] for i in range(x))]))
    
    for col in range(N):
        clues.append(len([x for x in range(N-1, -1, -1) if all(grid[i][col] < grid[x][col] for i in range(N-1, x, -1))]))
    
    for row in range(N):
        clues.append(len([x for x in range(N) if all(grid[row][i] < grid[row][x] for i in range(x))]))
    
    for row in range(N):
        clues.append(len([x for x in range(N-1, -1, -1) if all(grid[row][i] < grid[row][x] for i in range(N-1, x, -1))]))
    
    return ' '.join(map(str, clues))

def output_to_clues(output_grid):
    return format_for_rush01(output_grid)

def run_test(test_number):
    N = 4
    latin_square = generate_latin_square(N)
    
    if latin_square:
        input_clues = format_for_rush01(latin_square)
        print(f"\nテスト {test_number}:")
        print("生成されたラテン方格:")
        for row in latin_square:
            print(' '.join(map(str, row)))
        
        print(f"\nrush-01への入力: {input_clues}")
        
        start_time = time.time()
        result = subprocess.run(['./rush-01', input_clues], capture_output=True, text=True)
        end_time = time.time()
        execution_time = end_time - start_time
        
        print("\nrush-01の出力:")
        print(result.stdout)
        print(f"実行時間: {execution_time:.6f}秒")
        
        if 'Error' in result.stdout:
            print("rush-01がエラーを返しました。")
            return "エラー", execution_time
        else:
            # rush-01の出力を解析して2次元配列に変換
            output_grid = [list(map(int, line.split())) for line in result.stdout.strip().split('\n')]
            
            # 出力をクルーに変換
            output_clues = output_to_clues(output_grid)
            
            # 入力クルーと出力クルーを比較
            if input_clues == output_clues:
                return "成功", execution_time
            else:
                print("rush-01の出力クルーが入力クルーと一致しません。")
                print(f"入力クルー: {input_clues}")
                print(f"出力クルー: {output_clues}")
                return "不一致", execution_time
    return "生成失敗", 0

def main():
    num_tests = 576
    results = Counter()
    total_time = 0
    successful_times = []

    print("テスト開始...")
    for i in range(num_tests):
        result, execution_time = run_test(i + 1)
        results[result] += 1
        if result == "成功":
            total_time += execution_time
            successful_times.append(execution_time)

    print("\n最終結果:")
    print(f"テスト回数: {num_tests}")
    print(f"成功: {results['成功']}")
    print(f"エラー: {results['エラー']}")
    print(f"生成失敗: {results['生成失敗']}")
    print(f"最終成功率: {results['成功'] / num_tests * 100:.2f}%")
    
    if successful_times:
        avg_time = sum(successful_times) / len(successful_times)
        print(f"平均実行時間: {avg_time:.6f}秒")
        print(f"最短実行時間: {min(successful_times):.6f}秒")
        print(f"最長実行時間: {max(successful_times):.6f}秒")

if __name__ == "__main__":
    main()