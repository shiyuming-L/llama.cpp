# 贡献指南

本项目将贡献者分为三个级别：

- **贡献者（Contributor）**：曾经贡献过代码的人（无特殊权限）
- **协作者（Collaborator/Triage）**：有重大贡献的人，可能负责代码的某些部分，需要维护和审查他们负责的代码的贡献
- **维护者（Maintainer）**：负责审查和合并 PR，在获得代码所有者批准后进行

## AI 使用政策

> [!IMPORTANT]
> 本项目**不接受**完全或大部分由 AI 生成的 Pull Request。AI 工具只能作为辅助手段使用。
>
> 多次违反此政策可能导致你的账号被永久禁止参与本项目。
>
> 关于 AI 允许和限制使用的详细信息，请参见 [AGENTS.md](AGENTS.md)。

最初由 AI 生成随后经过编辑的代码，仍被视为 AI 生成的代码。AI 辅助仅在以下情况下允许：代码的主体部分由人类贡献者编写，AI 仅用于修正错误或扩展贡献者已经构思好的详细修改（例如，生成带有细微变化的重复行）。

如果使用了 AI 生成任何代码，贡献者必须遵守以下要求：

1. 明确披露 AI 的使用方式。
2. 在提交 Pull Request 前进行全面的手动审查。
3. 当维护者询问时，能够解释提交的每一行代码。
4. 严禁使用 AI 为你撰写帖子（bug 报告、功能请求、Pull Request 描述、Github 讨论、回复他人等……）。

更多信息请参见 [AGENTS.md](AGENTS.md)。

## Pull Request（贡献者和协作者）

提交 PR 前：

- 搜索已有的 PR，避免重复劳动
- llama.cpp 使用 ggml 张量库进行模型评估。如果你不熟悉 ggml，请考虑查看 [ggml 仓库中的示例](https://github.com/ggml-org/ggml/tree/master/examples/)。[simple](https://github.com/ggml-org/ggml/tree/master/examples/simple) 展示了使用 ggml 的最小示例。[gpt-2](https://github.com/ggml-org/ggml/tree/master/examples/gpt-2) 包含使用 GPT-2 进行语言模型推理的最小实现。[mnist](https://github.com/ggml-org/ggml/tree/master/examples/mnist) 演示了如何训练和评估一个简单的图像分类器
- 测试你的改动：
  - 在发布前在本地[运行完整的 CI](ci/README.md)
  - 验证困惑度和性能没有受到负面影响（使用 `llama-perplexity` 和 `llama-bench`）
  - 如果修改了 `ggml` 源码，运行 `test-backend-ops` 工具检查不同后端实现的 `ggml` 算子是否产生一致的结果（这需要至少两个不同的 `ggml` 后端）
  - 如果修改或新增了 `ggml` 算子，在 `test-backend-ops` 中添加相应的测试用例
- 为每个功能或修复创建单独的 PR：
  - 避免在单个 PR 中合并不相关的改动
  - 对于复杂功能，考虑先开一个功能请求进行讨论和预期对齐
  - 添加新模型或功能支持时，除非有充分理由，初始 PR 只关注 **CPU 支持**。在后续 PR 中添加 CUDA 等其他后端支持
  - 特别是，添加新的数据类型（扩展 `ggml_type` 枚举）会带来不成比例的维护负担。因此，要添加新的量化类型，你至少需要满足以下*额外*标准：
    - 将一个小模型使用新类型转换为 GGUF 并上传到 HuggingFace
    - 提供与 FP16/BF16（无论哪种是原始精度）以及相似大小类型的[困惑度](https://github.com/ggml-org/llama.cpp/tree/master/tools/perplexity)对比
    - 提供新类型与相似大小类型相对于 FP16/BF16（无论哪种是原始精度）版本的 KL 散度数据
    - 提供新类型与相似大小类型在纯 CPU 上的[性能数据](https://github.com/ggml-org/llama.cpp/tree/master/tools/llama-bench)
- 考虑允许对你分支的写入权限以加快审查，因为 reviewer 可以直接推送 commit
- 如果你是新贡献者：
  - 限制你的打开 PR 数量为 1
  - 不要提交微不足道的修复（例如拼写错误、格式更改）

提交 PR 后：

- 期望收到修改请求，以确保代码符合 llama.cpp 的质量和长期可维护性标准
- 维护者在最终决定批准和合并 PR 时，将依赖你的见解和批准
- 如果你的 PR 过期了，将其 rebase 到最新的 `master` 上以引起维护者的注意
- 考虑将自己添加到 [CODEOWNERS](CODEOWNERS) 中，表示你愿意修复相关问题和审查相关 PR

## Pull Request（维护者）

- 使用 squash merge 合并 PR
- 使用以下格式作为 squash 后的 commit 标题：`<module> : <commit title> (#<issue_number>)`。例如：`utils : fix typo in utils.py (#1234)`
- 可从以下位置选择 `<module>`：[Modules](https://github.com/ggml-org/llama.cpp/wiki/Modules)
- 让其他维护者合并他们自己的 PR
- 合并 PR 时，确保你充分理解了这些改动
- 如果 PR 不需要发布新版本，在 squash 的 commit 中添加 `[no release]` 以节省 CI 资源
- 注意维护负担：功能的大部分工作发生在 PR 合并之后。如果 PR 作者没有承诺长期贡献，其他人需要承担责任（你）

维护者保留以下情况下拒绝审查或关闭 Pull Request 的权利，无需任何解释：

- 提议的改动已在路线图或现有 issue 中提到，且已分配给他人
- Pull Request 与已有的重复
- 贡献者未遵守本贡献指南或 AI 政策

## 编码规范

- 避免添加第三方依赖、额外文件、额外头文件等
- 始终考虑与其他操作系统和架构的跨平台兼容性
- 避免花哨的现代 STL 语法，使用基本的 `for` 循环，避免模板，保持简单
- 垂直对齐使代码更易读且更便于批量编辑
- 清理所有尾随空格，使用 4 个空格缩进，大括号在同一行，`void * ptr`，`int & a`
- 在公共 API 中使用有大小的整数类型（如 `int32_t`），`size_t` 也可用于分配大小或字节偏移
- 使用 `struct foo {}` 声明结构体，而非 `typedef struct foo {} foo`
  - 在 C++ 代码中，当不需要时省略可选的 `struct` 和 `enum` 关键字

    ```cpp
    // OK
    llama_context * ctx;
    const llama_rope_type rope_type;

    // 不 OK
    struct llama_context * ctx;
    const enum llama_rope_type rope_type;
    ```

    *（注意：此规范尚未应用到 llama.cpp 代码库。新代码应遵循此规范。）*

- 尽量遵循代码中的现有模式（缩进、空格等）。如有疑问，使用 `clang-format`（来自 clang-tools v15+）格式化添加的代码
- 对于本规范未涵盖的内容，请参考 [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- 张量以行优先顺序存储数据。我们将维度 0 称为列，1 称为行，2 称为矩阵
- 矩阵乘法约定非标准：[`C = ggml_mul_mat(ctx, A, B)`](https://github.com/ggml-org/llama.cpp/blob/880e352277fc017df4d5794f0c21c44e1eae2b84/ggml.h#L1058-L1064) 意味着 $C^T = A B^T \Leftrightarrow C = B A^T$

![matmul](media/matmul.png)

## 命名规范

- 函数、变量和类型名使用 `snake_case`
- 命名通常优化最长公共前缀（参见[讨论](https://github.com/ggml-org/ggml/pull/302#discussion_r1243240963)）

    ```cpp
    // 不 OK
    int small_number;
    int big_number;

    // OK
    int number_small;
    int number_big;
    ```

- 枚举值始终使用大写，并以枚举名作为前缀

    ```cpp
    enum llama_vocab_type {
        LLAMA_VOCAB_TYPE_NONE = 0,
        LLAMA_VOCAB_TYPE_SPM  = 1,
        LLAMA_VOCAB_TYPE_BPE  = 2,
        LLAMA_VOCAB_TYPE_WPM  = 3,
        LLAMA_VOCAB_TYPE_UGM  = 4,
        LLAMA_VOCAB_TYPE_RWKV = 5,
    };
    ```

- 通用命名模式为 `<class>_<method>`，其中 `<method>` 为 `<action>_<noun>`

    ```cpp
    llama_model_init();           // class: "llama_model",         method: "init"
    llama_sampler_chain_remove(); // class: "llama_sampler_chain", method: "remove"
    llama_sampler_get_seed();     // class: "llama_sampler",       method: "get_seed"
    llama_set_embeddings();       // class: "llama_context",       method: "set_embeddings"
    llama_n_threads();            // class: "llama_context",       method: "n_threads"
    llama_adapter_lora_free();    // class: "llama_adapter_lora",  method: "free"
    ```

  - `get` `<action>` 可以省略
  - 如果不需要，`<noun>` 可以省略
  - `<class>` 的 `_context` 后缀是可选的。仅在需要时使用它来消除符号歧义
  - 构造/析构 `<action>` 使用 `init`/`free`

- 当类型对用户应该是不透明的时，使用 `_t` 后缀——用户不需要知道它是结构体还是其他什么

    ```cpp
    typedef struct llama_context * llama_context_t;

    enum llama_pooling_type llama_pooling_type(const llama_context_t ctx);
    ```

    *（注意：此规范尚未应用到 llama.cpp 代码库。新代码应遵循此规范。）*

- C/C++ 文件名全部小写加连字符。头文件使用 `.h` 扩展名。源文件使用 `.c` 或 `.cpp` 扩展名
- Python 文件名全部小写加下划线

- *（待补充：缩写使用规范）*

## 预处理指令

- *（待补充：添加带示例的规范并应用到代码库）*

    ```cpp
    #ifdef FOO
    #endif // FOO
    ```

## 代码维护

- 现有代码应在 [CODEOWNERS](CODEOWNERS) 文件中指定协作者和/或维护者，负责：
  - 审查和合并相关 PR
  - 修复相关 bug
  - 提供开发者指导/支持

- 添加或修改大块代码时：
  - 如果你是协作者，确保将自己添加到 [CODEOWNERS](CODEOWNERS) 中，表示你愿意审查相关 PR
  - 如果你是贡献者，找一个愿意长期审查和维护你代码的现有协作者
  - 提供必要的 CI 工作流（和硬件）来测试你的改动（参见 [ci/README.md](https://github.com/ggml-org/llama.cpp/tree/master/ci)）

- 新代码应遵循本文档中概述的规范（编码、命名等）。在与 `ggml` 接口不直接交互的、隔离的、特定后端的代码中，允许例外
  *（注意：由于历史原因，现有代码不强制要求遵循此规范）*

- 对于服务器的改动，请务必参考 [server 开发文档](./tools/server/README-dev.md)

## 文档

- 文档是社区协作的成果
- 当你需要查看源代码以了解如何使用 API 时，考虑在头文件中添加简短摘要供日后参考
- 当你发现不正确或过时的文档时，请更新它

## 资源

GitHub 的 issue、PR 和讨论包含大量有助于熟悉代码库的信息。为方便起见，一些更重要的信息从 GitHub 项目中引用：

[llama.cpp 项目](https://github.com/ggml-org/llama.cpp/projects)
