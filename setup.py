from setuptools import setup, find_packages



setup(
    name='my_3d_toolpackage',
    version='0.1.0',        
    description='A toolkit for 3D processing and manipulation in Python', 
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown', 
    author='Haitao Xu',  
    author_email='1271449616@qq.com@example.com', 
    url='https://github.com/yourusername/my_3d_toolpackage',
    license='MIT',  
    packages=find_packages(), 
    install_requires=[
        'bpy: 3.6.0',
        'urchin: 0.0.29',
        'urdfpy: 0.0.22',
        'numpy: 1.23.5',
        'networkx: 2.2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

