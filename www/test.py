import orm
from models import User, Blog, Comment
import asyncio

async def test(loop):
	global __pool
	if '__pool' not in dir():
		await orm.create_pool(loop=loop, user='root', password='962452648', database='webapp')

	#u = User(name='test', email='test@example.com', passwd='123', image='blank')
	print(User.__select__)
	u = await User.findAll(where='`name`=?', args='test')
	print(type(u))
	await u[0].remove()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()