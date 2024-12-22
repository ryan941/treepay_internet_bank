import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import threading
import time
from dotenv import load_dotenv
import os
import logging

FORMAT = '%(asctime)s %(filename)s %(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO)
load_dotenv()


# 创建 Selenium WebDriver
def create_driver():
	options = Options()
	# options.add_argument("--headless")  # 可选，无头模式
	options.add_argument("--disable-gpu")
	service = Service(executable_path=os.getenv('CHROME_DRIVER_PATH'))  # 确保 chromedriver 路径正确
	return webdriver.Chrome(service=service, options=options)


# Selenium 操作任务
def selenium_task(url, thread_id, update_status_callback):
	driver = create_driver()
	try:
		driver.get(url)
		time.sleep(10)  # 模拟浏览器操作
		print(f"线程 {thread_id} - 完成访问: {url}")
	finally:
		driver.quit()
		update_status_callback(-1)


# 多线程控制函数
def start_threads(urls, update_status_callback):
	threads = []
	for i, url in enumerate(urls):
		update_status_callback(1)  # 增加运行中的线程数
		thread = threading.Thread(target=selenium_task, args=(url, i + 1, update_status_callback))
		threads.append(thread)
		thread.start()


# GUI 应用
class App:
	def __init__(self, root):
		self.root = root
		self.root.title("ThreePay網銀端")
		self.root.geometry("400x300")

		# 当前正在运行的线程数
		self.running_threads = 0

		# 标题
		self.label = tk.Label(root, text="多线程 Selenium 控制", font=("Arial", 16))
		self.label.pack()

		# 开始按钮
		self.start_button = tk.Button(root, text="开始", command=self.start_execution, font=("Arial", 14))
		self.start_button.pack()

		# 添加示例 URL 列表
		self.urls = [
			"https://www.google.com",
			"https://www.wikipedia.org",
			"https://netbanking.aubank.in/drb/",
		]

	# 更新线程状态
	def update_status(self, delta):
		self.running_threads += delta
		# self.status_label.config(text=f"当前运行线程: {self.running_threads}")
		if self.running_threads == 0:
			self.log_message("所有线程已完成！")

	# 记录日志
	def log_message(self, message):
		print(message)

	# self.text_area.insert(tk.END, message + "\n")
	# self.text_area.see(tk.END)

	# 启动任务
	def start_execution(self):
		self.log_message("开始执行多线程任务...")
		threading.Thread(target=start_threads, args=(self.urls, self.update_status)).start()


# 主程序入口
if __name__ == "__main__":
	root = tk.Tk()
	app = App(root)
	root.mainloop()
