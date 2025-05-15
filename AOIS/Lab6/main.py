class Hash_map:

    def __init__(self, base_capacity=20, trace_enabled=False):
        self.set_up(base_capacity, trace_enabled)

    def set_up(self, base_capacity=20, trace_enabled=False):
        self.base_capacity = max(base_capacity, 20)
        self.trace_enabled = trace_enabled
        self.entry_count = 0
        self.storage = []
        counter = 0
        while counter < self.base_capacity:
            self.storage.append(self.make_entry())
            counter = counter + 1
        self.letter_map = {}
        letter_code = 0
        while letter_code < 33:
            self.letter_map[chr(ord('А') + letter_code)] = letter_code
            letter_code = letter_code + 1

    def make_entry(self, label=None, info=None):
        new_entry = {
            "label": label,
            "info": info,
            "code": None,
            "position": None,
            "collision_mark": 0,
            "occupied_mark": 0,
            "terminal_mark": 0,
            "link_mark": 0,
            "delete_mark": 0,
            "next_link": None
        }
        return new_entry

    def get_numeric_code(self, label):
        label_upper = label.upper()
        first_value = 0
        if label_upper[0] in self.letter_map:
            first_value = self.letter_map[label_upper[0]]
        else:
            first_value = 0
        second_value = 0
        if len(label_upper) > 1:
            if label_upper[1] in self.letter_map:
                second_value = self.letter_map[label_upper[1]]
            else:
                second_value = 0
        result = first_value * 33 + second_value
        return result

    def calculate_position(self, numeric_code):
        position = numeric_code % self.base_capacity
        return position

    def find_slot(self, label, is_for_addition=False):
        start_point = self.calculate_position(self.get_numeric_code(label))
        if self.trace_enabled:
            print(f"Ключ: {label}, начальная точка: {start_point}")
        first_empty = None
        current_point = start_point
        while True:
            entry = self.storage[current_point]
            if self.trace_enabled:
                print(f"Проверка позиции {current_point}: Label={entry['label']}, Занято={entry['occupied_mark']}, Удалено={entry['delete_mark']}")
            if entry["occupied_mark"] == 0 and entry["delete_mark"] == 0:
                if self.trace_enabled:
                    print(f"Свободная позиция найдена: {current_point}")
                if is_for_addition:
                    return current_point
                else:
                    return None
            if is_for_addition:
                if entry["delete_mark"] == 1 and first_empty is None:
                    first_empty = current_point
                    if self.trace_enabled:
                        print(f"Запомнена удалённая позиция: {current_point}")
            elif entry["occupied_mark"] == 1 and entry["delete_mark"] == 0 and entry["label"] == label:
                if self.trace_enabled:
                    print(f"Ключ {label} найден в позиции {current_point}")
                return current_point
            current_point = (current_point + 1) % self.base_capacity
            if current_point == start_point:
                if self.trace_enabled:
                    print(f"Цикл завершён, возвращено: {first_empty}")
                if is_for_addition:
                    return first_empty
                else:
                    return None

    def grow_storage(self):
        old_storage = self.storage
        self.base_capacity = self.base_capacity * 2
        self.storage = []
        counter = 0
        while counter < self.base_capacity:
            self.storage.append(self.make_entry())
            counter = counter + 1
        self.entry_count = 0
        index = 0
        while index < len(old_storage):
            entry = old_storage[index]
            if entry["occupied_mark"] == 1 and entry["delete_mark"] == 0:
                self.store_item(entry["label"], entry["info"])
            index = index + 1

    def store_item(self, label, info):
        if len(str(info)) > 10:
            info = f"ptr_{id(info)}"
            link_flag = 1
        else:
            link_flag = 0
        result = self.retrieve_item(label)
        if result is not None:
            raise KeyError(f"Ключ '{label}' уже существует")
        numeric_code = self.get_numeric_code(label)
        initial_pos = self.calculate_position(numeric_code)
        target_pos = self.find_slot(label, is_for_addition=True)
        if target_pos is None:
            self.grow_storage()
            target_pos = self.find_slot(label, is_for_addition=True)
        entry = self.storage[target_pos]
        if entry["occupied_mark"] == 0 or entry["delete_mark"] == 1:
            self.entry_count = self.entry_count + 1
        entry["label"] = label
        entry["info"] = info
        entry["code"] = numeric_code
        entry["position"] = initial_pos
        entry["occupied_mark"] = 1
        entry["delete_mark"] = 0
        entry["link_mark"] = link_flag
        has_collision = False
        index = 0
        while index < len(self.storage):
            if self.storage[index]["occupied_mark"] == 1 and self.storage[index]["label"] != label and self.calculate_position(self.storage[index]["code"]) == initial_pos:
                has_collision = True
                break
            index = index + 1
        if has_collision:
            entry["collision_mark"] = 1
            if target_pos > 0:
                if self.storage[target_pos - 1]["occupied_mark"] == 1 and self.storage[target_pos - 1]["collision_mark"] == 1:
                    self.storage[target_pos - 1]["next_link"] = target_pos
                    self.storage[target_pos - 1]["terminal_mark"] = 0
            entry["terminal_mark"] = 1
        if self.trace_enabled:
            print(f"Запись ({label}, {info}) сохранена в {target_pos}, Коллизия={entry['collision_mark']}, Конец={entry['terminal_mark']}\n")

    def retrieve_item(self, label):
        target_pos = self.find_slot(label, is_for_addition=False)
        if target_pos is not None:
            if self.storage[target_pos]["occupied_mark"] == 1 and self.storage[target_pos]["delete_mark"] == 0:
                data = self.storage[target_pos]["info"]
                if self.trace_enabled:
                    print(f"Найдено в позиции {target_pos}\n")
                return data
        if self.trace_enabled:
            print("Ключ не найден\n")
        return None

    def remove_item(self, label):
        target_pos = self.find_slot(label, is_for_addition=False)
        if target_pos is None:
            raise KeyError(f"Ключ '{label}' не найден")
        elif self.storage[target_pos]["occupied_mark"] == 0:
            raise KeyError(f"Ключ '{label}' не найден")
        elif self.storage[target_pos]["delete_mark"] == 1:
            raise KeyError(f"Ключ '{label}' не найден")
        final_data = self.storage[target_pos]
        final_data["delete_mark"] = 1
        self.entry_count = self.entry_count - 1
        if final_data["collision_mark"] == 0 and final_data["terminal_mark"] == 1:
            final_data["occupied_mark"] = 0
        elif final_data["terminal_mark"] == 1:
            prev_pos = target_pos
            while True:
                if self.storage[prev_pos]["next_link"] == target_pos:
                    break
                if self.storage[prev_pos]["next_link"] is None:
                    prev_pos = (prev_pos - 1) % self.base_capacity
                else:
                    prev_pos = self.storage[prev_pos]["next_link"]
                if prev_pos == target_pos:
                    break
            self.storage[prev_pos]["terminal_mark"] = 1
            self.storage[prev_pos]["next_link"] = None
            final_data["occupied_mark"] = 0
        elif final_data["collision_mark"] == 0:
            next_pos = final_data["next_link"]
            if next_pos is not None and next_pos < self.base_capacity:
                next_data = self.storage[next_pos]
                final_data["label"] = next_data["label"]
                final_data["info"] = next_data["info"]
                final_data["code"] = next_data["code"]
                final_data["position"] = next_data["position"]
                final_data["occupied_mark"] = next_data["occupied_mark"]
                final_data["delete_mark"] = next_data["delete_mark"]
                final_data["collision_mark"] = next_data["collision_mark"]
                final_data["terminal_mark"] = next_data["terminal_mark"]
                final_data["next_link"] = next_data["next_link"]
                next_data["occupied_mark"] = 0
        else:
            next_pos = final_data["next_link"]
            if next_pos is not None and next_pos < self.base_capacity:
                next_data = self.storage[next_pos]
                final_data["label"] = next_data["label"]
                final_data["info"] = next_data["info"]
                final_data["code"] = next_data["code"]
                final_data["position"] = next_data["position"]
                final_data["delete_mark"] = next_data["delete_mark"]
                final_data["collision_mark"] = next_data["collision_mark"]
                final_data["terminal_mark"] = next_data["terminal_mark"]
                final_data["next_link"] = next_data["next_link"]
                next_data["occupied_mark"] = 0
        if self.trace_enabled:
            print(f"Ключ {label} удалён из позиции {target_pos}\n")

    def update_item(self, label, new_info):
        target_pos = self.find_slot(label, is_for_addition=False)
        if target_pos is None:
            raise KeyError(f"Ключ '{label}' не найден для обновления")
        elif self.storage[target_pos]["occupied_mark"] == 0:
            raise KeyError(f"Ключ '{label}' не найден для обновления")
        elif self.storage[target_pos]["delete_mark"] == 1:
            raise KeyError(f"Ключ '{label}' не найден для обновления")
        if len(str(new_info)) > 10:
            new_info = f"ptr_{id(new_info)}"
            self.storage[target_pos]["link_mark"] = 1
        else:
            self.storage[target_pos]["link_mark"] = 0
        self.storage[target_pos]["info"] = new_info
        if self.trace_enabled:
            print(f"Данные для ключа {label} обновлены на {new_info} в позиции {target_pos}\n")

    def display_content(self):
        headers = ["Поз", "Ключ", "Код", "ПозХеш", "Коллизия", "Занято", "Терминальный", "Связь", "Вычеркивание", "Переполнение", "Данные"]
        rows = []
        index = 0
        while index < len(self.storage):
            final_data = self.storage[index]
            next_str = str(final_data["next_link"]) if final_data["next_link"] is not None else '-'
            row = [
                str(index), final_data["label"] or '-', str(final_data["code"] or '-'), str(final_data["position"] or '-'),
                str(final_data["collision_mark"]), str(final_data["occupied_mark"]), str(final_data["terminal_mark"]),
                str(final_data["link_mark"]), str(final_data["delete_mark"]), next_str, final_data["info"] or '-'
            ]
            rows.append(row)
            index = index + 1
        col_widths = []
        header_index = 0
        while header_index < len(headers):
            max_length = 0
            row_index = 0
            while row_index < len([headers] + rows):
                if row_index == 0:
                    current_length = len(headers[header_index])
                else:
                    current_length = len(rows[row_index - 1][header_index])
                if current_length > max_length:
                    max_length = current_length
                row_index = row_index + 1
            col_widths.append(max_length)
            header_index = header_index + 1

        def format_line(row):
            result = ""
            column_index = 0
            while column_index < len(row):
                if column_index > 0:
                    result = result + " | "
                result = result + row[column_index].ljust(col_widths[column_index])
                column_index = column_index + 1
            return result
        print(format_line(headers))
        print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        row_index = 0
        while row_index < len(rows):
            print(format_line(rows[row_index]))
            row_index = row_index + 1

    def get_length(self):
        return self.entry_count

    def process_input(self, data):
        try:
            return int(data)
        except ValueError:
            return data

    def begin(self):
        sample_data = [
            ("Абаев", "Сергей"), ("Бобков", "Тимур"), ("Видерт", "Евгений"),
            ("Гракова", "Иван"), ("Кожевников", "Максим"), ("Ковалев", ""),
            ("Крикунов", ""), ("Кот", ""), ("Давыденко", "Александр"),
            ("Горбань", ""), ("Данилов", ""), ("Козлов", ""), ("Азимов", "")
        ]
        index = 0
        while index < len(sample_data):
            label = sample_data[index][0]
            info = sample_data[index][1]
            self.store_item(label, info)
            index = index + 1

        while True:
            self.display_content()
            print("\nВыберите действие:")
            print("1. Добавить запись")
            print("2. Найти запись")
            print("3. Удалить запись")
            print("4. Изменить запись")
            print("0. Выйти")
            action = input("Введите номер (0-4): ").strip()
            try:
                if action == '1':
                    label = input("Введите ключ (фамилию): ").strip()
                    info = input("Введите данные (имя): ").strip()
                    self.store_item(label, info)
                    print("Запись добавлена.")
                elif action == '2':
                    label = input("Введите ключ для поиска (фамилию): ").strip()
                    result = self.retrieve_item(label)
                    if result:
                        print(f"Результат: {result}")
                    else:
                        print("Запись не найдена.")
                elif action == '3':
                    label = input("Введите ключ для удаления (фамилию): ").strip()
                    self.remove_item(label)
                    print("Запись удалена.")
                elif action == '4':
                    label = input("Введите ключ для изменения (фамилию): ").strip()
                    new_info = input("Введите новые данные (имя): ").strip()
                    self.update_item(label, new_info)
                    print("Запись изменена.")
                elif action == '0':
                    print("Программа завершена.")
                    break
                else:
                    print("Неверный ввод, попробуйте снова.")
            except KeyError as error:
                print(error)

if __name__ == "__main__":
    hash_map = Hash_map(base_capacity=20, trace_enabled=True)
    hash_map.begin()