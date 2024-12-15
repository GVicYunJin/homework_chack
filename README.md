数字化作业统计平台

项目背景

在教育教学过程中，作业收交与统计一直是困扰教师的难题，耗费大量时间精力且效率低下。为改善这一状况，我们开发了数字化作业统计平台。

功能概述

便捷的作业管理流程

• 学生在作业册侧面贴条形码，老师拍照上传，系统自动识别未交作业学生，简化检查流程，提高效率。

灵活的班级管理

• 支持班级注册与注销，适应分班或学生变动情况，未来计划拓展多班级管理及教师独立账号功能。

技术实现

基于Flask框架的Web应用

• 运用Flask构建后端，实现数据存储、处理与页面交互，确保平台稳定运行。

条形码技术应用

• 借助条形码实现学生作业精准识别与统计，提升作业管理准确性。

Docker容器化部署

• 采用Docker进行部署，便于环境配置与管理，确保平台在不同环境稳定运行。

私有化部署

提供私有化部署方案，用户可将平台部署在自有服务器，保障数据安全与隐私，具体步骤如下：

1. 以ubuntu22.04 live为例（默认有docker环境），使用finalshell或其他ssh工具连接服务器。

2. 上传【homework - ckack】文件夹到服务器任意位置，非root用户需授予777权限。

3. 获取根用户权限：su root。

4. 进入上传文件根目录，确保能看到dockerfile。

5. 构建docker容器：docker build -t homework - checker. （约需3 - 10分钟）。

6. 启动docker容器：docker run -d -p 44441:44441 --name homework - checker homework - checker。

7. 在安全组/防火墙放行44441端口。

8. 通过http://{服务器ip}:44441访问应用程序，若无公网可进行内网穿透。

未来规划

增强功能

• 实现多班级、多教师账号管理，方便教学工作。

• 优化登录验证，采用token技术提升用户体验。

数据统计与分析

• 提供详细作业完成情况统计，支持图表展示，助力教学决策。

数据安全提升

• 增加数据冗余与灾备，保障数据安全与平台稳定运行。

团队信息

• 团队成员：郭子路、龚毅夫

• 指导老师：薛仙

• 学校：西安市第六十六中学

致谢

感谢团队成员努力、指导老师帮助，以及CSDN、菜鸟编程等网络资源和相关库作者的支持。
