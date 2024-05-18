import tarantool

conn = tarantool.connect("localhost", 3303, user="admin", password="admin")


def add_employee(employee):
    conn.space("employees").insert(employee)
    print(f"Сотрудник {employee[1]} добавлен")


def get_all_employees():
    result = conn.space("employees").select()
    print("Список сотрудников:")
    for employee in result:
        print(employee)


add_employee((1, "John Doe", "Manager", 5000))
add_employee((2, "Jane Smith", "Developer", 4000))
get_all_employees()
