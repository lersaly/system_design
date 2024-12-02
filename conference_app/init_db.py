import asyncio
import asyncpg

async def create_db_pool():
    return await asyncpg.create_pool(user='postgres', password='postgres', database='conference_app', host='db')

async def init_db():
    await asyncio.sleep(5)  # Задержка перед подключением к базе данных
    pool = await create_db_pool()

    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,  -- Поле username остается
                password_hash VARCHAR(128) NOT NULL,  -- Поле для хэшированного пароля
                created_at TIMESTAMP DEFAULT NOW()
            );
        ''')

        # Создание таблицы конференций с UNIQUE ограничением для 'title'
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS conferences (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) UNIQUE NOT NULL,  -- Поле 'title' используется вместо 'name'
                description TEXT,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT NOW()
            );
        ''')

        # Создание таблицы докладов с UNIQUE ограничением для 'title'
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS talks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) UNIQUE NOT NULL,  -- Добавлено UNIQUE ограничение
                description TEXT,
                speaker_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        ''')

        # Создание таблицы для связывания докладов и конференций
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS conference_talk_link (
                conference_id INT NOT NULL REFERENCES conferences(id) ON DELETE CASCADE,
                talk_id INT NOT NULL REFERENCES talks(id) ON DELETE CASCADE,
                PRIMARY KEY (conference_id, talk_id)
            );
        ''')

        # Заполнение тестовыми данными
        await connection.execute('''
            INSERT INTO users (username, password_hash) VALUES
            ('admin', '$2b$12$KIX9H3uFCwbE/5zCRgH8lO5nS1ybQhK9LVW8UuC8eb1IwdS9hKk4G') -- password: secret
            ON CONFLICT (username) DO NOTHING;  -- Не добавлять, если уже существует
        ''')

        # Пример добавления тестовой конференции
        await connection.execute('''
            INSERT INTO conferences (title, description, start_date, end_date) VALUES
            ('Tech Conference 2024', 'Annual tech conference', '2024-06-01 09:00', '2024-06-02 17:00')
            ON CONFLICT (title) DO NOTHING;
        ''')

        # Пример добавления тестового доклада
        await connection.execute('''
            INSERT INTO talks (title, description, speaker_id) VALUES
            ('Innovations in AI', 'A talk about the latest innovations in AI.', 1)
            ON CONFLICT (title) DO NOTHING;
        ''')

        # Пример связывания доклада с конференцией
        await connection.execute('''
            INSERT INTO conference_talk_link (conference_id, talk_id) VALUES
            (1, 1)
            ON CONFLICT (conference_id, talk_id) DO NOTHING;
        ''')
        
    await pool.close()  # Закрываем пул после выполнения всех операций

if __name__ == '__main__':
    asyncio.run(init_db())

