# 广东省二手房数据可视化平台

基于Django的广东省二手房数据可视化平台，集成多种图表展示房价分析、区域对比、市场趋势等功能。

## 功能特性

- 🏠 房源数据管理和展示
- 📊 多维度数据可视化
  - 城市房源数量柱状图
  - 价格区间分布饼图
  - 房型分布统计
  - 朝向分布分析
  - 面积与价格散点图
  - 3D散点图展示
  - 各城市平均价格趋势
  - 区域房价箱线图
  - 城市综合指标雷达图
- 👤 用户认证系统
- 🔍 房源搜索和筛选
- 📱 响应式设计

## 技术栈

- **后端**: Django 4.x
- **数据库**: SQLite
- **可视化**: Pyecharts, Plotly
- **前端**: HTML, CSS, JavaScript
- **数据处理**: Pandas

## 项目结构

```
├── house_html/          # Django应用
│   ├── models.py        # 数据模型
│   ├── views.py         # 视图逻辑
│   ├── templates/       # HTML模板
│   └── static/          # 静态文件
├── data/                # 数据文件
├── txt/                 # Django项目配置
└── manage.py            # Django管理脚本
```

## 安装和运行

1. 克隆项目
```bash
git clone https://github.com/dadaguaijj/-.git
cd -
```

2. 安装依赖
```bash
pip install django pandas pyecharts plotly
```

3. 运行迁移
```bash
python manage.py migrate
```

4. 启动服务器
```bash
python manage.py runserver
```

5. 访问应用
打开浏览器访问 `http://localhost:8000`

## 数据说明

项目包含广东省主要城市的二手房数据：
- 广州、深圳、佛山、东莞
- 中山、珠海、惠州、江门
- 清远、湛江等

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 许可证

MIT License