# Шаг 1. Выбор датасета

В качестве рассматриваемого датасета возьмем данные по банковским операциям с использованием кредитных карт.
![1-dataset](pics/1-dataset.png)

# Шаг 2. Создание базы данных и загрузка датасета

Создадим БД локально, используя GUI и загрузим данные из csv файла.
![2-creation](pics/2-creation.png)

# Шаг 3. Выполнение CRUD запросов без индекса

1. Find

Проверим, что данные загрузились валидно. Для этого выполним запрос поиска:

![3-find](pics/3-find.png)

Посмотрим на время выполнения. Оно составило 3 мс.

![4-find-time](pics/4-find-time.png)

2. Insert

Запрос вставки:

![5-insert](pics/5-insert.png)

Запрос вставки выполнился за 0 мс.

![6-insert-time](pics/6-insert-time.png)

3. Delete

Запрос удаления:

![7-delete](pics/7-delete.png)

Запрос удаления выполнился за 1 мс.

![8-delete-time](pics/8-delete-time.png)

4. Update

Запрос обновления:

![9-update](pics/9-update.png)

Запрос обновления выполнился за 6 мс.

![10-update-time](pics/10-update-time.png)

# Шаг 4. Создание индекса

Создадим индекс для текущей таблицы creditFraud

![11-index](pics/11-index.png)

# Шаг 5. Выполнение CRUD запросов с индексом

1. Find

Выполним запрос поиска уже с использованием индекса

![12-index](pics/12-index-find.png)

Посмотрим на время выполнения. Оно составило 0 мс.

![13-index-find-time](pics/4-find-time.png)

2. Insert

Запрос вставки:

![14-index-insert](pics/14-index-insert.png)

Запрос вставки выполнился за 0 мс.

![15-index-insert-time](pics/15-index-insert-time.png)

3. Delete

Запрос удаления:

![16-index-delete](pics/16-index-delete.png)

Запрос удаления выполнился за 0 мс.

![17-index-delete-time](pics/17-index-delete-time.png)

4. Update

Запрос обновления:

![18-index-update](pics/18-index-update.png)

Запрос обновления выполнился за 0 мс.

![19-index-update-time](pics/19-index-update-time.png)

# Выводы:

Индекс существенно ускоряет CRUD-запросы. Для данного датасета ускорение позволило мгновенно выполнять запросы.