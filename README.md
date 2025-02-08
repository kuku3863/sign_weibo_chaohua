# 微博超话一键签到 & 发微博工具

[![访问量统计](https://komarev.com/ghpvc/?username=wd210010&style=flat-square)](https://github.com/)

本项目实现了**微博超话一键签到**和**自动发微博**功能。通过分析微博接口，我们提取了 `cardlist` 中的必需参数（如：`c`、`s`、`gsid`、`from`、`containerid`），结合 cookie 信息，实现自动签到及发微博。支持多账号管理，并内置推送通知功能，让你不错过每一次签到和发微博的结果。

## 目录

- [主要功能](#主要功能)
- [更新日志](#更新日志)
- [环境要求](#环境要求)
- [安装与使用](#安装与使用)
  - [方式一：本地运行](#方式一本地运行)
  - [方式二：青龙面板部署](#方式二青龙面板部署)
- [Cookie 获取方法](#cookie-获取方法)
  - [cardlist 链接方式](#cardlist-链接方式)
  - [status 链接方式](#status-链接方式)
- [运行结果展示](#运行结果展示)
- [推送通知设置](#推送通知设置)
- [常见问题](#常见问题)
- [鸣谢与联系方式](#鸣谢与联系方式)

## 主要功能

- **一键签到微博超话**  
  自动完成微博超话的每日签到任务，支持多账号同时签到。

- **自动发微博**  
  利用同一 cookie 信息，自动发布微博，支持通过环境变量自定义微博内容。

- **推送通知**  
  集成 QQ 邮箱与 Server 酱推送，确保你第一时间收到运行结果通知。

- **灵活配置**  
  可通过环境变量或本地修改代码，自定义参数设置，满足多场景需求。

## 更新日志

- **2025-02-07**  
  - 修改了 statuses 签到版本逻辑，应对微博最新签到机制更新。  
  - 新增固定值的 `body` 参数，后续根据运行效果调整。  
  - 支持多账号签到（配置环境变量如 `status_tianqi`、`status_taobudiao`）。

- **2024-07-26**  
  - 新增 `send_weibo.py` 发微博模块，支持使用 `WEIBO_CONTENT` 环境变量自定义微博内容。

- **2024-07-20**  
  - 新增 `chaohua_sign.py`，更新了原 `weibo_chaohua_sign.py` 的逻辑。

- **2023-08-14**  
  - 新增获取用户名功能，并推出 `multi_user_weibo_sign.py` 多用户支持（原通过 `weibo_my_cookie` 分号分隔多账号方式已弃用）。

- **2023-08-09**  
  - 新增推送通知功能，确保信息及时反馈。

## 环境要求

- **Docker**（可选）
- **青龙面板**（推荐用于定时任务管理）
- **Python 3**

## 安装与使用

### 方式一：本地运行

1. **获取代码**  
   将仓库中的 `weibo_chaohua_sign.py` 文件下载或复制到本地。

2. **配置 Cookie**  
   - 新增变量 `weibo_my_cookie`，将你通过抓包获取到的以 `https://api.weibo.cn/2/cardlist` 开头的链接赋值给它。  
   - 注释掉代码中通过环境变量读取 Cookie 的部分（例如：`params = extract_params(os.getenv("weibo_my_cookie"))`），并启用本地变量读取（解除 `# params = extract_params(weibo_my_cookie)` 前的注释）。

3. **运行脚本**  
   在命令行中执行脚本，检查日志确认是否签到和发微博成功。

### 方式二：青龙面板部署

1. **依赖管理**  
   - 在青龙面板中选择 `python3` 环境。  
   - 点击右上角 “新建依赖”，添加 `requests` 模块。

2. **添加脚本**  
   - 进入“脚本管理”，点击右上角 “+” 按钮，新建一个空文件（如 `weibo_sign.py`，注意保留后缀名）。  
   - 将 `weibo_chaohua_sign.py` 的全部代码复制粘贴到文件中并保存。

3. **设置环境变量**  
   - 在青龙面板中添加环境变量 `weibo_my_cookie`，值为抓包得到的链接（以 `https://api.weibo.cn/2/cardlist` 开头）。

4. **配置定时任务**  
   - 进入“定时任务”，点击 “新建任务”，设置任务名称。  
   - 在“命令/脚本”字段中填写文件名（如 `weibo_chaohua_sign.py`）。  
   - 根据需要设置定时规则（例如：`0 10 21 * * ?` 表示每天 21:10 执行）。

5. **测试运行**  
   - 在任务列表中找到刚添加的任务，点击运行按钮进行测试。

## Cookie 获取方法

获取 Cookie 链接是使用本项目的前提，可通过两种方式：

### cardlist 链接方式

1. **打开微博 APP**  
   使用手机打开微博 APP。

   ![打开 APP](images/20230804213711.jpg)

2. **抓包定位**  
   使用抓包工具搜索关键词 `cardlist`，定位到对应链接。

   ![抓包](images/20230804213710.jpg)

3. **复制链接**  
   复制以 `https://api.weibo.cn/2/cardlist` 开头的链接，用于配置 `weibo_my_cookie`。

   ![找到数据](images/20230804222552.jpg)

### status 链接方式

1. **打开微博 APP**  
   同样打开微博 APP。

   ![微博](https://github.com/user-attachments/assets/789233c7-7468-45d7-8b15-078e1a1f3a4c)

2. **抓包定位**  
   使用抓包工具搜索 `状态` 关键词，找到对应链接。

   ![111](https://github.com/user-attachments/assets/fecbdae8-52ca-4ddd-a655-229289cb2f79)

3. **复制链接**  
   复制以 `https://api.weibo.cn/2/statuses` 开头的链接备用。

   ![222](https://github.com/user-attachments/assets/69c375e1-0b87-448e-a8e5-3d3e2ba30b67)

## 运行结果展示

工具运行成功后的示例截图如下：

![运行结果](https://github.com/user-attachments/assets/f5276d6b-6378-44dd-b188-3a30251a1564)  
![运行结果](https://github.com/kuku3863/sign_weibo_chaohua/blob/master/images/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250207112445.png)  
![运行结果](https://github.com/kuku3863/sign_weibo_chaohua/blob/master/images/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250207112506.jpg)

## 推送通知设置

本项目内置推送功能，支持以下两种方式：

### 使用 QQ 邮箱推送

请修改配置参数：

- **SMTP_SERVER**：`smtp.qq.com:465`
- **SMTP_SSL**：`true`
- **SMTP_EMAIL**：你的 QQ 邮箱地址
- **SMTP_PASSWORD**：QQ 授权码
- **SMTP_NAME**：任意名称（用于标识发送者）

### 使用 Server 酱推送

配置参数：

- **PUSH_KEY**：填入 Server 酱提供的 PUSH_KEY

## 常见问题

1. **如何获取最新的 Cookie 链接？**  
   请参考[Cookie 获取方法](#cookie-获取方法)部分。

2. **如何配置多账号签到？**  
   请使用多个环境变量（例如：`status_tianqi`、`status_taobudiao`），具体参考更新日志说明。

3. **运行中遇到问题怎么办？**  
   - 请检查 Cookie 链接是否正确。  
   - 仔细核对环境变量配置及依赖安装情况。  
   - 如仍有疑问，可在 Issue 中反馈。

## 鸣谢与联系方式

- 感谢 [青龙面板](https://github.com/whyour/qinglong) 提供的优秀定时任务管理方案。
- 欢迎 Star、Fork 和提 Issue，帮助项目不断完善。  
- 如有疑问或建议，请在 Issue 中留言交流。
