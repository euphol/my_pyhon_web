#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-07 15:44:20
# @Author  : eupho (lid1665072686@gmail.com)
# @Link    : https://github.com/euphol
# @Version : $Id$


class APIError(Exception):
	'''
	the base APIError which contains error(required), data(optional) and message(optional)
	'''
	def __init__(self, error, data='', message=''):
		super(APIError,self).__init__(message)
		self.error = error
		self.data = data
		self.message = message

class APIValueError(APIError):
	"""indicate the input value has error or invalid. the data specifies the error of input form"""
	def __init__(self, field, message=''):
		super(APIValueError, self).__init__('value: invalid', field, message)

class APIResourceNotFoundError(APIError):
	"""Indicate the resource was not found. The data specifies the resource name"""
	def __init__(self, field, message=''):
		super(APIResourceNotFoundError, self).__init__('value: notfound', field, message)

class APIPermissionError(APIError):
	"""docstring for APIPermissionError"""
	def __init__(self, message=''):
		super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)
		
		
		