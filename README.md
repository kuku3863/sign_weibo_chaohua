### 微博超话一键签到

![访问量统计](https://komarev.com/ghpvc/?username=wd210010&style=flat-square)

通过分析得知，cardlist中c,s,gsid,from,containerid为必须参数
aid应该是身份信息，其他参数可以自行验证是否必须

#### 主要功能

- 一键签到微博超话
- 发微博功能，使用相同的cookies

---

### 更新日志

- **2024-07-26**：新增`send_weibo.py`发微博，使用status方式的环境变量`status_taobudiao`，并新增`WEIBO_CONTENT`环境变量，用于写入发送微博的内容。
- **2024-07-20**：新增`chaohua_sign.py`，修改了原来的`weibo_chaohua_sign.py`。
- **2023-08-14**：新增获取用户名，新增`multi_user_weibo_sign.py`，支持多用户，使用方法是之前环境变量`weibo_my_cookie`用`;`隔开多用户（弃用）。
- **2023-08-09**：新增推送功能。

---

### 环境要求

- Docker
- 青龙面板
- Python

---

### 使用说明

提供了两种方式来使用这个项目：一种是在本地运行，另一种是通过青龙面板。

---

### 方式一：在本地运行

1. **复制代码**：
   - 把仓库中的`weibo_chaohua_sign.py`内容全部复制，或者直接下载下来。

2. **修改代码**：
   - 首先新增一个变量`weibo_my_cookie`，值为之前抓包得到的`https://api.weibo.cn/2/cardlist`开头的链接。
   - 注释掉最后面`params = extract_params(os.getenv("weibo_my_cookie"))`这一行。
   - 把`# params = extract_params(weibo_my_cookie)`的注释去掉。
   - 运行脚本。

---

### 方式二：使用青龙面板

1. **依赖管理**：
   - 选择`python3`。
   - 点击右上角 "新建依赖"，名称填`requests`。

2. **添加脚本**：
   - 选择"脚本管理"，点击右上角"+"按钮。
   - 类型选择"空文件"，文件名自定义，如：`weibo_sign.py`。注意后缀必须添加。
   - 点击确定完成新建。

3. **添加代码**：
   - 点击左侧`weibo_sign.py`，点击右上角编辑按钮。
   - 将仓库中的`weibo_chaohua_sign.py`文件中的内容全部复制过来，然后点击保存。

4. **环境变量**：
   - 点击左侧环境变量，点击右上角新建变量。
   - 名称填`weibo_my_cookie`，值填抓包到的地址（`https://api.weibo.cn/2/cardlist?`开头的）。

5. **定时任务**：
   - 点击"定时任务"，点击右上角新建任务，名称自定义。
   - 命令/脚本，填写刚才的文件，即：`weibo_chaohua_sign.py`。
   - 定时规则根据自己需求，例如：`0 10 21 * * ?` 代表每天晚上9点10分执行。

6. **测试**：
   - 点击"定时任务"，找到添加好的任务，点击操作下面的第一个按钮，运行测试。

---

### 获取链接

首先，打开APP，使用抓包工具获取链接。

#### 第一种：cardlist链接方式

1. 打开APP
   ![打开 APP](images/20230804213711.jpg)

2. 运行抓包软件，搜索cardlist，找到对应的链接并打开。
   ![抓包](images/20230804213710.jpg)

3. 复制以`https://api.weibo.cn/2/cardlist`开头的链接。
   ![找到数据](images/20230804222552.jpg)

#### 第二种：status链接方式

1. 打开APP
   ![微博](https://github.com/user-attachments/assets/789233c7-7468-45d7-8b15-078e1a1f3a4c)
   ![微博](https://github.com/user-attachments/assets/be3326b3-4b25-4654-9ebd-92ec41881cfb)

2. 运行抓包软件，搜索status，找到对应的链接并打开。
   ![111](https://github.com/user-attachments/assets/fecbdae8-52ca-4ddd-a655-229289cb2f79)

3. 复制以`https://api.weibo.cn/2/statuses`开头的链接。
   ![222](https://github.com/user-attachments/assets/69c375e1-0b87-448e-a8e5-3d3e2ba30b67)

---

### 运行结果

![运行结果](https://github.com/user-attachments/assets/f5276d6b-6378-44dd-b188-3a30251a1564)

---

### 推送功能

#### 使用QQ邮箱推送

修改以下参数：

- `SMTP_SERVER`: `smtp.qq.com:465`
- `SMTP_SSL`: `true`
- `SMTP_EMAIL`: `你的QQ邮箱`
- `SMTP_PASSWORD`: `授权码`
- `SMTP_NAME`: `随意填`

#### 使用Server酱推送

修改以下参数：

- `PUSH_KEY`: `Server酱的PUSH_KEY`

---

### 其他

- 青龙面板使用方法请参考[青龙面板文档](https://github.com/whyour/qinglong)。
- 如有疑问，欢迎向我提问。
