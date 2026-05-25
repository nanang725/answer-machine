from selenium import webdriver
import time
import random
from selenium.webdriver.common.by import By
import requests
import parsel
from selenium.webdriver.chrome.options import Options

print("🚀 科目一自动答题程序启动...")

# 配置浏览器
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get('https://www.jsyks.com/kmy-mnks')

time.sleep(3)
driver.implicitly_wait(10)

print("📋 正在获取题目...")

lis = driver.find_elements(By.CSS_SELECTOR, '.Content>li')
total = len(lis)
print(f"✅ 共检测到 {total} 道题，开始自动答题...\n")

for i, li in enumerate(lis, 1):
    try:
        time.sleep(random.uniform(0.3, 0.8))  # 随机延时，更自然
        
        rid = li.get_attribute('c')
        url = f'https://tiba.jsyks.com/Post/{rid}.htm'
        
        response = requests.get(url=url, timeout=5).text
        selector = parsel.Selector(response)
        answer = selector.css('#question u::text').get()
        
        if answer == '对':
            answer = '正确'
        elif answer == '错':
            answer = '错误'
        
        bs = li.find_elements(By.CSS_SELECTOR, 'B')
        clicked = False
        for b in bs:
            choose = b.text.strip()
            if len(choose) > 2:
                choose = choose[0]
            if answer == choose:
                b.click()
                clicked = True
                break
                
        if clicked:
            print(f"✅ 第 {i}/{total} 题  已选择答案")
        else:
            print(f"⚠️  第 {i}/{total} 题  未找到匹配选项")
            
    except Exception as e:
        print(f"❌ 第 {i} 题出错，跳过")

print("\n🎯 所有题目已完成，正在提交试卷...")
driver.find_element(By.CSS_SELECTOR, '.btnJJ').click()

# 提交后等待，让你看成绩
print("⏳ 正在提交试卷，请稍等...")
time.sleep(8)

# 自动截图保存成绩
try:
    driver.save_screenshot("科目一答题成绩.png")
    print("📸 成绩已自动截图保存为：科目一答题成绩.png")
except:
    pass

print("\n✅ 自动答题已全部完成！")
print("请在浏览器中查看你的成绩")
input("\n按任意键关闭浏览器...")

driver.quit()
print("浏览器已关闭，程序结束。")