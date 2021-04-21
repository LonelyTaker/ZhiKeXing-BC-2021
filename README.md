# **知客行轨道交通智慧客流预测平台**
<hr>
##About
本项目是基于回归模型的轨道交通智慧客流预测平台。  
提供客流实况、客流预测、数据分析三大功能模块。  

##目录结构
	├─front-end				// 前端项目文件
	|	├─build				// 项目相关配置
	|	├─config			// 项目相关配置
	|	├─static			// 静态资源目录
	|	├─dist				// 打包后目录
	|	├─src				
	|	|	├─assets		// 字体图片资源
	|	|	├─components	// 组件目录
	|	|	├─lib			// 外部引入包
	|	|	├─router		// vue-router配置
	|	|	├─App.vue		// 根组件
	|	|	├─main.js		// 项目入口文件
	|	├─index.html		// 项目入口文件
	|	├─package.json		// 项目配置文件
	|	├─package-lock.json
	|	├─.babelrc
	|	├─.editorconfig
	|	├─.eslintignore
	|	├─.eslintrc.js
	|	├─.postcssrc.js
	|	└─.prettierrc
	├─WebApi				// 接口项目文件
	├─prediction-model		// 预测模型
	|	├─dailyForecast.py	// 日客流预测模型
	|	├─hourlyForecast.py	// 小时客流预测模型
	|	└─cntPflow.py		// 客流量统计
	├─database				
	|	└─zhikexing.sql		// 数据库文件
	├─接口文档.docx			 // 接口文档
	└─README.md				// 说明文件

##本地运行步骤
1.运行接口项目  
2.前端项目安装依赖  
> npm i  

3.运行前端项目  
> npm run dev

4.前端项目打包
> npm run build