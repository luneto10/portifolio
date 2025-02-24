from prisma import Prisma

prisma = Prisma()


async def connect():
    await prisma.connect()


async def disconnect():
    await prisma.disconnect()


def get_prisma():
    return prisma
