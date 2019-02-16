# Fond后端部分

我的第一个全栈练手项目的后端部分。这一块是我边学边做，虽然写的不太好，但是我的收获却很大。

## 项目说明

项目技术栈：Python Flask + sqlalchemy +wtf

项目通过gunicorn+nginx部署在centos

[项目演示](https://52chinaweb.com/v1/user)

[项目地址](https://github.com/ChangJun2019/fond_api)

## 项目功能

- 实现flask resetful API，为前端提供接口
- 通过**flask-httpauth** 实现登录机制
- 实现权限管理机制
- 通过**flask-cors**实现跨域访问
- 通过**flask-sqlalchemy**作为orm映射mysql
- 通过**flask-wtf**作为验证层
- 通过**qiniu**生成七牛token

## 项目待实现

尝试能否改写成**GraphQL**，或者去写一个简单GraphQL项目。

## 项目期间博客总结

- [前后端分离使用七牛云存储](https://blog.52chinaweb.com/frontend/useqiniu.html)

## 总结

通过这个项目学习到了如何去写一个web的后端，但对真正的后端来说自己考虑的方面还有很多不足，但通过这个项目，已经有了很多收获。