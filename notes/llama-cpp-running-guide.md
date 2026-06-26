# llama.cpp 运行指南

本文档介绍如何运行 llama.cpp，包括各种运行方式、可用工具、可调参数和性能优化。

---

## 目录

1. [可用工具一览](#可用工具一览)
2. [运行方式](#运行方式)
3. [参数详解](#参数详解)
4. [性能优化建议](#性能优化建议)
5. [常见问题](#常见问题)
6. [环境变量](#环境变量)

---

## 可用工具一览

编译完成后，`build/bin/Release/` 目录下包含以下工具：

### 核心工具

| 工具 | 说明 | 用途 |
| --- | --- | --- |
| `llama-cli` | 命令行交互工具 | 本地对话、测试模型 |
| `llama-server` | API 服务器 | 提供 OpenAI 兼容 API |
| `llama-bench` | 性能基准测试 | 测试推理速度 |
| `llama-quantize` | 模型量化工具 | 转换模型量化格式 |

### 模型工具

| 工具 | 说明 |
| --- | --- |
| `llama-gguf` | 查看/修改 GGUF 文件信息 |
| `llama-gguf-hash` | 计算 GGUF 文件哈希 |
| `llama-gguf-split` | 分割/合并大模型文件 |
| `llama-export-lora` | 导出 LoRA 适配器 |
| `llama-imatrix` | 计算重要性矩阵 |
| `llama-perplexity` | 计算模型困惑度 |
| `llama-quantize` | 模型量化 |
| `llama-tokenize` | 测试分词器 |

### 多模态工具

| 工具 | 说明 |
| --- | --- |
| `llama-mtmd-cli` | 多模态命令行工具 |
| `llama-mtmd-debug` | 多模态调试工具 |
| `llama-gemma3-cli` | Gemma3 专用工具 |
| `llama-llava-cli` | LLaVA 专用工具 |
| `llama-minicpmv-cli` | MiniCPM-V 专用工具 |
| `llama-qwen2vl-cli` | Qwen2VL 专用工具 |

### 示例程序

| 工具 | 说明 |
| --- | --- |
| `llama-simple` | 最简推理示例 |
| `llama-simple-chat` | 简单对话示例 |
| `llama-batched` | 批处理示例 |
| `llama-embedding` | 文本嵌入示例 |
| `llama-speculative` | 推测解码示例 |
| `llama-parallel` | 并行推理示例 |
| `llama-lookahead` | Lookahead 解码示例 |
| `llama-lookup` | Lookup 解码示例 |
| `llama-finetune` | 模型微调示例 |

### 测试工具

| 工具 | 说明 |
| --- | --- |
| `test-backend-ops` | 后端运算测试 |
| `test-tokenizer-0` | 分词器测试 |
| `test-gguf` | GGUF 格式测试 |
| `test-chat-template` | 对话模板测试 |
| `test-quantize-fns` | 量化函数测试 |
| ... | 等 30+ 测试程序 |

---

## 运行方式

### 1. 本地对话（llama-cli）

#### 基本用法

```bash
# 使用本地模型
build/bin/Release/llama-cli -m 模型路径.gguf

# 从 Hugging Face 下载并运行
build/bin/Release/llama-cli -hf ggml-org/gemma-3-1b-it-GGUF

# 带参数运行
build/bin/Release/llama-cli -m 模型.gguf -ngl 99 -c 4096 -t 8
```

#### 常用命令

```bash
# 单次问答
build/bin/Release/llama-cli -m 模型.gguf -p "你好" -n 100

# 对话模式
build/bin/Release/llama-cli -m 模型.gguf -cnv

# 从文件读取提示词
build/bin/Release/llama-cli -m 模型.gguf -f prompt.txt

# 使用系统提示词
build/bin/Release/llama-cli -m 模型.gguf -sys "你是一个助手"
```

### 2. API 服务器（llama-server）

#### 启动服务器

```bash
# 基本启动
build/bin/Release/llama-server -m 模型.gguf

# 指定端口和主机
build/bin/Release/llama-server -m 模型.gguf --host 0.0.0.0 --port 8080

# 启用 GPU 加速
build/bin/Release/llama-server -m 模型.gguf -ngl 99

# 启用 API Key 认证
build/bin/Release/llama-server -m 模型.gguf --api-key your-key
```

#### API 端点

| 端点 | 方法 | 说明 |
| --- | --- | --- |
| `/v1/chat/completions` | POST | 聊天补全（OpenAI 兼容） |
| `/v1/completions` | POST | 文本补全 |
| `/v1/embeddings` | POST | 文本嵌入 |
| `/v1/models` | GET | 列出可用模型 |
| `/health` | GET | 健康检查 |
| `/v1/reranking` | POST | 重排序（需启用） |

#### curl 示例

```bash
# 聊天补全
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model",
    "messages": [{"role": "user", "content": "你好"}],
    "temperature": 0.7
  }'

# 文本补全
curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model",
    "prompt": "从前有座山",
    "max_tokens": 100
  }'
```

### 3. 性能测试（llama-bench）

```bash
# 基本测试
build/bin/Release/llama-bench -m 模型.gguf

# 测试 GPU 加速效果
build/bin/Release/llama-bench -m 模型.gguf -ngl 0   # CPU
build/bin/Release/llama-bench -m 模型.gguf -ngl 99  # GPU

# 比较不同量化
build/bin/Release/llama-bench -m 模型-Q4_K_M.gguf
build/bin/Release/llama-bench -m 模型-Q8_0.gguf
```

### 4. 模型量化（llama-quantize）

```bash
# 量化模型
build/bin/Release/llama-quantize 输入.gguf 输出.gguf Q4_K_M

# 可用量化类型
# Q2_K, Q3_K_S, Q3_K_M, Q3_K_L, Q4_0, Q4_K_S, Q4_K_M
# Q5_0, Q5_K_S, Q5_K_M, Q6_K, Q8_0, F16, BF16
```

---

## 参数详解

### 通用参数

#### 模型加载

| 参数 | 短写 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--model FNAME` | `-m` | 无 | 模型文件路径 |
| `--hf-repo <user>/<model>` | `-hf` | 无 | Hugging Face 模型仓库 |
| `--hf-file FILE` | `-hff` | 无 | Hugging Face 指定文件 |
| `--model-url URL` | `-mu` | 无 | 模型下载 URL |
| `--docker-repo <repo>/<model>` | `-dr` | 无 | Docker Hub 模型 |

#### GPU 配置

| 参数 | 短写 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--n-gpu-layers N` | `-ngl` | auto | **GPU 卸载层数**，最重要的 GPU 参数 |
| `--device <dev1,dev2>` | `-dev` | 无 | 指定使用的设备 |
| `--list-devices` | 无 | 无 | 列出可用设备 |
| `--split-mode {none,layer,row,tensor}` | `-sm` | layer | 多 GPU 分割模式 |
| `--tensor-split N0,N1` | `-ts` | 无 | 多 GPU 张量分割比例 |
| `--main-gpu INDEX` | `-mg` | 0 | 主 GPU 索引 |
| `--fit [on\|off]` | `-fit` | on | 自动调整参数适配显存 |
| `--fit-target MiB` | `-fitt` | 1024 | 显存目标余量 |
| `--kv-offload` | `-kvo` | on | KV 缓存卸载到 GPU |
| `--flash-attn [on\|off\|auto]` | `-fa` | auto | Flash Attention |
| `--cpu-moe` | `-cmoe` | off | MoE 权重保留在 CPU |

#### 上下文和批处理

| 参数 | 短写 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--ctx-size N` | `-c` | 0(模型默认) | **上下文长度** |
| `--n-predict N` | `-n` | -1(无限) | 最大生成 token 数 |
| `--batch-size N` | `-b` | 2048 | 逻辑批处理大小 |
| `--ubatch-size N` | `-ub` | 512 | 物理批处理大小 |
| `--keep N` | 无 | 0 | 保留初始提示词 token 数 |
| `--parallel N` | `-np` | 1 | 并行序列数（服务器用） |

#### 线程和 CPU

| 参数 | 短写 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--threads N` | `-t` | -1(自动) | CPU 线程数 |
| `--threads-batch N` | `-tb` | 同 --threads | 批处理线程数 |
| `--cpu-mask M` | `-C` | 无 | CPU 亲和性掩码 |
| `--cpu-range lo-hi` | `-Cr` | 无 | CPU 范围 |
| `--prio N` | 无 | 0 | 进程优先级(-1~3) |
| `--numa TYPE` | 无 | 无 | NUMA 优化 |

#### 内存管理

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--mlock` | off | 锁定模型在 RAM 中 |
| `--mmap` | on | 内存映射模型文件 |
| `--direct-io` | off | 使用 DirectIO |
| `--cache-type-k TYPE` | f16 | KV 缓存 K 的数据类型 |
| `--cache-type-v TYPE` | f16 | KV 缓存 V 的数据类型 |

**KV 缓存数据类型选项**: f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1

#### RoPE 位置编码

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--rope-scaling {none,linear,yarn}` | 模型默认 | RoPE 缩放方法 |
| `--rope-scale N` | 无 | 上下文扩展因子 |
| `--rope-freq-base N` | 模型默认 | RoPE 基础频率 |
| `--rope-freq-scale N` | 无 | 频率缩放因子 |
| `--yarn-orig-ctx N` | 0 | YaRN 原始上下文大小 |
| `--yarn-ext-factor N` | -1.0 | YaRN 外推混合因子 |

---

### 采样参数

#### 采样器序列

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--samplers SAMPLERS` | penalties;dry;top_n_sigma;top_k;typ_p;top_p;min_p;xtc;temperature | 采样器顺序 |
| `--sampler-seq SEQ` | edskypmxt | 简化的采样器序列 |

#### 温度控制

| 参数 | 短写 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--temperature N` | `--temp` | 0.8 | **温度**，控制随机性 |
| `--dynatemp-range N` | 无 | 0.0 | 动态温度范围 |
| `--dynatemp-exp N` | 无 | 1.0 | 动态温度指数 |

**温度说明**:

- `0.0`: 确定性输出，总是选择最可能的 token
- `0.1-0.5`: 较保守，适合事实性回答
- `0.6-0.9`: 平衡，适合一般对话
- `1.0+`: 较随机，适合创意写作

#### Top-K 采样

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--top-k N` | 40 | 从概率最高的 K 个 token 中采样 |

**Top-K 说明**:

- `1`: 贪心解码，总是选最可能的
- `10-50`: 常用范围
- `0`: 禁用

#### Top-P (Nucleus) 采样

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--top-p N` | 0.95 | 累积概率阈值 |

**Top-P 说明**:

- `0.9`: 只考虑累积概率 90% 的 token
- `0.95`: 常用值
- `1.0`: 禁用

#### Min-P 采样

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--min-p N` | 0.05 | 最小概率阈值（相对于最可能的 token） |

**Min-P 说明**:

- `0.0`: 禁用
- `0.05-0.1`: 常用范围
- 过滤掉概率低于最可能 token 一定比例的选项

#### 重复惩罚

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--repeat-penalty N` | 1.0 | 重复 token 惩罚系数 |
| `--presence-penalty N` | 0.0 | 存在惩罚 |
| `--frequency-penalty N` | 0.0 | 频率惩罚 |
| `--repeat-last-n N` | 64 | 考虑的最后 N 个 token |

**惩罚说明**:

- `repeat-penalty > 1.0`: 惩罚重复
- `presence-penalty > 0.0`: 鼓励新话题
- `frequency-penalty > 0.0`: 惩罚高频词

#### DRY 采样

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--dry-multiplier N` | 0.0 | DRY 采样乘数 |
| `--dry-base N` | 1.75 | DRY 基础值 |
| `--dry-allowed-length N` | 2 | 允许的重复长度 |
| `--dry-penalty-last-n N` | -1 | DRY 惩罚范围 |

#### 其他采样器

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--typical-p N` | 1.0 | 典型采样参数 |
| `--top-n-sigma N` | -1.0 | Top-N-Sigma 采样 |
| `--xtc-probability N` | 0.0 | XTC 概率 |
| `--xtc-threshold N` | 0.10 | XTC 阈值 |
| `--mirostat N` | 0 | Mirostat 采样 (0=禁用, 1=v1, 2=v2) |
| `--mirostat-lr N` | 0.10 | Mirostat 学习率 |
| `--mirostat-ent N` | 5.00 | Mirostat 目标熵 |
| `--adaptive-target N` | -1.0 | 自适应 P 目标 |
| `--adaptive-decay N` | 0.90 | 自适应 P 衰减率 |

#### 高级采样

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--seed SEED` | -1 | 随机种子（-1=随机） |
| `--logit-bias ID(+/-)BIAS` | 无 | 调整特定 token 概率 |
| `--ignore-eos` | off | 忽略结束符继续生成 |
| `--grammar GRAMMAR` | 无 | BNF 语法约束 |
| `--json-schema SCHEMA` | 无 | JSON Schema 约束 |
| `--backend-sampling` | off | 后端采样（实验） |

---

### 服务器特有参数

| 参数 | 短写 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--host HOST` | 无 | 127.0.0.1 | 监听地址 |
| `--port PORT` | 无 | 8080 | 监听端口 |
| `--api-key KEY` | 无 | 无 | API 认证密钥 |
| `--api-key-file FNAME` | 无 | 无 | API 密钥文件 |
| `--ssl-key-file FNAME` | 无 | 无 | SSL 私钥文件 |
| `--ssl-cert-file FNAME` | 无 | 无 | SSL 证书文件 |
| `--timeout N` | `-to` | 3600 | 读写超时（秒） |
| `--ui [on\|off]` | `--webui` | on | 启用 Web UI |
| `--path PATH` | 无 | 无 | 静态文件路径 |
| `--api-prefix PREFIX` | 无 | 无 | API 路径前缀 |
| `--embedding` | `--embeddings` | off | 嵌入模式 |
| `--reranking` | `--rerank` | off | 重排序模式 |
| `--cont-batching` | `-cb` | on | 连续批处理 |
| `--pooling TYPE` | 无 | 模型默认 | 嵌入池化类型 |
| `--image-min-tokens` | 无 | 模型默认 | 图片最小 token 数 |
| `--image-max-tokens` | 无 | 模型默认 | 图片最大 token 数 |

---

### 推测解码参数

推测解码使用小型"草稿"模型加速大型"目标"模型的推理：

| 参数 | 说明 |
| --- | --- |
| `--model-draft FNAME` | 草稿模型路径 |
| `--hf-repo-draft REPO` | 草稿模型 HF 仓库 |
| `--n-gpu-layers-draft N` | 草稿模型 GPU 层数 |
| `--spec-draft-n-max N` | 草稿 token 最大数量 |
| `--spec-draft-n-min N` | 草稿 token 最小数量 |
| `--spec-type TYPE` | 推测解码类型 |

**推测解码类型**:

- `none`: 禁用
- `draft-simple`: 简单草稿模型
- `draft-eagle3`: Eagle3 草稿
- `draft-mtp`: MTP 草稿
- `ngram-simple`: N-gram 简单
- `ngram-map-k`: N-gram 映射
- `ngram-mod`: N-gram 模块

---

### 其他参数

#### LoRA 适配器

| 参数 | 说明 |
| --- | --- |
| `--lora FNAME` | LoRA 适配器路径 |
| `--lora-scaled FNAME:SCALE` | 带缩放的 LoRA |

#### 控制向量

| 参数 | 说明 |
| --- | --- |
| `--control-vector FNAME` | 控制向量文件 |
| `--control-vector-scaled FNAME:SCALE` | 带缩放的控制向量 |
| `--control-vector-layer-range START END` | 控制向量作用层范围 |

#### 日志和调试

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--log-disable` | off | 禁用日志 |
| `--log-file FNAME` | 无 | 日志文件 |
| `--log-colors [on\|off\|auto]` | auto | 日志颜色 |
| `--verbose` | off | 详细输出 |
| `--log-verbosity N` | 1 | 日志级别 (0-5) |
| `--log-timestamps` | off | 日志时间戳 |
| `--offline` | off | 离线模式 |
| `--check-tensors` | off | 检查张量数据 |
| `--perf` | off | 性能计时 |

---

## 性能优化建议

### 1. GPU 加速

```bash
# 最重要的参数：-ngl
# 设置为 99 或 "all" 把所有层放到 GPU
llama-cli -m 模型.gguf -ngl 99

# 或使用 auto 自动适配
llama-cli -m 模型.gguf -ngl auto
```

### 2. 上下文长度

```bash
# 根据需要设置，不要设太大浪费显存
llama-cli -m 模型.gguf -c 4096  # 4K 上下文
llama-cli -m 模型.gguf -c 8192  # 8K 上下文
```

### 3. KV 缓存量化

```bash
# 量化 KV 缓存节省显存
llama-cli -m 模型.gguf -ctk q8_0 -ctv q8_0
```

### 4. Flash Attention

```bash
# 启用 Flash Attention（如果支持）
llama-cli -m 模型.gguf -fa on
```

### 5. 线程数设置

```bash
# 设置为 CPU 核心数
llama-cli -m 模型.gguf -t 8
```

### 6. 批处理大小

```bash
# 增大批处理可加速 prompt 处理
llama-cli -m 模型.gguf -b 2048 -ub 512
```

### 7. 内存锁定

```bash
# 防止模型被换出到磁盘
llama-cli -m 模型.gguf --mlock
```

---

## 常见问题

### Q: 如何查看 GPU 是否工作？

运行时会显示类似信息：

```text
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA GeForce RTX 4050 Laptop GPU, compute capability 8.9, VMM: yes
```

### Q: 显存不够怎么办？

1. 减少 GPU 层数：`-ngl 20`（部分层用 GPU）
2. 使用更小的量化：Q4_K_M 或 Q3_K_S
3. 减小上下文长度：`-c 2048`
4. 量化 KV 缓存：`-ctk q4_0 -ctv q4_0`
5. 使用 `--fit` 自动适配：`-fit on`

### Q: 如何选择量化类型？

```text
显存充足 (>=8GB)  → Q8_0 或 Q6_K
显存中等 (4-8GB)  → Q4_K_M（推荐）
显存紧张 (2-4GB)  → Q3_K_S
极致压缩 (<2GB)   → Q2_K（质量有损）
```

### Q: 服务器如何对外访问？

```bash
llama-server -m 模型.gguf --host 0.0.0.0 --port 8080
```

### Q: 如何使用多个 GPU？

```bash
# 层分割（默认，推荐）
llama-server -m 模型.gguf -sm layer -ts 3,1

# 行分割
llama-server -m 模型.gguf -sm row
```

### Q: 如何限制生成长度？

```bash
# 生成 100 个 token 后停止
llama-cli -m 模型.gguf -n 100

# 使用 -1 无限生成（直到遇到结束符）
llama-cli -m 模型.gguf -n -1
```

### Q: 如何提高生成质量？

1. 使用更高的量化（Q8_0 > Q6_K > Q4_K_M）
2. 降低温度（0.3-0.7）
3. 使用 Top-P 采样（0.9-0.95）
4. 设置重复惩罚（1.1-1.3）
5. 使用更大的模型

---

## 环境变量

| 变量 | 说明 |
| --- | --- |
| `LLAMA_ARG_MODEL` | 模型路径 |
| `LLAMA_ARG_CTX_SIZE` | 上下文长度 |
| `LLAMA_ARG_N_PREDICT` | 最大生成数 |
| `LLAMA_ARG_THREADS` | 线程数 |
| `LLAMA_ARG_N_GPU_LAYERS` | GPU 层数 |
| `LLAMA_ARG_BATCH` | 批处理大小 |
| `LLAMA_ARG_UBATCH` | 物理批处理大小 |
| `LLAMA_ARG_FLASH_ATTN` | Flash Attention |
| `LLAMA_ARG_CACHE_TYPE_K` | KV 缓存 K 类型 |
| `LLAMA_ARG_CACHE_TYPE_V` | KV 缓存 V 类型 |
| `LLAMA_ARG_HOST` | 服务器主机 |
| `LLAMA_ARG_PORT` | 服务器端口 |
| `LLAMA_API_KEY` | API 密钥 |
| `HF_TOKEN` | Hugging Face Token |
