# 🦄 大规模分类

> LLM 在从 5、10、甚至 50 个类别中进行分类方面很出色。但当我们有超过 1000 个类别时，该如何处理这种情况？或许是一个不断变化的类别列表？

[视频](https://youtu.be/6B7MzraQMZk)

[![大规模分类](https://img.youtube.com/vi/6B7MzraQMZk/0.jpg)](https://www.youtube.com/watch?v=6B7MzraQMZk)

## 运行此代码

```bash
# 安装依赖
uv sync
```

```bash
# 将 BAML 文件转换为 Python
uv run baml-cli generate
```

```bash
# 运行代码
uv run hello.py
```

## 后续练习 - 从数百个工具中选择工具

如果您想玩弄这段代码并尝试扩展它，可以尝试这个练习。

1. 浏览 [./tools.json](./tools.json) 文件
2. 将工具列表加载为 `Category` 或为 `Tool` 创建类似类
3. 实现 `f(tool) -> string` 用于嵌入文本和 `g(tool) -> string` 用于 LLM 文本
4. 更新代码以嵌入并搜索用户查询，选择最可能的 topk 工具
5. 探索一些用于模糊工具的输入，看看您能得到多高的准确度

如果您想添加更多 MCP 服务器或其他工具，生成 json 的代码在 https://github.com/dexhorthy/thousands-of-tools-mcp

## 后续练习 - 后 LLM 探测

1. 将核心 LLM 提示更改为选择 `Category[]` 而不是单个 `Category`
2. 添加后续步骤（确定性或基于 LLM）来从 `Category[]` 列表中选择最终 `Category`
3. 编写一些示例，其中最终探测可以解决密切重叠的类别
4. 如果您做了工具选择练习，您可以使用 `Tool` 而不是 `Category`

## 图表

![image](https://github.com/user-attachments/assets/233eca5d-07a9-4238-a812-bae538dc7b78)

![image](https://github.com/user-attachments/assets/02b775f1-50a2-424f-934a-14982e5025a4)

![image](https://github.com/user-attachments/assets/abe0e587-360f-4d06-8973-cd91a8e4ea0d)

![image](https://github.com/user-attachments/assets/c13795d4-1ada-40a3-9d11-5912dbd3a787)

![image](https://github.com/user-attachments/assets/3dfa6815-c7b0-46cb-b02c-189e51c016c4)

![image](https://github.com/user-attachments/assets/6cb9c541-ba25-478b-8244-62b4114acb97)
