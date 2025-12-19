# AI SDK 项目结构

最后更新: 2025-12-19

## 完整项目结构

```
my_ai_api/
├── ai_sdk/                      # SDK核心代码
│   ├── __init__.py             # 包初始化，导出主要类
│   ├── client.py               # 核心客户端类
│   ├── exceptions.py           # 异常定义
│   ├── _utils.py               # 工具函数
│   ├── resources/              # 资源模块
│   │   ├── __init__.py
│   │   ├── chat.py            # Chat相关API
│   │   └── tasks.py           # 任务管理API
│   └── types/                  # 类型定义
│       ├── __init__.py
│       └── chat.py            # Chat相关类型
│
├── docs/                        # MkDocs文档
│   ├── index.md
│   ├── quickstart.md
│   ├── usage.md
│   ├── api-reference.md
│   ├── image-generation.md
│   └── examples/
│       ├── basic-chat.md
│       ├── image-analysis.md
│       └── advanced-usage.md
│
├── examples/                    # 使用示例（未实现）
│   ├── basic_chat.py
│   ├── image_analysis.py
│   ├── image_generation.py
│   └── advanced_usage.py
│
├── tests/                       # 测试文件（未实现）
│   └── test_chat.py
│
├── .github/                     # GitHub配置
│   └── workflows/
│       └── docs.yml            # 文档自动部署
│
├── .env.example                 # 环境变量模板
├── .gitignore                   # Git忽略规则
├── mkdocs.yml                   # MkDocs配置
├── requirements.txt             # 项目依赖
├── setup.py                     # 安装配置
│
├── README.md                    # 项目README
├── test_results.md              # 测试结果报告
├── test_sdk.py                  # 简单测试脚本
├── API差异分析.md               # API差异分析文档
└── OpenAI协议接口完整文档.md    # API接口文档
```

## 核心文件说明

### SDK核心代码

| 文件 | 说明 |
|------|------|
| `ai_sdk/__init__.py` | 导出主要类：AIClient, ChatMessage, 异常类等 |
| `ai_sdk/client.py` | 核心客户端，处理HTTP请求和认证 |
| `ai_sdk/resources/chat.py` | Chat completions接口实现 |
| `ai_sdk/resources/tasks.py` | 任务查询接口 |
| `ai_sdk/types/chat.py` | Pydantic数据模型 |
| `ai_sdk/exceptions.py` | 自定义异常类 |
| `ai_sdk/_utils.py` | 工具函数 |

### 文档文件

| 文件 | 说明 |
|------|------|
| `README.md` | 项目主文档，快速开始指南 |
| `test_results.md` | 功能测试结果报告 |
| `API差异分析.md` | API文档与实现的差异分析 |
| `OpenAI协议接口完整文档.md` | 完整的API接口文档 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `.env.example` | 环境变量模板 |
| `.gitignore` | Git忽略规则 |
| `mkdocs.yml` | MkDocs文档配置 |
| `requirements.txt` | Python依赖 |
| `setup.py` | 包安装配置 |

## 开发状态

### ✅ 已完成

- SDK核心功能实现
- 生文、生图、理解图功能
- Python 3.8+兼容性
- 完整的文档体系
- GitHub发布（v0.1.1）
- 在线文档部署

### 📋 待完成

- examples/ 示例代码
- tests/ 单元测试
- CI/CD测试流程
- 更多高级功能

## 文档链接

- 在线文档: https://randbear.github.io/ai-sdk/
- GitHub仓库: https://github.com/randbear/ai-sdk
- 测试结果: [test_results.md](./test_results.md)
