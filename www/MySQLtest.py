import asyncio
import orm
from model import User  # 假设你的模型类定义在 model.py 文件中

async def test():
    try:
        # 创建事件循环对象
        loop = asyncio.get_event_loop()

        # 替换为你的数据库信息
        db_params = dict(
            host='localhost',
            port=3306,
            user='root',
            password='1234',
            db='awesome'
        )

        # 创建数据库连接池
        await orm.create_pool(loop, **db_params)

        # 创建一个用户对象
        user = User(name='Test1', email='test1@example.com', passwd='0000000', image='about:pink')

        # 保存用户对象到数据库
        await user.save()

        # 查询所有用户
        users = await User.findAll()

        # 输出查询结果
        for u in users:
            print(u)

    except Exception as e:
        print(f"An error occurred: {e}")

# 在事件循环中运行测试函数
loop = asyncio.get_event_loop()
loop.run_until_complete(test())
