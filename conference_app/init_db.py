import asyncio
import asyncpg

async def create_db_pool():
    return await asyncpg.create_pool(user='postgres', password='postgres', database='conference_app', host='db')

async def wait_for_db(pool):
    for _ in range(5):  # Ожидание 5 раз с интервалом в 1 секунду
        try:
            async with pool.acquire() as connection:
                await connection.execute('SELECT 1')
                return
        except Exception:
            await asyncio.sleep(1)

async def init_db():
    pool = await create_db_pool()
    await wait_for_db(pool)  # Ожидаем доступности базы данных

    async with pool.acquire() as connection:
        # Создание таблицы пользователей
        try:
            await connection.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(128) NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
        except Exception as e:
            print(f"Error creating table: {e}")

        # Создание индекса для оптимизации поиска по username
        try:
            await connection.execute('''
                CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
            ''')
        except Exception as e:
            print(f"Error creating index: {e}")

        # Заполнение тестовыми данными
        try:
            await connection.execute('''
                INSERT INTO users (username, password_hash) VALUES
                ('admin', '$2b$12$KIX9H3uFCwbE/5zCRgH8lO5nS1ybQhK9LVW8UuC8eb1IwdS9hKk4G') -- password: secret
                ON CONFLICT (username) DO NOTHING;  -- Чтобы не вставлять дубликаты
            ''')
        except Exception as e:
            print(f"Error inserting data: {e}")

    await pool.close()

if __name__ == '__main__':
    asyncio.run(init_db())




