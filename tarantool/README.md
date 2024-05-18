# Конфигурация кластера

Зададим топологию кластера:

- 3 ноды
  - 1 мастер нода
  - 2 слейв ноды реплики

![1-topology](pics/1-topology.png)

Настроим кластер в режиме Automated Failover: при удалении мастер-ноды на кластере будут происходить выборы нового мастера:

![2-failover](pics/2-failover.png)

Используем утилиту tt от Tarantool для инициализации окружения:

```bash
tt init
```

В директории instances.enabled добавим файл `instances.yaml`, который определяет запускаемые инстансы:

```yaml
instance001:
instance002:
instance003:
```

В той же директории создаем `config.yaml`, в котором опишем конфигурацию кластера:

```yml
credentials:
  users:
    admin:
      password: "admin"
      roles: [super]
    replicator:
      password: "topsecret"
      roles: [replication]
iproto:
  advertise:
    peer:
      login: replicator
replication:
  failover: election
groups:
  group001:
    replicasets:
      replicaset001:
        instances:
          instance001:
            iproto:
              listen:
                - uri: "127.0.0.1:3301"
          instance002:
            iproto:
              listen:
                - uri: "127.0.0.1:3302"
          instance003:
            iproto:
              listen:
                - uri: "127.0.0.1:3303"
```

В этом файле также определены два пользователя: `admin` и `replicator` с соответствующими правами. В дальнейшем для CRUD операций через API Python будем использовать пользователя `admin`.

# Запуск кластера

Запустим кластер:
![start](pics/3-start.png)

Убедимся, что конфигурация валидная и все ноды запустились:
![status](pics/4-status.png)

Подключимся к мастеру - им стала нода 1, как можно увидеть из результатов голосования:
![master](pics/5-master.png)

Посмотрим текстовую схему топологии кластера:
![replication](pics/6-replication.png)
Ноды 2 и 3 являются репликами мастера - ноды 1

# Схема хранения данных

Создадим схему для сотрудников:
![schema](pics/7-schema.png)
Будем хранить id, имя, позицию и зарплату сотрудника.

Создадим индекс для id:
![index](pics/8-index.png)

# Подключение через Python

Напишем простой коннектор к БД. Добавим функции создания сотрудников и выбора всех сотрудников из БД:

```python
def add_employee(employee):
    conn.space("employees").insert(employee)
    print(f"Сотрудник {employee[1]} добавлен")


def get_all_employees():
    result = conn.space("employees").select()
    print("Список сотрудников:")
    for employee in result:
        print(employee)
```

Создадим подключение через `admin` пользователя:

```python
conn = tarantool.connect("localhost", 3301, user="admin", password="admin")
```

Заполним БД тестовыми данными:

```python
add_employee((1, "John Doe", "Manager", 5000))
add_employee((2, "Jane Smith", "Developer", 4000))
get_all_employees()
```

Выполним скрипт:
![python-api](pics/9-python-api.png)
Он успешно вставил данные в БД.

# Failover

Отключим мастер-ноду и спровоцируем кластер выбрать нового мастера. Также проверим, насколько успешные данные были реплицированы на оставшиеся ноды:
![failover](pics/10-failover-node1.png)

Подключимся ко второй ноде, узнаем о результатах голосования:
![new-elections](pics/11-new-elections.png)
Мастером стала третья нода, вторая слейвом.

Подключимся к новому мастеру - третьей ноде и посмотрим информацию по репликам:
![new-status](pics/12-new-status.png)
Как видим, upstream статус 1-й ноды disconnected, а downstream статус - stopped. То есть 3-я нода считает старого мастера отключенным, а старый мастер говорит, что его отключили, что мы в действительности и сделали.
Вторая нода (instance002) по прежнему работает.

С помощью коннектора на Python проверим, остались ли данные на новом мастере и реплике:

```python
conn = tarantool.connect("localhost", 3303, user="admin", password="admin")
get_all_employees()
```

![same-data](pics/13-same-data.png)
Действительно, данные сохранились!
