# notes 文件夹说明

个人笔记和参考资料，记录 llama.cpp 项目的配置、编译、运行相关信息。

---

## 文件结构

```text
notes/
├── README.md                             # 本文件，文件夹说明
├── my-commands.md                        # 我常用命令
├── temp.md                               # 临时记录
├── gguf-models-explained.md              # 模型详解（参数、架构、量化说明）
├── output-cmake-configure-explained.md   # 配置输出解释说明
├── output-cmake-build-explained.md       # 编译输出解释说明
├── llama-cpp-running-guide.md            # 运行指南（参数、命令、优化）
├── output-llama-cli-explained.md         # llama-cli 运行输出解释
│
└── outputs/                              # 原始数据文件
    ├── gguf_models_list.txt              # GGUF 模型列表
    ├── output-cmake-configure.txt        # cmake 配置原始输出
    ├── output-cmake-build.txt            # cmake 编译原始输出
    └── output-llama-cli.txt              # llama-cli 运行测试输出
```

---

## 文件说明

### 文档文件（.md）

| 文件 | 说明 |
| --- | --- |
| `gguf-models-explained.md` | 每个模型的详细参数、架构对比、量化类型说明 |
| `output-cmake-configure-explained.md` | cmake 配置输出的逐行解释 |
| `output-cmake-build-explained.md` | cmake 编译输出的阶段说明 |
| `llama-cpp-running-guide.md` | 完整运行指南：工具、参数、命令、优化 |
| `my-commands.md` | 个人常用命令记录 |
| `temp.md` | 临时记录（命令、笔记等） |
| `output-llama-cli-explained.md` | llama-cli 运行输出的逐行解释 |

### 数据文件（outputs/）

| 文件 | 说明 |
| --- | --- |
| `gguf_models_list.txt` | 模型列表、路径、元数据 |
| `output-cmake-configure.txt` | cmake 配置原始输出 |
| `output-cmake-build.txt` | cmake 编译原始输出（约 3.8MB） |
| `output-llama-cli.txt` | llama-cli 运行测试原始输出 |

---

## 更新记录

- **2026-06-26**: 初始创建，包含编译、运行、模型相关信息
