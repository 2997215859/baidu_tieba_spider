# coding:utf-8
import re
import urllib2

class SpiderMain():
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        self.floor_num = 0
        self.url_base = "http://tieba.baidu.com/p/3138733512?see_lz=1&pn="

    def craw(self):
        max_page, title = self.get_max_page_and_title()
        self.fout = open('output.html', 'w')# 打开文件
        self.fout.write('<html>')
        self.fout.write('<body>')
        self.fout.write('<h1>%s</h1>' % title.encode('utf-8'))
        self.fout.write('<h3>共%s页</h3>' % max_page.encode('utf-8'))
        for page_num in range(1, int(max_page)+1):
            url = self.url_base + str(page_num)
            html_cont = self.get_html_cont(url)
            paras = self.get_paras(html_cont)
            self.write_paras(paras, page_num)

        self.fout.write('</body>')
        self.fout.write('</html>')
        self.fout.close()

    def get_html_cont(self, url):
        try:
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            print '访问url错误，错误原因如下:'
            if e.hasattr(e, 'code'):
                print e.code
            if e.hasattr(e, 'reason'):
                print e.reason

    def get_paras(self, html_cont):
        # < div
        # id = "post_content_53018668923"
        # class ="d_post_content j_d_post_content " > 很多媒体都在每赛季之前给球员排个名，我也有这个癖好…………，我会尽量理性的分析球队地位，个人能力等因素，评出我心目中的下赛季50大现役球员，这个50大是指预估他本赛季在篮球场上对球队的影响力……不是过去的荣誉什么的，所以难免有一定的主观性……如果把你喜欢的球星排低了，欢迎理性讨论！ < img class ="BDE_Image" src="http://imgsrc.baidu.com/forum/w%3D580/sign=557ae4d4fadcd100cd9cf829428947be/a9d6277f9e2f0708468564d9eb24b899a801f263.jpg" pic_ext="jpeg" pic_type="0" width="339" height="510" > < br > < br > < br > < br > 状元维金斯镇楼 < br > P.S 1 我每天都至少更新一个，不TJ。 < br > 2 今年的新秀我就不考虑了，没上赛季参照 < / div >
        pattern = re.compile('<div.*?d_post_content j_d_post_content.*?>(.*?)</div>', re.S)
        paras = re.findall(pattern, html_cont)
        return paras

    def write_paras(self, paras, page_num):
        self.fout.write('<h1>第%d页</h1>' % page_num)
        for para in paras:
            self.floor_num = self.floor_num + 1
            # print para, '\n'
            self.fout.write('<div>%s<div>' % para.encode('utf-8'))
            self.fout.write('<br /><div>%d楼 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - </div><br />' % self.floor_num)

    def get_max_page_and_title(self):
        # < li
        #
        # class ="l_reply_num" style="margin-left:8px" > < span class ="red" style="margin-right:3px" > 141 < / span > 回复贴，共 < span class ="red" > 5 < / span > 页 < / li >
        html_cont = self.get_html_cont(self.url_base+'1')
        pattern = re.compile('<li.*?l_reply_num.*?<span.*?red.*?<span.*?red.*?>(.*?)</span>', re.S)
        res = re.search(pattern, html_cont)
        max_page = res.group(1).strip()

        # < h3
        # class ="core_title_txt pull-left text-overflow  " title="纯原创我心中的NBA2014-2015赛季现役50大" style="width: 396px" > 纯原创我心中的NBA2014-2015赛季现役50大 < / h3 >
        pattern = re.compile('<h3.*?core_title_txt.*?>(.*?)<', re.S)
        res = re.search(pattern, html_cont)
        title = res.group(1).strip()
        return max_page, title

if __name__ == "__main__":
    obj_spider = SpiderMain()
    obj_spider.craw()
