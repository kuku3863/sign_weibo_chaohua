# 微博超话一键签到

通过分析得知,cardlist中c,s,gsid,from,containerid为必须参数，count可以控制每页数量多页以后会出一个since_id,包含三个参数，其中有page，但是第一页是没有这个参数的。

使用 Python 编写的微博超话一键签到。

---

## 获取链接

首先，打开 APP，使用抓包工具获取链接。

1. 打开 APP

   ![打开 APP](images/20230804213711.jpg)

2. 运行抓包软件。我这边用的是 storm Sniffer，搜索 cardlist，找到我框中的这个，打开。

   ![抓包](images/20230804213710.jpg)

3. 复制这个以 `https[:]//api.weibo.cn/2/cardlist` 开头的链接。

   ![找到数据](images/20230804222552.jpg)

---

## 环境要求

- Docker
- 青龙面板
- Python

---

## 如何使用

提供了两种方式来使用这个项目：一种是在本地运行，另一种是通过青龙面板。

### 方式一：在本地运行

1. **复制代码**：
   - 把仓库中的weibo_chaohua_sign.py内容全部复制，或者直接下载下来。

2. **修改代码**：
   
   - ![打开 APP](images/20230807032900.jpg)
   - 首先新增一个变量weibo_my_cookie，值为之前抓包得到的 `https[:]//api.weibo.cn/2/cardlist` 开头的链接。
   - 找到最后面params = extract_params(os.getenv("weibo_my_cookie"))这一行注释掉
     把# params = extract_params(weibo_cookier)这里的注释去掉
   - 运行

### 方式二：使用青龙面板

-安装 [青龙面板](https://github.com/whyour/qinglong)。
-确保已经安装并打开了 [青龙面板](http://localhost:5700/)。

**步骤如下：**

1. **依赖管理**：
   - 选择 `python3`。
   - 点击右上角 "新建依赖"，名称填 `requests`。

2. **添加脚本**：
   - 选择 "脚本管理"，点击右上角 "+" 按钮。
   - 类型选择 "空文件"，文件名自定义，如：`weibo_sign.py`。注意后缀必须添加。
   - 点击确定完成新建。

3. **添加代码**：
   - 点击左侧 `weibo_sign.py`，点击右上角编辑按钮。
   - 将仓库中的 `weibo_chaohua_sign.py` 文件中的内容全部复制过来，然后点击保存。

4. **环境变量**：
   - 点击左侧环境变量，点击右上角新建变量。
   - 名称填 `weibo_my_cookie`，值填第一步抓包到的地址（`https://api.weibo.cn/2/cardlist?`开头的）。

5. **定时任务**：
   - 点击 "定时任务"，点击右上角新建任务，名称自定义。
   - 命令/脚本，填写刚才的文件，即：`weibo_chaohua_sign.py`。
   - 定时规则根据自己需求，可以百度查看相关规则。例如：`0 10 21 * * ?` 代表每天晚上9点10分执行。

6. **测试**：
   - 点击 "定时任务" 找到添加好的任务，点击操作下面的第一个按钮，运行测试。

   ![结果](images/20230804234216.jpg)
