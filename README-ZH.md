# 华中科技大学羽毛球场地抢订脚本

## 项目简介
该项目用于自动抢订华中科技大学的羽毛球场地。

## 使用步骤
1. 安装依赖：
   linux用户(以ubuntu为例)直接运行以下命令，

   ```sudo apt update```

   ```sudo apt install tesseract-ocr```

   ```pip install -r requirements.txt```

   windows用户先按照[附注](#附注)操作，随后执行以下命令

   ```pip install -r requirements.txt```

2. 修改```info.toml```配置文件
3. 执行脚本

    ```python main.py```

## 附注
1. 点击 [Tesseract](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe) 进行安装
2. 将Tesseract的路径添加到环境变量中

## court.json填写原理(以光谷体育场为例,主馆羽毛球场为例)
1. 浏览器打开网址https://pecg.hust.edu.cn/cggl/front/syqk?cdbh=45

2. `cdbh`即上述链接中所提(`cdbh:chang di bian hao`)(可恶的英文不好的中文开发者)

3. 右键-查看页面源代码

4. `ctrl+f`,搜索`"pian"`字段,即可发现原理
