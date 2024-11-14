from setuptools import setup, find_packages

setup(
    name='my_3d_toolpackage',  # 您的包名称
    version='0.1.0',            # 版本号
    description='A toolkit for 3D processing and manipulation in Python',  # 简要描述
    long_description=open('README.md').read(),  # 长描述，通常是 README.md 中的内容
    long_description_content_type='text/markdown',  # 长描述内容类型
    author='Haitao Xu',         # 您的姓名
    author_email='your_email@example.com',  # 联系邮箱
    url='https://github.com/yourusername/my_3d_toolpackage',  # 项目主页（如 GitHub）
    license='MIT',              # 许可证类型
    packages=find_packages(),   # 自动找到包含 `__init__.py` 的所有子包
    install_requires=[
        'numpy',
        'bpy',                 # 如果您的库有依赖的第三方库，可以在这里列出
        # 添加其他必要的库
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',    # 需要的 Python 版本
)

