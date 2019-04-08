#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-08 19:01:27
# @Author  : eupho (lid1665072686@gmail.com)
# @Link    : https://github.com/euphol
# @Version : $Id$

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from models import User, Comment, Blog, next_id

@get('/')
async def index(request):
	users = await User.findAll()
	return {
		'__template__': 'test.html',
		'users': users
	}
