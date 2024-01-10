# Бонусная программа для сети магазинов

## Описание проекта
Проект представляет собой бонусную программу для небольшой сети магазинов. Основная цель проекта — предоставить возможность продавцам вводить номер покупателя и осуществлять несколько операций с ним, включая проведение продажи или обращение по гарантии. Администратор получает более широкие права и имеет возможность управлять данными клиентов, изменять процент начисления бонусов, управлять списком сотрудников и генерировать отчеты.

## Основные функции
1. Ввод и обработка номера покупателя:
   - Если в базе данных отсутствует номер покупателя, предлагается добавить его в систему.
   - Если номер покупателя уже существует, предоставляются два варианта: провести продажу или обратиться по гарантии.

2. Управление клиентами:
   - Администратор может изменять данные клиентов, включая зачисленные бонусы за продажу.

3. Управление процентами начислений:
   - Администратор имеет возможность изменять процент начислений бонусов для клиентов.

4. Управление сотрудниками:
   - Администратор может предоставлять сотрудникам доступ к программе, либо удалять доступ.
   - Администратор может назначать сотрудников администраторами программы или удалять их из администраторов.

5. Отчеты:
   - Генерация отчетов в виде таблицы, содержащих данные о клиентах, сотрудниках и чеках за определенные промежутки времени или за все время.

## Технологии и инструменты
- Библиотеки `aiogram`, `alembic`, `sqlalchemy`, `openpyxl` используются для разработки проекта.
- В качестве базы данных планируется использование `PostgreSQL`.
- Контейнеризация с использованием `Docker`.

## Планы по развитию проекта
- Развертывание и настройка базы данных `PostgreSQL` для хранения данных.
- Создание контейнера `Docker` для обеспечения легкого развертывания.
- Расширение функциональности бонусной программы в соответствии с потребностями магазина.
- Улучшение пользовательского интерфейса.

## Установка и настройка проекта
- Подробные инструкции по установке и настройки проекта будут предоставлены после завершения проекта
- Если все же хочется то клонируем репозиторий
- в .env BOT_TOKEN - ваш токен, DB_URL - ваша бд
- устанавливаем зависимости из requirements
- делаем манипуляции с алембиком alembic upgrade head
- запускаем main.py
- что бы увидить весь функционал добавь свой tg_id в бд и сделай админом или закомить миделвари в хендлерах и добавь себя через бота (пока так, дальше будет реализация создания пользователя другая)