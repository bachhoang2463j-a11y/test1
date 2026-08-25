# RPG Combat 静态资源库 (my_assets)

本仓库为 **RPG 战斗系统 / 酒馆网页端** 提供统一的音频、音效、特效视频、角色立绘与头像等媒体资源托管，并附带开箱即用的**多线程跨域本地静态资源服务器**脚本。

---

## 📁 目录结构概览

```text
.
├── BGM_fanren/               # 背景音乐库 (凡人修仙传/仙侠风格等 20+ 首 BGM)
├── 埃利奥特/                 # 角色专属语音 (回合开始、第一回合、半血等)
├── 弗兰克/                   # 角色专属语音
├── 玛德琳/                   # 角色专属语音
├── 索恩/                     # 角色专属语音
├── 头像/                     # 角色头像图标 (包含压缩优化版及原图备份)
├── 立绘/                     # 角色全身立绘与战斗形象 (含立绘压缩优化版)
│
├── *.mp3 / *.wav             # 根目录基础战斗与环境音效 (攻击、破防、看破、法术、斩杀等)
├── *.webm / *.mp4            # 根目录技能特效与全屏动画 (斩击、弹幕、火冰雷、爆炸等)
│
├── serve_assets.py           # Python 高性能 Threading + CORS/CORP 本地静态服务器
├── 启动my_assets服务器.bat    # Windows 一键启动脚本
└── README.md                 # 仓库说明文档
```

---

## 🚀 本地资源服务快速启动

为了解决浏览器跨域（CORS）、CORP 隔离策略以及大文件/并发预加载时的排队问题，仓库内置了定制版静态服务器。

### 方法一：Windows 一键启动（推荐）
直接双击根目录下的 **`启动my_assets服务器.bat`** 即可自动检测 Python 环境并启动服务。

### 方法二：命令行启动
```bash
# 默认监听 0.0.0.0:8766，支持局域网内其他设备（如手机端酒馆）共同访问
python serve_assets.py --port 8766 --host 0.0.0.0

# 可选参数指定其他目录或端口：
python serve_assets.py --port 8767 --dir "D:\Project\my_assets"
```

### 🌟 服务端核心特性
1. **高并发不卡顿**：基于 `ThreadingHTTPServer`，解决多资源并发加载（如战斗开局同时预加载 30+ 资源）时的串行阻塞问题。
2. **完整跨域支持**：
   - 注入 `Access-Control-Allow-Origin: *`
   - 注入 `Cross-Origin-Resource-Policy: cross-origin`
   - 支持 `Range` 分片请求与 `206 Partial Content`，音视频拖动进度条即时响应。
3. **显式 MIME 补全**：自动补齐 `.webm`、`.mp4`、`.mp3`、`.wav`、`.ogg` 等媒体类型，避免被浏览器识别为二进制下载流。

---

## 🔗 前端调用示例

在前端战斗页面（如 `RpgCombat`）或酒馆插件中，配置静态资源根地址：

```javascript
// 资源服务器基础地址 (本机或局域网 IP)
const ASSET_BASE = "http://127.0.0.1:8766"; 
// 局域网手机访问示例：const ASSET_BASE = "http://192.168.110.83:8766";

// 1. 播放基础攻击音效
const sfx = new Audio(`${ASSET_BASE}/atk1.mp3`);
sfx.play();

// 2. 播放角色中文语音 (建议使用 encodeURIComponent 避免编码问题)
const voiceUrl = `${ASSET_BASE}/${encodeURIComponent('索恩')}/${encodeURIComponent('索恩_第一回合.mp3')}`;
const voice = new Audio(voiceUrl);
voice.play();

// 3. 技能特效视频 (跨域 video 渲染至 Canvas)
const video = document.createElement('video');
video.crossOrigin = 'anonymous';
video.src = `${ASSET_BASE}/strafe-ezremove.mp4`;
```

---

## 🛠️ 仓库维护与文件更新

本仓库基于 Git 增量版本控制，**完全支持单独增删或更新单个文件**（无需重新上传已有的大型多媒体资源）：

* **通过 Git 命令行更新**：
  ```bash
  git add <新增或修改的文件>
  git commit -m "更新说明"
  git push origin main
  ```
* **通过 GitHub 网页端上传**：
  点击网页右上角 **Add file** $\rightarrow$ **Upload files**，直接拖拽需要更新的文件并提交即可。
