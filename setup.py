"""
AI SDK 安装配置文件
"""
from setuptools import setup, find_packages
import os


def read_file(filename):
    """读取文件内容"""
    with open(
        os.path.join(os.path.dirname(__file__), filename), encoding="utf-8"
    ) as f:
        return f.read()


# 读取README作为长描述
long_description = read_file("README.md")

# 读取requirements
requirements = [
    line.strip()
    for line in read_file("requirements.txt").splitlines()
    if line.strip() and not line.startswith("#")
]

setup(
    name="ai-sdk",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="兼容OpenAI SDK的AI API客户端，支持元宝和Gemini模型",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/ai-sdk",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords="ai api sdk openai yuanbao gemini chat completion",
    project_urls={
        "Bug Reports": "https://github.com/your-username/ai-sdk/issues",
        "Source": "https://github.com/your-username/ai-sdk",
        "Documentation": "https://github.com/your-username/ai-sdk#readme",
    },
)
