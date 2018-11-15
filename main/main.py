# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


class Main:

    # ------初始化，打开浏览器和易班登陆页----------
    def initWebkit(self):
        self.browser = Firefox()
        # self.browser.implicitly_wait(10)  # 隐性等待
        self.browser.get('https://www.yiban.cn/login')

    # ------模拟登陆易班进入首页----------
    def loginModel(self):
        self.browser.find_element_by_id("account-txt").send_keys('17376579036')  # 伟杰15397035243  王颢霖15968869844   17376579036
        self.browser.find_element_by_id("password-txt").send_keys('qq13931975931')  # 720237lwj   wangyifei123   qq13931975931
        self.browser.find_element_by_id("login-btn").click()
        sleep(3)
        try:
            captcha_img = self.browser.find_element_by_css_selector(".captcha")
            str = input('是否继续')
            self.browser.find_element_by_id("login-btn").click()
        except:
            print('直接进入首页')

    # ------模拟操作之签到（一天只能进行一回操作，有效次数一回）----------
    def signInModel(self):
        try:
            WebDriverWait(self.browser, 20, 0.5).until_not(EC.presence_of_element_located((By.ID, 'tool-newbie')))
            self.browser.find_element_by_id("tool-sign").click()
            WebDriverWait(self.browser, 3, 0.5).until(EC.visibility_of_element_located((By.ID, 'sign-survey')))
            self.browser.find_element_by_xpath("//div[@id='sign-survey']/dl/dd[1]/i").click()
            self.browser.find_element_by_css_selector(".dialog-confirm").click()
        except:
            return True

    # ------模拟操作之发布博文（一天能进行无数次，有效次数两次）----------
    def publishBlogModel(self):
        WebDriverWait(self.browser, 20, 0.5).until(EC.element_to_be_clickable((By.ID, 'y-publish')))
        self.browser.find_element_by_id("y-publish").click()  # 点击发布按钮
        WebDriverWait(self.browser, 20, 0.5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'font-publish-blog')))
        self.browser.find_element_by_css_selector(".font-publish-blog").click()  # 点击博文按钮，这时产生新窗口
        self.handles = self.browser.window_handles  # 获取所有窗口句柄
        self.browser.switch_to_window(self.handles[1])  # 定位博文窗口
        WebDriverWait(self.browser, 20, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'blog-title')))
        self.browser.find_element_by_class_name('blog-title').send_keys('每日好句')  # 填写题目
        WebDriverWait(self.browser, 5, 0.5).until(EC.visibility_of_element_located((By.ID, 'ueditor_0')))
        frame = self.browser.find_element_by_id('ueditor_0')  # 获取编辑器frame
        self.browser.switch_to_frame(frame)  # 切换到编辑器frame
        text = '喜欢白色，单纯，天真，当然，在那暇净的背后也掩饰着死亡的苍凉。'
        self.browser.find_element_by_tag_name('body').send_keys(text)  # 填写文章内容
        self.browser.switch_to_default_content()  # 回退到博文主frame
        # 由于单选框被遮挡，所以使用添加执行js脚本的方法点击单选框
        self.browser.execute_script('document.getElementById(\'sync-ymm\').click()')
        self.browser.find_element_by_class_name('js-submit').click()  # 点击提交按钮
        self.browser.close()  # 关闭博文网页
        self.browser.switch_to_window(self.handles[0])  # 选中易班首页窗口

    # ------模拟操作之发布动态（一天能进行无数次，有效次数两次）----------
    def pulishTrendsModel(self):
        WebDriverWait(self.browser, 5, 0.5).until(EC.element_to_be_clickable((By.ID, 'y-publish')))
        self.browser.find_element_by_id("y-publish").click()  # 点击发布按钮
        WebDriverWait(self.browser, 5, 0.5).until(
            EC.visibility_of(self.browser.find_elements_by_class_name('font-publish-feed')[1]))
        self.browser.find_elements_by_class_name('font-publish-feed')[1].click()  # 点击动态按钮，这时产生新窗口
        self.handles = self.browser.window_handles  # 获取所有窗口句柄
        self.browser.switch_to_window(self.handles[1])  # 定位动态窗口
        WebDriverWait(self.browser, 5, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'textarea')))
        self.browser.find_element_by_class_name('textarea').send_keys('今天天气真好')
        try:
            WebDriverWait(self.browser, 3, 0.5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'guid_publish_topic')))
            self.browser.find_element_by_class_name('guid_publish_topic').click()
        except:
            print(' ')
        WebDriverWait(self.browser, 3, 0.5).until_not(
            EC.visibility_of_element_located((By.CLASS_NAME, 'guid_publish_topic')))
        self.browser.find_element_by_class_name('js-submit').click()  # 点击提交按钮
        self.browser.close()  # 关闭博文网页
        self.browser.switch_to_window(self.handles[0])  # 选中易班首页窗口

    # ------模拟操作之发布话题（一天能进行无数次，有效次数两次）----------
    def pulishTopicModel(self):
        WebDriverWait(self.browser, 10, 0.5).until(EC.element_to_be_clickable((By.ID, 'y-publish')))
        self.browser.find_element_by_id("y-publish").click()  # 点击发布按钮
        WebDriverWait(self.browser, 5, 0.5).until(
            EC.visibility_of(self.browser.find_elements_by_class_name('font-publish-topic')[1]))
        self.browser.find_elements_by_class_name('font-publish-topic')[1].click()  # 点击话题按钮，这时产生新窗口
        self.handles = self.browser.window_handles  # 获取所有窗口句柄
        self.browser.switch_to_window(self.handles[1])  # 定位话题窗口
        WebDriverWait(self.browser, 30, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'topic-title')))
        self.browser.find_element_by_class_name('topic-title').send_keys('每日好句')  # 填写题目
        WebDriverWait(self.browser, 10, 0.5).until(EC.element_to_be_clickable((By.TAG_NAME, 'iframe')))
        frame = self.browser.find_element_by_id('ueditor_0')  # 获取编辑器frame
        self.browser.switch_to_frame(frame)  # 切换到编辑器frame
        text = '喜欢白色，单纯，天真，当然，在那暇净的背后也掩饰着死亡的苍凉。'
        self.browser.find_element_by_tag_name('body').send_keys(text)  # 填写文章内容
        self.browser.switch_to_default_content()  # 回退到博文主frame
        self.browser.execute_script("window.scrollBy(0, 700)")  # 滚动屏幕
        self.browser.execute_script("arguments[0].click()",
                                    self.browser.find_elements_by_xpath('//label')[1])  # 点击发布范围单选框
        self.browser.find_element_by_class_name('js-submit').click()  # 点击提交按钮
        self.browser.close()  # 关闭博文网页
        self.browser.switch_to_window(self.handles[0])  # 选中易班首页窗口

    # ------模拟操作之更改个人信息（一天能进行无数次，一次有效）----------
    def changeInformationModel(self):
        WebDriverWait(self.browser, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//i[@title="个人主页"]')))
        self.browser.find_element_by_xpath('//i[@title="个人主页"]').click()  # 点击个人主页按钮
        WebDriverWait(self.browser, 10, 0.5).until(EC.element_to_be_clickable((By.ID, 'view-userinfo')))
        self.browser.find_element_by_id("view-userinfo").click()  # 点击查看个人信息按钮
        WebDriverWait(self.browser, 10, 0.5).until(EC.visibility_of_element_located(
            (By.XPATH, '//div[@id="userinfo-popup"]//div[@class="iblock last-child"]/a')))
        self.browser.find_element_by_xpath(
            '//div[@id="userinfo-popup"]//div[@class="iblock last-child"]/a').click()  # 点击个人主页按钮
        WebDriverWait(self.browser, 10, 0.5).until(EC.element_to_be_clickable((By.ID, 'nick')))
        name = self.browser.find_element_by_id('nick').get_attribute('value')
        nameList = ['笨', '蛋']
        for i in nameList:
            if (i != name):
                self.browser.find_element_by_id('nick').clear()
                self.browser.find_element_by_id('signature').clear()
                self.browser.find_element_by_id('nick').send_keys(i)
                self.browser.find_element_by_id('signature').send_keys(i)
        WebDriverWait(self.browser, 10, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit')))
        self.browser.find_element_by_class_name('submit').click()
        WebDriverWait(self.browser, 10, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'alert_sure')))
        self.browser.find_element_by_class_name('alert_sure').click()
        self.browser.back()
        self.browser.back()


# ------主函数-----------
if __name__ == '__main__':
    m = Main()  # 声明主类
    m.initWebkit()  # 打开浏览器
    m.loginModel()  # 登陆易班
    m.signInModel()  # 签到
    m.publishBlogModel()  # 发布博文
    m.pulishTrendsModel()  # 发布动态
    m.pulishTopicModel()  # 发布话题
    m.changeInformationModel()  # 更改个人信息
