import streamlit as st
import random
from collections import Counter

# Title
st.title("TOTO 4D 彩票号码预测器 🎲")

st.markdown("""
本工具根据历史开奖数据的统计特征，提供以下类型的预测号码：
- **热号推荐**（出现频率高）
- **冷号推荐**（很少出现）
- **模式构造号**（如顺子、重复）
- **基于奇偶/大小的号码**
""")

# Dummy result generator (replace with actual scraping in production)
def simulate_results(n=200):
    return [f"{random.randint(0, 9999):04d}" for _ in range(n)]

# 热/冷号分析
def get_hot_and_cold_numbers(results, top_n=20):
    counter = Counter(results)
    most_common = counter.most_common(top_n)
    least_common = counter.most_common()[:-top_n-1:-1]
    hot = [num for num, _ in most_common]
    cold = [num for num, _ in least_common]
    return hot, cold

# 模式号码生成
def generate_number_from_patterns():
    pattern = random.choice(["sequential", "repeating", "random"])
    if pattern == "sequential":
        start = random.randint(0, 6)
        return f"{start}{start+1}{start+2}{start+3}"
    elif pattern == "repeating":
        digit = str(random.randint(0, 9))
        return digit * 2 + str(random.randint(0, 9)) * 2
    else:
        return ''.join(str(random.randint(0, 9)) for _ in range(4))

# 位置特征号码生成
def apply_position_characteristics():
    def get_digit(pos):
        if pos == 'thousand':
            return str(random.choice([6, 8]))  # large even
        elif pos == 'hundred':
            return str(random.choice([0, 2, 4]))  # small even
        elif pos == 'ten':
            return str(random.choice([5, 7, 9]))  # large odd
        elif pos == 'unit':
            return str(random.choice([7, 9]))  # large odd
    return get_digit('thousand') + get_digit('hundred') + get_digit('ten') + get_digit('unit')

# 执行预测
def generate_predictions(results):
    hot, cold = get_hot_and_cold_numbers(results)
    return {
        "热号推荐": random.choice(hot),
        "冷号推荐": random.choice(cold),
        "模式构造号": generate_number_from_patterns(),
        "位置特征号": apply_position_characteristics()
    }

# 主程序
results = simulate_results()
predictions = generate_predictions(results)

st.subheader("🎯 预测结果")
for key, value in predictions.items():
    st.write(f"**{key}**: `{value}`")

st.caption("免责声明：本工具仅供娱乐用途，不能保证中奖概率。")
