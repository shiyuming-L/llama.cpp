# Claude 项目指南（llama.cpp）

> **开始工作前，请务必阅读 [AGENTS_CN.md](AGENTS_CN.md)（贡献者和 AI 助手行为准则）和 [SECURITY_CN.md](SECURITY_CN.md)（安全策略）。**

---

## 项目概述

llama.cpp 是一个纯 C/C++ 实现的大语言模型（LLM）推理引擎，无外部依赖，支持多种硬件后端（CPU、CUDA、Metal、Vulkan、SYCL 等）。它同时也是 [ggml](https://github.com/ggml-org/ggml) 库新功能的主要开发试验场。

---

## 构建方式

```bash
# 基础构建
cmake -B build
cmake --build build --config Release

# 启用 CUDA 支持
cmake -B build -DGGML_CUDA=ON

# 启用 Metal 支持（macOS）
cmake -B build -DGGML_METAL=ON

# 构建产物位于 build/bin/ 目录
```

常用构建选项：

- `-DGGML_CUDA=ON` — NVIDIA GPU 支持
- `-DGGML_HIP=ON` — AMD GPU 支持
- `-DGGML_METAL=ON` — Apple Silicon 支持
- `-DGGML_VULKAN=ON` — Vulkan GPU 支持
- `-DGGML_SYCL=ON` — Intel GPU 支持

---

## 目录结构

| 目录 | 说明 |
| --- | --- |
| `src/` | llama.cpp 核心源码（模型加载、推理逻辑等） |
| `include/` | 公共头文件（`llama.h` 等 API 定义） |
| `ggml/` | ggml 张量库（底层计算引擎） |
| `common/` | 各工具共享的通用工具代码 |
| `tools/` | 可执行工具（`server`、`cli`、`quantize`、`perplexity`、`llama-bench` 等） |
| `examples/` | 示例程序（`simple`、`embedding` 等） |
| `gguf-py/` | Python GGUF 工具库 |
| `conversion/` | 模型格式转换脚本 |
| `grammars/` | GBNF 语法文件（用于约束输出格式） |
| `tests/` | 测试代码 |
| `ci/` | CI/CD 配置 |
| `cmake/` | CMake 模块 |
| `docs/` | 文档 |
| `vendor/` | 第三方依赖 |

---

## 关键文件

| 文件 | 说明 |
| --- | --- |
| `include/llama.h` | 核心公共 API 头文件 |
| `src/llama.cpp` | 核心推理实现 |
| `src/llama-model.cpp` | 模型加载和量化实现 |
| `src/llama-context.cpp` | 上下文管理 |
| `ggml/include/ggml.h` | ggml 张量库 API |
| `ggml/src/ggml.c` | ggml 核心实现 |
| `common/arg.cpp` | 命令行参数解析 |
| `common/chat.cpp` | 聊天模板处理 |

---

## 测试

```bash
# 构建后运行测试
cd build && ctest

# 运行后端操作测试（验证 ggml 算子在不同后端的一致性）
./build/bin/test-backend-ops

# 测量困惑度
./build/bin/llama-perplexity -m model.gguf -f file.txt

# 性能基准测试
./build/bin/llama-bench -m model.gguf
```

---

## 代码规范摘要

- 使用 `snake_case` 命名函数、变量和类型
- 使用 4 空格缩进，大括号在同一行
- 避免使用花哨的 STL 语法，保持简单
- 优先复用已有基础设施，避免引入新依赖
- 使用 sized 整数类型（如 `int32_t`）
- 结构体使用 `struct foo {}` 而非 `typedef struct foo {} foo`
- 文件名使用小写加连字符（C/C++），小写加下划线（Python）
- 注释简洁，不复述代码本身已表达的内容

---

## 命名约定

```text
函数命名：<class>_<method>，method 为 <action>_<noun>
枚举值：全大写，以枚举名作为前缀
不透明类型：使用 _t 后缀
构造/析构：使用 init/free
```

示例：

```cpp
llama_model_init();           // class: "llama_model",         method: "init"
llama_sampler_chain_remove(); // class: "llama_sampler_chain", method: "remove"
llama_adapter_lora_free();    // class: "llama_adapter_lora",  method: "free"
```

---

## 注意事项

- **不接受完全由 AI 生成的 PR**，详见 [AGENTS_CN.md](AGENTS_CN.md)
- 不得代替用户执行 `git push` 或创建 PR
- 大改动需先与用户确认，提醒可能被维护者拒绝
- 添加新量化类型需满足额外标准（困惑度对比、性能数据等）
- 修改服务器代码需参考 [server 开发文档](tools/server/README-dev.md)
- 矩阵乘法约定非标准：`C = ggml_mul_mat(ctx, A, B)` 等价于 $C = B A^T$
