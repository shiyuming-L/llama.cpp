# 我常用命令

记录个人习惯使用的命令，方便快速查找。

---

## 基本运行

```bash
# 示例：
# build/bin/Release/llama-cli -m "D:/LM-Studio/LM Studio models/models/repository/SEX_ROLEPLAY-3.2-1B.i1-Q6_K.gguf" -ngl 99
```

---

## GPU 加速

```bash
# 示例：
# build/bin/Release/llama-cli -m 模型.gguf -ngl 99
```

---

## 对话模式

```bash
# 示例：
# build/bin/Release/llama-cli -m 模型.gguf -cnv
```

---

## API 服务器

```bash
# 示例：
# build/bin/Release/llama-server -m 模型.gguf --host 0.0.0.0 --port 8080 -ngl 99
```

---

## 性能测试

```bash
# 示例：
# build/bin/Release/llama-bench -m 模型.gguf -ngl 99
```

---

## 自定义命令

<!-- 在这里添加你习惯使用的命令 -->
