#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-07 14:01:49
# @Author  : eupho (lid1665072686@gmail.com)
# @Link    : https://github.com/euphol
# @Version : $Id$

import asyncio, os, inspect, functools, logging

from aiohttp import web

from apis import APIError

# 定义装饰器，将一个函数映射为URL处理函数
# 使用工厂模式生成装饰器
def request(path, method):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(**args, **kw)
		wrapper.__method__ = method
		wrapper.__route__ = path
		return wrapper
	return decorator

get = functools.partial(request, method='GET')
post = functools.partial(request, method='POST')

# RequestHandler的作用是从URL函数中分析其所需要的参数，从request中获取接收到的参数
# 用RequestHandler将URL函数封装为一个coroutine，确定参数后进行调用，实现response
# 用URL函数初始化一个RequestHandler实例，由于有__call__，该实例可以作为一个函数接受request
# 从request中提取所需要的参数，利用封装好的URL函数完成request的处理和response
def RequestHandler(object):

	def __init__(self, func):
		self._func = asyncio.coroutine(func) # 将URL函数封装为coroutine

	async def __call__(self, request): # __call__可以让类的实例有函数的功能，此处可处理request
		# 分析URL函数所需要的参数
		required_args = inspect.signature(self._func).parameters
		logging.info('required args: %s' % required_args)

		# 判断request中的参数是否是URL函数所需要的，是则提取出来
		kw = {arg: value for arg, value in request.__data__.items() if arg in required_args}

		# 提取match_info参数
		kw.update(request.match_info)

		# 如果URL函数需要request参数的话也添加进来
		if 'request' in required_args:
			kw['request'] = request

		# 检查参数的合理性，并且检查有没有参数缺失
		for key, arg in required_args.items():
			# request参数不应该为可变长参数
			if key == 'request' and arg.kind in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
				return web.HTTPBadRequest(text='request paramter cannot be the var argument')
			if arg.kind not in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
				# 一定要接收到没有缺省值的非变长参数
				if arg.default == arg.empty and arg.name not in kw:
					return web.HTTPBadRequest(text='Missing argument: %s' % arg.name)

		logging.info('call with args: %s' % kw)
		try:
			return await self._func(**kw) # 将分析完毕的参数列表传入封装后的URL函数完成request的处理与response
		except APIError as e:
			return dict(error=e.error, data=e.data, message=e.message)

# 在路由中添加一个模块中所有的URL处理函数
def add_routes(app, module_name):
	try:
		mod = __import__(module_name, fromlist=['get_submodule']) # 导入模块
	except ImportError as e:
		raise e
	for attr in dir(mod): # 从模块的属性列表中寻找所需函数
		if attr.startswith('_'): # 排除以'_'开头的属性
			continue
		func = getattr(mod, attr) # 获取属性内容
		if callable(func) and hasattr(func, '__method__') and hasattr('__route__'): # 判断是否为URL处理函数
			args = ', '.join(inspect.signature(func).parameters.keys())
			logging.info('add route %s %s => %s(%s)' % (func.__method__, func.__route__, func.__name__, args))
			app.router.add_routes(func.__method__, func.__route__, RequestHandler(func)) # 生成RequestHandler实例，添加到路由中

def add_static(app):
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
	app.router.add_static('/static/', path)
	logging.info('add static %s => %s' % ('/static/', path))
