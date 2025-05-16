import streamlit as st
import random
from collections import Counter
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import re
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 关闭TensorFlow日志

# st.title("TOTO 4D 彩票号码预测器 \U0001F3B2")


DEFAULT_FILE_PATH = r"C:\Users\zongm\Desktop\Personal\4D\4D.txt"


def fetch_latest_results_with_selenium():
    url = "https://www.4dmoon.com/"
    results_by_provider = {"Magnum": {}, "Sports Toto": {}, "Damacai": {}}
    latest_draw_date = "未知"
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--ignore-certificate-errors')  # 新增
        chrome_options.add_argument('--allow-running-insecure-content')  # 新增
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)

        dmc_section = driver.find_element(By.ID, "dmc")
        draw_date_text = dmc_section.find_element(By.ID, "DDD").text.strip()
        parts = draw_date_text.split("-")
        if len(parts) == 3:
            latest_draw_date = f"{parts[2]}{parts[1]}{parts[0]}"
        else:
            latest_draw_date = draw_date_text

       # Damacai
        try:
            dmc_section = driver.find_element(By.ID, "dmc")
            dp1 = dmc_section.find_element(By.ID, "DP1").text.strip()
            dp2 = dmc_section.find_element(By.ID, "DP2").text.strip()
            dp3 = dmc_section.find_element(By.ID, "DP3").text.strip()

            special = []
            for i in range(1, 11):
                try:
                    val = dmc_section.find_element(By.ID, f"DS{i}").text.strip()
                    if val and val != "----":
                        special.append(val)
                    if len(special) >= 10:
                        break
                except:
                    continue

            consolation = []
            for i in range(1, 11):
                try:
                    val = dmc_section.find_element(By.ID, f"DC{i}").text.strip()
                    if val and val != "----":
                        consolation.append(val)
                except:
                    continue

            results_by_provider["Damacai"] = {
                "1st Prize": dp1,
                "2nd Prize": dp2,
                "3rd Prize": dp3,
                "Special": special,
                "Consolation": consolation
            }
        except Exception as e:
            results_by_provider["Damacai"] = {"Error": f"{e}"}

       # Magnum
        try:
            m4d_section = driver.find_element(By.ID, "m4d")
            mp1 = m4d_section.find_element(By.ID, "MP1").text.strip()
            mp2 = m4d_section.find_element(By.ID, "MP2").text.strip()
            mp3 = m4d_section.find_element(By.ID, "MP3").text.strip()

            special = []
            for i in range(1, 14):
                try:
                    val = m4d_section.find_element(By.ID, f"MS{i}").text.strip()
                    if val and val != "----":
                        special.append(val)
                    if len(special) >= 10:
                        break
                except:
                    continue

            consolation = []
            for i in range(1, 11):
                try:
                    val = m4d_section.find_element(By.ID, f"MC{i}").text.strip()
                    if val and val != "----":
                        consolation.append(val)
                except:
                    continue

            results_by_provider["Magnum"] = {
                "1st Prize": mp1,
                "2nd Prize": mp2,
                "3rd Prize": mp3,
                "Special": special,
                "Consolation": consolation
            }
        except Exception as e:
            results_by_provider["Magnum"] = {"Error": f"{e}"}

        # Toto
        try:
            toto_section = driver.find_element(By.ID, "toto")
            tp1 = toto_section.find_element(By.ID, "TP1").text.strip()
            tp2 = toto_section.find_element(By.ID, "TP2").text.strip()
            tp3 = toto_section.find_element(By.ID, "TP3").text.strip()

            special = []
            for i in range(1, 14):
                try:
                    val = toto_section.find_element(By.ID, f"TS{i}").text.strip()
                    if val and val != "----":
                        special.append(val)
                    if len(special) >= 10:
                        break
                except:
                    continue

            consolation = []
            for i in range(1, 11):
                try:
                    val = toto_section.find_element(By.ID, f"TC{i}").text.strip()
                    if val and val != "----":
                        consolation.append(val)
                except:
                    continue

            results_by_provider["Sports Toto"] = {
                "1st Prize": tp1,
                "2nd Prize": tp2,
                "3rd Prize": tp3,
                "Special": special,
                "Consolation": consolation
            }
        except Exception as e:
            results_by_provider["Sports Toto"] = {"Error": f"{e}"}
            
        driver.quit()
    except Exception as e:
        results_by_provider["抓取失败"] = {"Error": str(e)}
    return results_by_provider, latest_draw_date

def get_hot_and_cold_numbers(results, top_n=20):
    counter = Counter(results)
    most_common = counter.most_common(top_n)
    least_common = counter.most_common()[:-top_n-1:-1]
    hot = [num for num, _ in most_common]
    cold = [num for num, _ in least_common]
    return hot, cold

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

def apply_position_characteristics():
    def get_digit(pos):
        if pos == 'thousand':
            return str(random.choice([6, 8]))
        elif pos == 'hundred':
            return str(random.choice([0, 2, 4]))
        elif pos == 'ten':
            return str(random.choice([5, 7, 9]))
        elif pos == 'unit':
            return str(random.choice([7, 9]))
    return get_digit('thousand') + get_digit('hundred') + get_digit('ten') + get_digit('unit')

def generate_predictions(results):
    hot, cold = get_hot_and_cold_numbers(results)
    return {
        "热号推荐（出现频率高）": random.choice(hot) if hot else "N/A",
        "冷号推荐（很少出现）": random.choice(cold) if cold else "N/A",
        "模式构造号（如顺子、重复）": generate_number_from_patterns(),
        "位置特征号(基于奇偶/大小的号码)": apply_position_characteristics()
    }

def format_web_date(raw_date_str):
    try:
        year = raw_date_str[:4]
        rest = raw_date_str[4:]
        m = re.match(r"([A-Za-z]+)\((\w+)\) (\d+)", rest)
        if m:
            month_str, weekday, day = m.groups()
            datetime_object = datetime.strptime(month_str, "%b")
            month_fmt = datetime_object.strftime("%b")
            formatted = f"{int(day):02d}-{month_fmt}-{year}, ({weekday})"
            return formatted
        else:
            return raw_date_str
    except:
        return raw_date_str

def parse_date_for_compare(date_str):
    try:
        year = int(date_str[:4])
        m = re.match(r"\d{4}([A-Za-z]+)\(\w+\) (\d+)", date_str)
        if m:
            month_str, day = m.groups()
            dt_obj = datetime.strptime(f"{year} {month_str} {day}", "%Y %b %d")
            return dt_obj
        else:
            return None
    except:
        return None

# 读取历史数据（自动从默认路径）
results = []
latest_txt_date = "未知"

if os.path.exists(DEFAULT_FILE_PATH):
    try:
        with open(DEFAULT_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.strip().split("\n")[1:]
        if lines:
            last_line = lines[-1].strip().split(",")
            if len(last_line) >= 2:
                latest_txt_date = last_line[1]
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 25:
                numbers = parts[2:25]
                for num in numbers:
                    num = num.strip()
                    if num.isdigit() and len(num) == 4:
                        results.append(num)
        st.success(f"成功从默认路径文件读取 {len(results)} 条号码记录。")
    except Exception as e:
        st.error(f"读取默认路径文件失败：{e}")
else:
    with st.spinner("未找到历史文件，尝试抓取历史开奖记录..."):
        results = fetch_toto_4d_results(pages=3)
    latest_txt_date = "未知"

# 网页数据
latest_results, latest_web_date = fetch_latest_results_with_selenium()

# 日期处理
latest_txt_date_disp = "无" if latest_txt_date == "未知" else format_web_date(latest_txt_date)
latest_web_date_disp = format_web_date(latest_web_date)

dt_latest_web = parse_date_for_compare(latest_web_date)
#dt_latest_txt = parse_date_for_compare(latest_txt_date) if latest_txt_date != "未知" else None
# 修改原有的latest_txt_date获取逻辑
dt_latest_txt = None
if os.path.exists(DEFAULT_FILE_PATH):
    try:
        with open(DEFAULT_FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.read().strip().split("\n")
            
        if len(lines) > 1:  # 确保有数据行
            last_line = lines[-1].strip()
            if last_line.count(",") >= 24:  # 验证列数
                draw_date_str = last_line.split(",")[1]
                try:
                    # 直接转换文件中的yyyymmdd格式
                    dt_latest_txt = datetime.strptime(draw_date_str, "%Y%m%d")
                    latest_txt_date = draw_date_str  # 保持原始格式
                except ValueError:
                    st.warning("历史文件日期格式异常")
            else:
                st.warning("历史文件最后一行格式不完整")
    except Exception as e:
        st.error(f"读取历史文件失败: {e}")

# 原有的日期显示保持不动
latest_txt_date_disp = "无" if latest_txt_date == "未知" else format_web_date(latest_txt_date)


if dt_latest_web and dt_latest_txt:
    if dt_latest_web > dt_latest_txt:
        st.success("✅ 有新开奖结果，请更新记录。")
    else:
        st.info("❌ 没有新开奖结果，文件已是最新。")
elif dt_latest_web and not dt_latest_txt:
    st.info("无法比较，历史日期不存在。")
else:
    st.info("日期信息不足，无法判断是否有更新")

# Inject custom CSS for card styling
st.markdown("""
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}

.custom-card { 
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.custom-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px 0 rgba(0,0,0,0.3);
}

.damacai-card {
    background-image: linear-gradient(to bottom right, #000080, #0000CD) !important;
    color: white !important;
}
.damacai-card h3, .damacai-card p, .damacai-card .prize-number, .damacai-card .number-box span {
    color: white !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}
.damacai-card hr {
    border-top: 1px solid rgba(255,255,255,0.5) !important;
    opacity: 0.7;
}
.damacai-card .number-box {
    border: 2px solid rgba(255,255,255,0.7);
    box-shadow: inset 0 0 5px rgba(255,255,255,0.3), 0 0 8px rgba(255,255,255,0.3);
}

.magnum-card {
    background-image: linear-gradient(to bottom right, #FFD700, #FFEC8B) !important;
    color: black !important;
}
.magnum-card h3, .magnum-card p, .magnum-card .prize-number, .magnum-card .number-box span {
    color: black !important;
    text-shadow: 1px 1px 1px rgba(255,255,255,0.3);
}
.magnum-card hr {
    border-top: 1px solid rgba(0,0,0,0.3) !important;
    opacity: 0.7;
}
.magnum-card .number-box {
    border: 2px solid rgba(0,0,0,0.5);
    box-shadow: inset 0 0 5px rgba(0,0,0,0.2), 0 0 8px rgba(0,0,0,0.2);
}

.toto-card {
    background-image: linear-gradient(to bottom right, #FF0000, #FF6347) !important;
    color: white !important;
}
.toto-card h3, .toto-card p, .toto-card .prize-number, .toto-card .number-box span {
    color: white !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}
.toto-card hr {
    border-top: 1px solid rgba(255,255,255,0.5) !important;
    opacity: 0.7;
}
.toto-card .number-box {
    border: 2px solid rgba(255,255,255,0.7);
    box-shadow: inset 0 0 5px rgba(255,255,255,0.3), 0 0 8px rgba(255,255,255,0.3);
}

.custom-card h3 {
    font-size: 1.7em; /* Even larger title */
    font-weight: 700; /* Bolder title */
    margin-bottom: 15px;
    border-bottom: 2px solid currentColor;
    padding-bottom: 10px;
    opacity: 0.95;
}

.custom-card p {
    font-size: 1em; /* Standardized paragraph font size */
    line-height: 1.7;
}

.custom-card p strong { 
    color: inherit !important;
    font-weight: 700; /* Bolder strong text */
}

.prize-category {
    margin-bottom: 15px;
}

.prize-category strong {
    display: block;
    font-size: 1.2em; /* Larger category title */
    margin-bottom: 8px;
}

.prize-number {
    font-size: 1.5em !important; /* Larger and bolder prize numbers */
    font-weight: bold !important;
    display: inline-block;
    margin-right: 10px; /* Space between numbers if multiple */
    padding: 5px 0px;
}

.number-box-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px; /* Spacing between number boxes */
    margin-top: 5px;
}

.number-box {
    padding: 8px 12px;
    border-radius: 8px;
    background-color: rgba(0,0,0,0.1); /* Slight dark background for the box */
    font-size: 1.4em; /* Larger font for numbers in boxes */
    font-weight: bold;
    min-width: 60px; /* Ensure boxes have some width */
    text-align: center;
    /* 3D effect */
    border-style: solid;
    border-width: 2px; 
    border-color: #aaa #444 #444 #aaa; /* Light top/left, dark bottom/right for 3D */
    box-shadow: 1px 1px 3px rgba(0,0,0,0.3) inset, 1px 1px 2px rgba(255,255,255,0.2);
    transition: transform 0.2s ease;
}

.number-box:hover {
    transform: scale(1.05); /* Slight zoom on hover */
}

.prediction-section {
    margin-top: 30px;
    padding: 20px;
    background-color: #222; /* Darker background for prediction section */
    border-radius: 15px;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.3);
}

.prediction-section h3 {
    color: #eee;
    font-size: 1.8em;
    text-align: center;
    margin-bottom: 20px;
    border-bottom: 2px solid #FFD700; /* Gold underline for prediction title */
    padding-bottom: 10px;
}

.prediction-item {
    background-color: #333; /* Card-like background for each prediction */
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
}

.prediction-item strong {
    color: #FFD700; /* Gold color for prediction type */
    font-size: 1.1em;
    margin-right: 15px;
    min-width: 200px; /* Ensure alignment */
}

.prediction-item span {
    color: #ddd; /* Lighter text for predicted number */
    font-size: 1.3em;
    font-weight: bold;
}

.prediction-icon {
    font-size: 1.5em;
    margin-right: 10px;
    color: #FFD700;
}

</style>
""", unsafe_allow_html=True)

# Define a helper function to display prizes for a provider
def display_provider_results(provider_name_display, provider_data_key, column_object, results_data, card_class_name):
    prizes = results_data.get(provider_data_key, {})
    
    card_html_parts = [
        f"""<div class='{card_class_name} custom-card'>
<h3>{provider_name_display}</h3>"""
    ]

    if isinstance(prizes, dict) and "Error" not in prizes:
        # Helper to format numbers into boxes
        def format_numbers_to_boxes(numbers_data):
            if not numbers_data:
                return "<span class='prize-number'>----</span>"
            
            if isinstance(numbers_data, str):
                # Split by comma, then strip whitespace from each part
                numbers_list = [n.strip() for n in numbers_data.split(",") if n.strip() and n.strip() != "----"]
            elif isinstance(numbers_data, list):
                numbers_list = [str(n).strip() for n in numbers_data if n and str(n).strip() and str(n).strip() != "----"]
            else:
                return "<span class='prize-number'>----</span>"
            
            if not numbers_list:
                 return "<span class='prize-number'>----</span>"

            inner_boxes_html_parts = []
            for num in numbers_list:
                inner_boxes_html_parts.append(f"  <div class='number-box'><span>{num}</span></div>")
            
            inner_boxes_joined = "\n".join(inner_boxes_html_parts)
            
            boxes_html = f"""<div class='number-box-container'>
{inner_boxes_joined}
</div>"""
            return boxes_html

        card_html_parts.append("<hr>")
        card_html_parts.append(f"""<div class='prize-category'><strong>头奖 (1st Prize)</strong>{format_numbers_to_boxes(prizes.get("1st Prize"))}</div>""")
        card_html_parts.append(f"""<div class='prize-category'><strong>二奖 (2nd Prize)</strong>{format_numbers_to_boxes(prizes.get("2nd Prize"))}</div>""")
        card_html_parts.append(f"""<div class='prize-category'><strong>三奖 (3rd Prize)</strong>{format_numbers_to_boxes(prizes.get("3rd Prize"))}</div>""")
        card_html_parts.append("<hr>")
        card_html_parts.append(f"""<div class='prize-category'><strong>特别奖 (Special)</strong>{format_numbers_to_boxes(prizes.get("Special"))}</div>""")
        card_html_parts.append("<hr>")
        card_html_parts.append(f"""<div class='prize-category'><strong>安慰奖 (Consolation)</strong>{format_numbers_to_boxes(prizes.get("Consolation"))}</div>""")

    elif isinstance(prizes, dict) and "Error" in prizes:
        error_text_color = "pink" if "damacai" in card_class_name or "toto" in card_class_name else "#FF6347"
        card_html_parts.append(f"""<p style='color: {error_text_color}; font-weight: bold;'>抓取 {provider_name_display} 数据时出错: {prizes.get("Error")}</p>""")
    else:
        warning_text_color = "lightyellow" if "damacai" in card_class_name or "toto" in card_class_name else "#FFA500"
        card_html_parts.append(f"""<p style='color: {warning_text_color}; font-weight: bold;'>没有 {provider_name_display} 的数据或数据格式不正确。</p>""")
    
    card_html_parts.append("</div>")
    final_card_html = "\n".join(card_html_parts)

    with column_object:
        st.markdown(final_card_html, unsafe_allow_html=True)
st.subheader(f"\U0001F9FE 最新开奖结果: `{latest_web_date_disp}`")

# Create columns
col1, col2, col3 = st.columns(3)

# Display results in columns
if "抓取失败" not in latest_results:
    display_provider_results("Damacai", "Damacai", col1, latest_results, "damacai-card")
    display_provider_results("Magnum", "Magnum", col2, latest_results, "magnum-card")
    display_provider_results("Toto", "Sports Toto", col3, latest_results, "toto-card")
elif latest_results.get("抓取失败"):
    st.error(f"抓取最新开奖结果失败: {latest_results.get("抓取失败", {}).get("Error", "未知错误")}")
else:
    st.error("无法显示最新开奖结果，数据抓取可能存在未知问题。")

if results:
    predictions = generate_predictions(results)
    # Beautified Prediction Section
    prediction_html = "<div class=\"prediction-section\"><h3>\U0001F9E0 幸运号码预测 \U0001F52E</h3>"
    icons = {
        "热号推荐（出现频率高）": "🔥",
        "冷号推荐（很少出现）": "❄️",
        "模式构造号（如顺子、重复）": "⚙️",
        "位置特征号(基于奇偶/大小的号码)": "📍"
    }
    for k, v in predictions.items():
        icon = icons.get(k, "🔮") # Default icon
        prediction_html += f"<div class=\"prediction-item\"><span class=\"prediction-icon\">{icon}</span><strong>{k}:</strong> <span>{v}</span></div>"
    prediction_html += "</div>"
    st.markdown(prediction_html, unsafe_allow_html=True)
else:
    st.warning("暂无历史开奖记录，无法生成预测。")

from dateutil.parser import parse

# 在DEFAULT_FILE_PATH定义之后添加以下函数
def get_next_draw_number(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) < 2:  # 只有标题行或无数据
                return "000001"
            last_line = lines[-1].strip()
            last_draw_no = last_line.split(",")[0]
            next_no = int(last_draw_no) + 1
            return f"{next_no:06d}"
    except FileNotFoundError:
        return "000001"
    except Exception as e:
        st.error(f"获取最新DrawNo失败: {e}")
        return "000001"

def convert_web_date(web_date_str):
    try:
        dt = parse(web_date_str.split(",")[0].strip())
        return dt.strftime("%Y%m%d")
    except Exception as e:
        st.error(f"日期转换失败: {web_date_str} - {e}")
        return None




st.write(f"历史最新日期: `{dt_latest_txt}`")
st.write(f"网页最新日期: `{dt_latest_web}`")
# 在现有的日期比较逻辑之后添加以下代码
if dt_latest_web and dt_latest_txt and dt_latest_web > dt_latest_txt:
    st.success("✅ 有新开奖结果，请更新记录。")
    
    # 转换日期格式
    formatted_web_date = convert_web_date(latest_web_date_disp)
    
    if formatted_web_date and latest_results.get("Sports Toto"):
        toto_data = latest_results["Sports Toto"]
        if "1st Prize" in toto_data and "Special" in toto_data and "Consolation" in toto_data:
            # 构建新数据行
            new_draw_no = get_next_draw_number(DEFAULT_FILE_PATH)
            first_prizes = toto_data["1st Prize"][:3]  # 取前三个作为1st,2nd,3rd
            specials = toto_data["Special"][:10]       # 取前10个Special
            consolations = toto_data["Consolation"][:10] # 取前10个Consolation
            
            # 确保数据完整性
            if len(first_prizes) == 3 and len(specials) == 10 and len(consolations) == 10:
                new_line = [
                    new_draw_no,
                    formatted_web_date,
                    *first_prizes,
                    *specials,
                    *consolations
                ]
                
                # 写入文件
                try:
                    with open(DEFAULT_FILE_PATH, "a", encoding="utf-8") as f:
                        f.write("\n" + ",".join(new_line))
                    st.success(f"成功添加新开奖记录：DrawNo {new_draw_no}")
                except Exception as e:
                    st.error(f"写入文件失败: {e}")
            else:
                st.warning("开奖数据不完整，无法添加记录")
        else:
            st.warning("未能获取完整的Sports Toto开奖数据")
else:
    # 原有代码
    if dt_latest_web and dt_latest_txt:
        st.info("❌ 没有新开奖结果，文件已是最新。")