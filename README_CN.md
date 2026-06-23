<!-- markdownlint-disable MD033 -->
# llama.cpp

![llama](https://raw.githubusercontent.com/ggml-org/llama.brand/refs/heads/master/cover/llama-cpp/cover-llama-cpp-dark.svg)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/github/v/release/ggml-org/llama.cpp)](https://github.com/ggml-org/llama.cpp/releases)
[![Server](https://github.com/ggml-org/llama.cpp/actions/workflows/server.yml/badge.svg)](https://github.com/ggml-org/llama.cpp/actions/workflows/server.yml)
[![Docker](https://github.com/ggml-org/llama.cpp/actions/workflows/docker.yml/badge.svg)](https://github.com/ggml-org/llama.cpp/actions/workflows/docker.yml)
[![Winget](https://github.com/ggml-org/llama.cpp/actions/workflows/winget.yml/badge.svg)](https://github.com/ggml-org/llama.cpp/actions/workflows/winget.yml)

[宣言](https://github.com/ggml-org/llama.cpp/discussions/205) / [ggml](https://github.com/ggml-org/ggml) / [ops](https://github.com/ggml-org/llama.cpp/blob/master/docs/ops.md)

使用 C/C++ 实现的大语言模型推理

## 最近的 API 变更

- [`libllama` API 变更日志](https://github.com/ggml-org/llama.cpp/issues/9289)
- [`llama-server` REST API 变更日志](https://github.com/ggml-org/llama.cpp/issues/9291)

## 热门话题

- **Hugging Face 缓存迁移：使用 `-hf` 下载的模型现在存储在标准 Hugging Face 缓存目录中，可与其他 HF 工具共享。**
- **[指南：使用 llama.cpp 的新 WebUI](https://github.com/ggml-org/llama.cpp/discussions/16938)**
- [指南：在 llama.cpp 中运行 gpt-oss](https://github.com/ggml-org/llama.cpp/discussions/15396)
- [[反馈] 为 llama.cpp 提供更好的打包以支持下游消费者 🤗](https://github.com/ggml-org/llama.cpp/discussions/15313)
- 已添加对原生 MXFP4 格式的 `gpt-oss` 模型的支持 | [PR](https://github.com/ggml-org/llama.cpp/pull/15091) | [与 NVIDIA 合作](https://blogs.nvidia.com/blog/rtx-ai-garage-openai-oss) | [评论](https://github.com/ggml-org/llama.cpp/discussions/15095)
- `llama-server` 已支持多模态：[#12898](https://github.com/ggml-org/llama.cpp/pull/12898) | [文档](./docs/multimodal.md)
- VS Code 扩展，用于 FIM 补全：[llama.vscode](https://github.com/ggml-org/llama.vscode)
- Vim/Neovim 插件，用于 FIM 补全：[llama.vim](https://github.com/ggml-org/llama.vim)
- Hugging Face Inference Endpoints 现已原生支持 GGUF！[讨论](https://github.com/ggml-org/llama.cpp/discussions/9669)
- Hugging Face GGUF 编辑器：[讨论](https://github.com/ggml-org/llama.cpp/discussions/9268) | [工具](https://huggingface.co/spaces/CISCai/gguf-editor)
- WebGPU 支持已在浏览器中可用，查看[博客/演示](https://reeselevine.github.io/llamas-on-the-web/)了解更多。

----

## 快速开始

使用 llama.cpp 非常简单。以下是在你的机器上安装它的几种方式：

- 使用 [brew、nix、winget 或 conda-forge](docs/install.md) 安装 `llama.cpp`
- 使用 Docker 运行 - 参见 [Docker 文档](docs/docker.md)
- 从[发布页面](https://github.com/ggml-org/llama.cpp/releases)下载预编译的二进制文件
- 通过克隆此仓库从源码构建 - 参见[构建指南](docs/build.md)

安装完成后，你需要一个模型来使用。前往[获取和量化模型](#获取和量化模型)部分了解更多。

示例命令：

```sh
# 使用本地模型文件
llama-cli -m my_model.gguf

# 或者直接从 Hugging Face 下载并运行模型
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF

# 启动兼容 OpenAI 的 API 服务器
llama-server -hf ggml-org/gemma-3-1b-it-GGUF
```

## 项目简介

`llama.cpp` 的主要目标是以最少的设置，在各种硬件上实现最先进的 LLM 推理性能——无论是在本地还是在云端。

- 纯 C/C++ 实现，无任何外部依赖
- Apple 芯片是一等公民——通过 ARM NEON、Accelerate 和 Metal 框架进行优化
- x86 架构支持 AVX、AVX2、AVX512 和 AMX
- RISC-V 架构支持 RVV、ZVFH、ZFH、ZICBOP 和 ZIHINTPAUSE
- 支持 1.5-bit、2-bit、3-bit、4-bit、5-bit、6-bit 和 8-bit 整数量化，实现更快推理和更低内存占用
- 自定义 CUDA 内核，用于在 NVIDIA GPU 上运行 LLM（通过 HIP 支持 AMD GPU，通过 MUSA 支持摩尔线程 GPU）
- 支持 Vulkan 和 SYCL 后端
- CPU+GPU 混合推理，可部分加速超过显存总容量的模型

`llama.cpp` 项目是开发 [ggml](https://github.com/ggml-org/ggml) 库新功能的主要试验场。

<details>
<summary>支持的模型</summary>

通常以下基础模型的微调版本也被支持。

添加新模型支持的说明：[HOWTO-add-model.md](docs/development/HOWTO-add-model.md)

### 纯文本模型

- [X] LLaMA 🦙
- [x] LLaMA 2 🦙🦙
- [x] LLaMA 3 🦙🦙🦙
- [X] [Mistral 7B](https://huggingface.co/mistralai/Mistral-7B-v0.1)
- [x] [Mixtral MoE](https://huggingface.co/models?search=mistral-ai/Mixtral)
- [x] [DBRX](https://huggingface.co/databricks/dbrx-instruct)
- [x] [Jamba](https://huggingface.co/ai21labs)
- [X] [Falcon](https://huggingface.co/models?search=tiiuae/falcon)
- [X] [Chinese LLaMA / Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) 和 [Chinese LLaMA-2 / Alpaca-2](https://github.com/ymcui/Chinese-LLaMA-Alpaca-2)
- [X] [Vigogne (法语)](https://github.com/bofenghuang/vigogne)
- [X] [BERT](https://github.com/ggml-org/llama.cpp/pull/5423)
- [X] [Koala](https://bair.berkeley.edu/blog/2023/04/03/koala/)
- [X] [Baichuan 1 & 2](https://huggingface.co/models?search=baichuan-inc/Baichuan) + [衍生版本](https://huggingface.co/hiyouga/baichuan-7b-sft)
- [X] [Aquila 1 & 2](https://huggingface.co/models?search=BAAI/Aquila)
- [X] [Starcoder 模型](https://github.com/ggml-org/llama.cpp/pull/3187)
- [X] [Refact](https://huggingface.co/smallcloudai/Refact-1_6B-fim)
- [X] [MPT](https://github.com/ggml-org/llama.cpp/pull/3417)
- [X] [Bloom](https://github.com/ggml-org/llama.cpp/pull/3553)
- [x] [Yi 模型](https://huggingface.co/models?search=01-ai/Yi)
- [X] [StableLM 模型](https://huggingface.co/stabilityai)
- [x] [Deepseek 模型](https://huggingface.co/models?search=deepseek-ai/deepseek)
- [x] [Qwen 模型](https://huggingface.co/models?search=Qwen/Qwen)
- [x] [PLaMo-13B](https://github.com/ggml-org/llama.cpp/pull/3557)
- [x] [Phi 模型](https://huggingface.co/models?search=microsoft/phi)
- [x] [PhiMoE](https://github.com/ggml-org/llama.cpp/pull/11003)
- [x] [GPT-2](https://huggingface.co/gpt2)
- [x] [Orion 14B](https://github.com/ggml-org/llama.cpp/pull/5118)
- [x] [InternLM2](https://huggingface.co/models?search=internlm2)
- [x] [CodeShell](https://github.com/WisdomShell/codeshell)
- [x] [Gemma](https://ai.google.dev/gemma)
- [x] [Mamba](https://github.com/state-spaces/mamba)
- [x] [Grok-1](https://huggingface.co/keyfan/grok-1-hf)
- [x] [Xverse](https://huggingface.co/models?search=xverse)
- [x] [Command-R 模型](https://huggingface.co/models?search=CohereForAI/c4ai-command-r)
- [x] [SEA-LION](https://huggingface.co/models?search=sea-lion)
- [x] [GritLM-7B](https://huggingface.co/GritLM/GritLM-7B) + [GritLM-8x7B](https://huggingface.co/GritLM/GritLM-8x7B)
- [x] [OLMo](https://allenai.org/olmo)
- [x] [OLMo 2](https://allenai.org/olmo)
- [x] [OLMoE](https://huggingface.co/allenai/OLMoE-1B-7B-0924)
- [x] [Granite 模型](https://huggingface.co/collections/ibm-granite/granite-code-models-6624c5cec322e4c148c8b330)
- [x] [GPT-NeoX](https://github.com/EleutherAI/gpt-neox) + [Pythia](https://github.com/EleutherAI/pythia)
- [x] [Snowflake-Arctic MoE](https://huggingface.co/collections/Snowflake/arctic-66290090abe542894a5ac520)
- [x] [Smaug](https://huggingface.co/models?search=Smaug)
- [x] [Poro 34B](https://huggingface.co/LumiOpen/Poro-34B)
- [x] [Bitnet b1.58 模型](https://huggingface.co/1bitLLM)
- [x] [Flan T5](https://huggingface.co/models?search=flan-t5)
- [x] [Open Elm 模型](https://huggingface.co/collections/apple/openelm-instruct-models-6619ad295d7ae9f868b759ca)
- [x] [ChatGLM3-6b](https://huggingface.co/THUDM/chatglm3-6b) + [ChatGLM4-9b](https://huggingface.co/THUDM/glm-4-9b) + [GLMEdge-1.5b](https://huggingface.co/THUDM/glm-edge-1.5b-chat) + [GLMEdge-4b](https://huggingface.co/THUDM/glm-edge-4b-chat)
- [x] [GLM-4-0414](https://huggingface.co/collections/THUDM/glm-4-0414-67f3cbcb34dd9d252707cb2e)
- [x] [SmolLM](https://huggingface.co/collections/HuggingFaceTB/smollm-6695016cad7167254ce15966)
- [x] [EXAONE-3.0-7.8B-Instruct](https://huggingface.co/LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct)
- [x] [FalconMamba 模型](https://huggingface.co/collections/tiiuae/falconmamba-7b-66b9a580324dd1598b0f6d4a)
- [x] [Jais](https://huggingface.co/inceptionai/jais-13b-chat)
- [x] [Bielik-11B-v2.3](https://huggingface.co/collections/speakleash/bielik-11b-v23-66ee813238d9b526a072408a)
- [x] [RWKV-7](https://huggingface.co/collections/shoumenchougou/rwkv7-gxx-gguf)
- [x] [RWKV-6](https://github.com/BlinkDL/RWKV-LM)
- [x] [QRWKV-6](https://huggingface.co/recursal/QRWKV6-32B-Instruct-Preview-v0.1)
- [x] [GigaChat-20B-A3B](https://huggingface.co/ai-sage/GigaChat-20B-A3B-instruct)
- [X] [Trillion-7B-preview](https://huggingface.co/trillionlabs/Trillion-7B-preview)
- [x] [Ling 模型](https://huggingface.co/collections/inclusionAI/ling-67c51c85b34a7ea0aba94c32)
- [x] [LFM2 模型](https://huggingface.co/collections/LiquidAI/lfm2-686d721927015b2ad73eaa38)
- [x] [Hunyuan 模型](https://huggingface.co/collections/tencent/hunyuan-dense-model-6890632cda26b19119c9c5e7)
- [x] [BailingMoeV2 (Ring/Ling 2.0) 模型](https://huggingface.co/collections/inclusionAI/ling-v2-68bf1dd2fc34c306c1fa6f86)
- [x] [Mellum 模型](https://huggingface.co/JetBrains/models?search=mellum)

#### 多模态模型

- [x] [LLaVA 1.5 模型](https://huggingface.co/collections/liuhaotian/llava-15-653aac15d994e992e2677a7e)、[LLaVA 1.6 模型](https://huggingface.co/collections/liuhaotian/llava-16-65b9e40155f60fd046a5ccf2)
- [x] [BakLLaVA](https://huggingface.co/models?search=SkunkworksAI/Bakllava)
- [x] [Obsidian](https://huggingface.co/NousResearch/Obsidian-3B-V0.5)
- [x] [ShareGPT4V](https://huggingface.co/models?search=Lin-Chen/ShareGPT4V)
- [x] [MobileVLM 1.7B/3B 模型](https://huggingface.co/models?search=mobileVLM)
- [x] [Yi-VL](https://huggingface.co/models?search=Yi-VL)
- [x] [Mini CPM](https://huggingface.co/models?search=MiniCPM)
- [x] [Moondream](https://huggingface.co/vikhyatk/moondream2)
- [x] [Bunny](https://github.com/BAAI-DCAI/Bunny)
- [x] [GLM-EDGE](https://huggingface.co/models?search=glm-edge)
- [x] [Qwen2-VL](https://huggingface.co/collections/Qwen/qwen2-vl-66cee7455501d7126940800d)
- [x] [LFM2-VL](https://huggingface.co/collections/LiquidAI/lfm2-vl-68963bbc84a610f7638d5ffa)

</details>

<details>
<summary>语言绑定</summary>

- Python: [ddh0/easy-llama](https://github.com/ddh0/easy-llama)
- Python: [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- Go: [go-skynet/go-llama.cpp](https://github.com/go-skynet/go-llama.cpp)
- Node.js: [withcatai/node-llama-cpp](https://github.com/withcatai/node-llama-cpp)
- JS/TS（llama.cpp 服务器客户端）: [lgrammel/modelfusion](https://modelfusion.dev/integration/model-provider/llamacpp)
- JS/TS（可编程提示引擎 CLI）: [offline-ai/cli](https://github.com/offline-ai/cli)
- JavaScript/Wasm（支持浏览器）: [tangledgroup/llama-cpp-wasm](https://github.com/tangledgroup/llama-cpp-wasm)
- Typescript/Wasm（更友好的 API，可在 npm 获取）: [ngxson/wllama](https://github.com/ngxson/wllama)
- Ruby: [yoshoku/llama_cpp.rb](https://github.com/yoshoku/llama_cpp.rb)
- Ruby: [docusealco/rllama](https://github.com/docusealco/rllama)
- Rust（更多功能）: [edgenai/llama_cpp-rs](https://github.com/edgenai/llama_cpp-rs)
- Rust（更友好的 API）: [mdrokz/rust-llama.cpp](https://github.com/mdrokz/rust-llama.cpp)
- Rust（更直接的绑定）: [utilityai/llama-cpp-rs](https://github.com/utilityai/llama-cpp-rs)
- Rust（从 crates.io 自动构建）: [ShelbyJenkins/llm_client](https://github.com/ShelbyJenkins/llm_client)
- C#/.NET: [SciSharp/LLamaSharp](https://github.com/SciSharp/LLamaSharp)
- C#/VB.NET（更多功能 - 社区许可证）: [LM-Kit.NET](https://docs.lm-kit.com/lm-kit-net/index.html)
- Scala 3: [donderom/llm4s](https://github.com/donderom/llm4s)
- Clojure: [phronmophobic/llama.clj](https://github.com/phronmophobic/llama.clj)
- React Native: [mybigday/llama.rn](https://github.com/mybigday/llama.rn)
- Java: [kherud/java-llama.cpp](https://github.com/kherud/java-llama.cpp)
- Java: [QuasarByte/llama-cpp-jna](https://github.com/QuasarByte/llama-cpp-jna)
- Zig: [deins/llama.cpp.zig](https://github.com/Deins/llama.cpp.zig)
- Flutter/Dart: [netdur/llama_cpp_dart](https://github.com/netdur/llama_cpp_dart)
- Flutter: [xuegao-tzx/Fllama](https://github.com/xuegao-tzx/Fllama)
- PHP（API 绑定和基于 llama.cpp 构建的功能）: [distantmagic/resonance](https://github.com/distantmagic/resonance) [（更多信息）](https://github.com/ggml-org/llama.cpp/pull/6326)
- Guile Scheme: [guile_llama_cpp](https://savannah.nongnu.org/projects/guile-llama-cpp)
- Swift: [srgtuszy/llama-cpp-swift](https://github.com/srgtuszy/llama-cpp-swift)
- Swift: [ShenghaiWang/SwiftLlama](https://github.com/ShenghaiWang/SwiftLlama)
- Delphi: [Embarcadero/llama-cpp-delphi](https://github.com/Embarcadero/llama-cpp-delphi)
- Go（无需 CGo）: [hybridgroup/yzma](https://github.com/hybridgroup/yzma)
- Android: [llama.android](/examples/llama.android)

</details>

<details>
<summary>用户界面</summary>

*（要在此列出项目，应明确说明其依赖于 `llama.cpp`）*

- [AI Sublime Text 插件](https://github.com/yaroslavyaroslav/OpenAI-sublime-text) (MIT)
- [BonzAI App](https://apps.apple.com/us/app/bonzai-your-local-ai-agent/id6752847988) (专有)
- [cztomsik/ava](https://github.com/cztomsik/ava) (MIT)
- [Dot](https://github.com/alexpinel/Dot) (GPL)
- [eva](https://github.com/ylsdamxssjxxdd/eva) (MIT)
- [iohub/collama](https://github.com/iohub/coLLaMA) (Apache-2.0)
- [janhq/jan](https://github.com/janhq/jan) (AGPL)
- [johnbean393/Sidekick](https://github.com/johnbean393/Sidekick) (MIT)
- [KanTV](https://github.com/zhouwg/kantv?tab=readme-ov-file) (Apache-2.0)
- [KodiBot](https://github.com/firatkiral/kodibot) (GPL)
- [llama.vim](https://github.com/ggml-org/llama.vim) (MIT)
- [LARS](https://github.com/abgulati/LARS) (AGPL)
- [Llama Assistant](https://github.com/vietanhdev/llama-assistant) (GPL)
- [LlamaLib](https://github.com/undreamai/LlamaLib) (Apache-2.0)
- [LLMFarm](https://github.com/guinmoon/LLMFarm?tab=readme-ov-file) (MIT)
- [LLMUnity](https://github.com/undreamai/LLMUnity) (MIT)
- [LMStudio](https://lmstudio.ai/) (专有)
- [LocalAI](https://github.com/mudler/LocalAI) (MIT)
- [LostRuins/koboldcpp](https://github.com/LostRuins/koboldcpp) (AGPL)
- [MindMac](https://mindmac.app) (专有)
- [MindWorkAI/AI-Studio](https://github.com/MindWorkAI/AI-Studio) (FSL-1.1-MIT)
- [Mobile-Artificial-Intelligence/maid](https://github.com/Mobile-Artificial-Intelligence/maid) (MIT)
- [Mozilla-Ocho/llamafile](https://github.com/Mozilla-Ocho/llamafile) (Apache-2.0)
- [nat/openplayground](https://github.com/nat/openplayground) (MIT)
- [nomic-ai/gpt4all](https://github.com/nomic-ai/gpt4all) (MIT)
- [ollama/ollama](https://github.com/ollama/ollama) (MIT)
- [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui) (AGPL)
- [PocketPal AI](https://github.com/a-ghorbani/pocketpal-ai) (MIT)
- [psugihara/FreeChat](https://github.com/psugihara/FreeChat) (MIT)
- [ptsochantaris/emeltal](https://github.com/ptsochantaris/emeltal) (MIT)
- [pythops/tenere](https://github.com/pythops/tenere) (AGPL)
- [ramalama](https://github.com/containers/ramalama) (MIT)
- [semperai/amica](https://github.com/semperai/amica) (MIT)
- [withcatai/catai](https://github.com/withcatai/catai) (MIT)
- [Autopen](https://github.com/blackhole89/autopen) (GPL)

</details>

<details>
<summary>工具</summary>

- [akx/ggify](https://github.com/akx/ggify) – 从 Hugging Face Hub 下载 PyTorch 模型并转换为 GGML
- [akx/ollama-dl](https://github.com/akx/ollama-dl) – 从 Ollama 库下载模型以直接与 llama.cpp 配合使用
- [crashr/gppm](https://github.com/crashr/gppm) – 启动利用 NVIDIA Tesla P40 或 P100 GPU 的 llama.cpp 实例，降低空闲功耗
- [gpustack/gguf-parser](https://github.com/gpustack/gguf-parser-go/tree/main/cmd/gguf-parser) - 检查/审查 GGUF 文件并估算内存使用量
- [Styled Lines](https://marketplace.unity.com/packages/tools/generative-ai/styled-lines-llama-cpp-model-292902)（专有许可证，Unity3d 游戏开发的推理部分异步包装器，提供预构建的移动端和 Web 平台包装器及模型示例）
- [unslothai/unsloth](https://github.com/unslothai/unsloth) – 🦥 将微调和训练的模型导出/保存为 GGUF (Apache-2.0)

</details>

<details>
<summary>基础设施</summary>

- [Paddler](https://github.com/intentee/paddler) - 开源 LLMOps 平台，用于在你自己的基础设施中托管和扩展 AI
- [GPUStack](https://github.com/gpustack/gpustack) - 管理 GPU 集群以运行 LLM
- [llama_cpp_canister](https://github.com/onicai/llama_cpp_canister) - 将 llama.cpp 作为 Internet Computer 上的智能合约，使用 WebAssembly
- [llama-swap](https://github.com/mostlygeek/llama-swap) - 透明代理，为 llama-server 添加自动模型切换功能
- [Kalavai](https://github.com/kalavai-net/kalavai-client) - 众包端到端 LLM 部署，支持任意规模
- [llmaz](https://github.com/InftyAI/llmaz) - ☸️ 在 Kubernetes 上运行大语言模型的简易高级推理平台
- [LLMKube](https://github.com/defilantech/llmkube) - 用于 llama.cpp 的 Kubernetes operator，支持多 GPU 和 Apple Silicon Metal

</details>

<details>
<summary>游戏</summary>

- [Lucy's Labyrinth](https://github.com/MorganRO8/Lucys_Labyrinth) - 一个简单的迷宫游戏，由 AI 模型控制的代理会试图欺骗你。

</details>

## 支持的后端

| 后端 | 目标设备 |
| --- | --- |
| [Metal](docs/build.md#metal-build) | Apple Silicon |
| [BLAS](docs/build.md#blas-build) | 所有设备 |
| [BLIS](docs/backend/BLIS.md) | 所有设备 |
| [SYCL](docs/backend/SYCL.md) | Intel GPU |
| [OpenVINO [开发中]](docs/backend/OPENVINO.md) | Intel CPU、GPU 和 NPU |
| [MUSA](docs/build.md#musa) | 摩尔线程 GPU |
| [CUDA](docs/build.md#cuda) | Nvidia GPU |
| [HIP](docs/build.md#hip) | AMD GPU |
| [ZenDNN](docs/build.md#zendnn) | AMD CPU |
| [Vulkan](docs/build.md#vulkan) | GPU |
| [CANN](docs/build.md#cann) | 昇腾 NPU |
| [OpenCL](docs/backend/OPENCL.md) | Adreno GPU |
| [IBM zDNN](docs/backend/zDNN.md) | IBM Z 和 LinuxONE |
| [WebGPU](docs/build.md#webgpu) | 所有设备 |
| [RPC](https://github.com/ggml-org/llama.cpp/tree/master/tools/rpc) | 所有设备 |
| [Hexagon [开发中]](docs/backend/snapdragon/README.md) | Snapdragon |
| [VirtGPU](docs/backend/VirtGPU.md) | VirtGPU APIR |

## 获取和量化模型

[Hugging Face](https://huggingface.co) 平台托管了大量与 `llama.cpp` 兼容的 [LLM 模型](https://huggingface.co/models?library=gguf&sort=trending)：

- [热门模型](https://huggingface.co/models?library=gguf&sort=trending)
- [LLaMA](https://huggingface.co/models?sort=trending&search=llama+gguf)

你可以手动下载 GGUF 文件，或通过 CLI 参数 `-hf <user>/<model>[:quant]` 直接使用任何来自 [Hugging Face](https://huggingface.co/) 或其他模型托管站点的 `llama.cpp` 兼容模型。例如：

```sh
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
```

默认情况下，CLI 会从 Hugging Face 下载，你可以通过环境变量 `MODEL_ENDPOINT` 切换到其他选项。`MODEL_ENDPOINT` 必须指向兼容 Hugging Face 的 API 端点。

下载模型后，使用 CLI 工具在本地运行——参见下文。

`llama.cpp` 要求模型以 [GGUF](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md) 文件格式存储。其他数据格式的模型可以使用此仓库中的 `convert_*.py` Python 脚本转换为 GGUF。

Hugging Face 平台提供了多种在线工具，用于转换、量化和托管 `llama.cpp` 模型：

- 使用 [GGUF-my-repo 空间](https://huggingface.co/spaces/ggml-org/gguf-my-repo) 将模型转换为 GGUF 格式并将模型权重量化为更小的尺寸
- 使用 [GGUF-my-LoRA 空间](https://huggingface.co/spaces/ggml-org/gguf-my-lora) 将 LoRA 适配器转换为 GGUF 格式（更多信息：[讨论](https://github.com/ggml-org/llama.cpp/discussions/10123)）
- 使用 [GGUF-editor 空间](https://huggingface.co/spaces/CISCai/gguf-editor) 在浏览器中编辑 GGUF 元数据（更多信息：[讨论](https://github.com/ggml-org/llama.cpp/discussions/9268)）
- 使用 [Inference Endpoints](https://ui.endpoints.huggingface.co/) 直接在云端托管 `llama.cpp`（更多信息：[讨论](https://github.com/ggml-org/llama.cpp/discussions/9669)）

要了解更多关于模型量化的信息，请[阅读此文档](tools/quantize/README.md)

## [`llama-cli`](tools/cli)

### 一个用于访问和体验 `llama.cpp` 大部分功能的 CLI 工具

- <details open>
    <summary>在对话模式下运行</summary>

    内置聊天模板的模型将自动激活对话模式。如果未自动激活，你可以通过添加 `-cnv` 并使用 `--chat-template NAME` 指定合适的聊天模板来手动启用

    ```bash
    llama-cli -m model.gguf

    # > hi, who are you?
    # Hi there! I'm your helpful assistant! I'm an AI-powered chatbot designed to assist and provide information to users like you. I'm here to help answer your questions, provide guidance, and offer support on a wide range of topics. I'm a friendly and knowledgeable AI, and I'm always happy to help with anything you need. What's on your mind, and how can I assist you today?
    #
    # > what is 1+1?
    # Easy peasy! The answer to 1+1 is... 2!
    ```

    </details>

- <details>
    <summary>使用自定义聊天模板在对话模式下运行</summary>

    ```bash
    # 使用 "chatml" 模板（使用 -h 查看支持的模板列表）
    llama-cli -m model.gguf -cnv --chat-template chatml

    # 使用自定义模板
    llama-cli -m model.gguf -cnv --in-prefix 'User: ' --reverse-prompt 'User:'
    ```

    </details>

- <details>
    <summary>使用自定义语法约束输出</summary>

    ```bash
    llama-cli -m model.gguf -n 256 --grammar-file grammars/json.gbnf -p 'Request: schedule a call at 8pm; Command:'

    # {"appointmentTime": "8pm", "appointmentDetails": "schedule a a call"}
    ```

    [grammars/](grammars/) 文件夹包含一些示例语法。要编写自己的语法，请查看 [GBNF 指南](grammars/README.md)。

    要编写更复杂的 JSON 语法，请查看 [Intrinsic Labs](https://grammar.intrinsiclabs.ai/)

    </details>

## [`llama-server`](tools/server)

### 一个轻量级的、兼容 [OpenAI API](https://github.com/openai/openai-openapi) 的 HTTP 服务器，用于提供 LLM 服务

- <details open>
    <summary>在端口 8080 上启动默认配置的本地 HTTP 服务器</summary>

    ```bash
    llama-server -m model.gguf --port 8080

    # 基础 Web UI 可通过浏览器访问：http://localhost:8080
    # 聊天补全端点：http://localhost:8080/v1/chat/completions
    ```

    </details>

- <details>
    <summary>支持多用户和并行解码</summary>

    ```bash
    # 最多 4 个并发请求，每个请求最大 4096 上下文
    llama-server -m model.gguf -c 16384 -np 4
    ```

    </details>

- <details>
    <summary>启用投机解码</summary>

    ```bash
    # draft.gguf 模型应该是 target model.gguf 的小型变体
    llama-server -m model.gguf -md draft.gguf
    ```

    </details>

- <details>
    <summary>提供嵌入模型服务</summary>

    ```bash
    # 使用 /embedding 端点
    llama-server -m model.gguf --embedding --pooling cls -ub 8192
    ```

    </details>

- <details>
    <summary>提供重排序模型服务</summary>

    ```bash
    # 使用 /reranking 端点
    llama-server -m model.gguf --reranking
    ```

    </details>

- <details>
    <summary>使用语法约束所有输出</summary>

    ```bash
    # 自定义语法
    llama-server -m model.gguf --grammar-file grammar.gbnf

    # JSON
    llama-server -m model.gguf --grammar-file grammars/json.gbnf
    ```

    </details>

## [`llama-perplexity`](tools/perplexity)

### 一个用于测量模型在给定文本上的[困惑度](tools/perplexity/README.md)[^1]（和其他质量指标）的工具

- <details open>
    <summary>测量文本文件上的困惑度</summary>

    ```bash
    llama-perplexity -m model.gguf -f file.txt

    # [1]15.2701,[2]5.4007,[3]5.3073,[4]6.2965,[5]5.8940,[6]5.6096,[7]5.7942,[8]4.9297, ...
    # Final estimate: PPL = 5.4007 +/- 0.67339
    ```

    </details>

- <details>
    <summary>测量 KL 散度</summary>

    ```bash
    # 待完成
    ```

    </details>

[^1]: [https://huggingface.co/docs/transformers/perplexity](https://huggingface.co/docs/transformers/perplexity)

## [`llama-bench`](tools/llama-bench)

### 针对各种参数对推理性能进行基准测试

- <details open>
    <summary>运行默认基准测试</summary>

    ```bash
    llama-bench -m model.gguf

    # 输出：
    # | model               |       size |     params | backend    | threads |          test |                  t/s |
    # | ------------------- | ---------: | ---------: | ---------- | ------: | ------------: | -------------------: |
    # | qwen2 1.5B Q4_0     | 885.97 MiB |     1.54 B | Metal,BLAS |      16 |         pp512 |      5765.41 ± 20.55 |
    # | qwen2 1.5B Q4_0     | 885.97 MiB |     1.54 B | Metal,BLAS |      16 |         tg128 |        197.71 ± 0.81 |
    #
    # build: 3e0ba0e60 (4229)
    ```

    </details>

## [`llama-simple`](examples/simple)

### 一个使用 `llama.cpp` 实现应用的最小示例，对开发者很有用

- <details>
    <summary>基础文本补全</summary>

    ```bash
    llama-simple -m model.gguf

    # Hello my name is Kaitlyn and I am a 16 year old girl. I am a junior in high school and I am currently taking a class called "The Art of
    ```

    </details>

## 贡献指南

- 贡献者可以提交 PR
- 协作者将根据贡献情况受邀加入
- 维护者可以推送到 `llama.cpp` 仓库的分支并将 PR 合并到 `master` 分支
- 任何帮助管理 issue、PR 和项目的贡献都非常感谢！
- 查看 [good first issues](https://github.com/ggml-org/llama.cpp/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) 了解适合首次贡献的任务
- 阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多信息
- 请务必阅读：[边缘推理](https://github.com/ggml-org/llama.cpp/discussions/205)
- 一些背景故事，供感兴趣的人参考：[Changelog podcast](https://changelog.com/podcast/532)

## 其他文档

- [CLI](tools/cli/README.md)
- [补全](tools/completion/README.md)
- [服务器](tools/server/README.md)
- [GBNF 语法](grammars/README.md)

### 开发文档

- [如何构建](docs/build.md)
- [在 Docker 中运行](docs/docker.md)
- [在 Android 上构建](docs/android.md)
- [多 GPU 使用](docs/multi-gpu.md)
- [性能故障排除](docs/development/token_generation_performance_tips.md)
- [GGML 技巧与窍门](https://github.com/ggml-org/llama.cpp/wiki/GGML-Tips-&-Tricks)

### 关于模型的重要论文和背景资料

如果你的问题是关于模型生成质量的，请至少浏览以下链接和论文，以了解 LLaMA 模型的局限性。这在选择合适的模型大小以及理解 LLaMA 模型与 ChatGPT 之间显著和细微差异时尤为重要：

- LLaMA：
  - [介绍 LLaMA：一个基础的 650 亿参数大语言模型](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/)
  - [LLaMA：开放高效的基础语言模型](https://arxiv.org/abs/2302.13971)
- GPT-3
  - [语言模型是少样本学习者](https://arxiv.org/abs/2005.14165)
- GPT-3.5 / InstructGPT / ChatGPT：
  - [对齐语言模型以遵循指令](https://openai.com/research/instruction-following)
  - [通过人类反馈训练语言模型遵循指令](https://arxiv.org/abs/2203.02155)

## XCFramework

XCFramework 是为 iOS、visionOS、tvOS 和 macOS 预编译的库版本。它可以在 Swift 项目中使用，无需从源码编译库。例如：

```swift
// swift-tools-version: 5.10
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "MyLlamaPackage",
    targets: [
        .executableTarget(
            name: "MyLlamaPackage",
            dependencies: [
                "LlamaFramework"
            ]),
        .binaryTarget(
            name: "LlamaFramework",
            url: "https://github.com/ggml-org/llama.cpp/releases/download/b5046/llama-b5046-xcframework.zip",
            checksum: "c19be78b5f00d8d29a25da41042cb7afa094cbf6280a225abe614b03b20029ab"
        )
    ]
)
```

上面的示例使用的是库的中间构建版本 `b5046`。可以通过更改 URL 和校验和来使用不同的版本。

## 命令行补全

某些环境支持命令行补全。

### Bash 补全

```bash
build/bin/llama-cli --completion-bash > ~/.llama-completion.bash
source ~/.llama-completion.bash
```

可以选择将其添加到 `.bashrc` 或 `.bash_profile` 中以自动加载。例如：

```console
echo "source ~/.llama-completion.bash" >> ~/.bashrc
```

## 依赖项

- [yhirose/cpp-httplib](https://github.com/yhirose/cpp-httplib) - 单头文件 HTTP 服务器，被 `llama-server` 使用 - MIT 许可证
- [stb-image](https://github.com/nothings/stb) - 单头文件图像格式解码器，被多模态子系统使用 - 公共领域
- [nlohmann/json](https://github.com/nlohmann/json) - 单头文件 JSON 库，被各种工具/示例使用 - MIT 许可证
- [miniaudio.h](https://github.com/mackron/miniaudio) - 单头文件音频格式解码器，被多模态子系统使用 - 公共领域
- [subprocess.h](https://github.com/sheredom/subprocess.h) - 单头文件 C/C++ 进程启动解决方案 - 公共领域
