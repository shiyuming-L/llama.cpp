# llama-cli 运行输出解释

本文档详细解释 `llama-cli` 启动时的输出内容。

---

## 输出原文

```text
Loading model...


▄▄ ▄▄
██ ██
██ ██  ▀▀█▄ ███▄███▄  ▀▀█▄    ▄████ ████▄ ████▄
██ ██ ▄█▀██ ██ ██ ██ ▄█▀██    ██    ██ ██ ██ ██
██ ██ ▀█▄██ ██ ██ ██ ▀█▄██ ██ ▀████ ████▀ ████▀
                                    ██    ██
                                    ▀▀    ▀▀

build      : b9782-f9c3ebb67
model      : D:/LM-Studio/LM Studio models/models/repository/SEX_ROLEPLAY-3.2-1B.i1-Q6_K.gguf
modalities : text

available commands:
  /exit or Ctrl+C     stop or exit
  /regen              regenerate the last response
  /clear              clear the chat history
  /read <file>        add a text file
  /glob <pattern>     add text files using globbing pattern


> 
```

---

## 逐段解释

### 1. 模型加载提示

```text
Loading model...
```

- 表示正在将模型从磁盘加载到内存
- 加载时间取决于模型大小和硬盘速度
- 1.2GB 的 1B 模型通常 2-5 秒
- 8GB 的 14B 模型可能需要 10-20 秒

---

### 2. ASCII Logo

```text
▄▄ ▄▄
██ ██
██ ██  ▀▀█▄ ███▄███▄  ▀▀█▄    ▄████ ████▄ ████▄
██ ██ ▄█▀██ ██ ██ ██ ▄█▀██    ██    ██ ██ ██ ██
██ ██ ▀█▄██ ██ ██ ██ ▀█▄██ ██ ▀████ ████▀ ████▀
                                    ██    ██
                                    ▀▀    ▀▀
```

- llama.cpp 的 ASCII 艺术 Logo
- 纯装饰，没有实际功能
- 每次启动都会显示

---

### 3. 版本和模型信息

```text
build      : b9782-f9c3ebb67
model      : D:/LM-Studio/LM Studio models/models/repository/SEX_ROLEPLAY-3.2-1B.i1-Q6_K.gguf
modalities : text
```

| 字段 | 值 | 含义 |
| --- | --- | --- |
| `build` | `b9782-f9c3ebb67` | 编译版本号（commit hash） |
| `model` | 模型文件路径 | 当前加载的模型文件 |
| `modalities` | `text` | 模态类型（text=纯文本，其他可能是 vision/audio） |

---

### 4. 可用命令列表

```text
available commands:
  /exit or Ctrl+C     stop or exit
  /regen              regenerate the last response
  /clear              clear the chat history
  /read <file>        add a text file
  /glob <pattern>     add text files using globbing pattern
```

这是交互模式下可用的内置命令：

| 命令 | 作用 |
| --- | --- |
| `/exit` 或 `Ctrl+C` | 退出程序 |
| `/regen` | 重新生成上一个回复 |
| `/clear` | 清空聊天历史，重新开始 |
| `/read <file>` | 读取一个文本文件，将其内容作为上下文 |
| `/glob <pattern>` | 使用 glob 模式批量添加文本文件 |

---

### 5. 输入提示符

```text
>
```

- `>` 是用户输入提示符
- 在这里输入你想说的话，模型会回复
- 支持多行输入（按回车换行，空行发送）

---

## 交互示例

```text
>你好，请介绍一下自己

你好！我是一个 AI 助手，很高兴认识你。我可以帮助你回答问题、进行对话、
创作内容等。有什么我可以帮你的吗？

> /clear

[聊天历史已清空]

> 这是一个新的对话

...
```

---

## 启动参数对应关系

你使用的命令：

```bash
build/bin/Release/llama-cli -m "模型路径" -ngl 99 -cnv
```

| 参数 | 作用 | 在输出中的体现 |
| --- | --- | --- |
| `-m "模型路径"` | 指定模型文件 | `model: D:/LM-Studio/...` |
| `-ngl 99` | GPU 加速（加载时显示 CUDA 信息） | 加载时会显示 GPU 设备信息 |
| `-cnv` | 进入对话模式 | 显示 `>` 提示符，支持交互 |

---

## 注意事项

1. **加载时间**: 首次加载较慢，因为需要将模型权重读入内存
2. **显存占用**: `-ngl 99` 会将所有层放入 GPU，占用显存约等于模型大小
3. **交互模式**: 使用 `-cnv` 参数才会进入对话模式，否则会一次性生成后退出
4. **历史记录**: 对话历史保存在内存中，退出程序后丢失
