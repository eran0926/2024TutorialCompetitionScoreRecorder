
def get_nested_attribute(obj, attr_name):
    attrs = attr_name.split('.')
    current_obj = obj
    for attr in attrs:
        try:
            current_obj = getattr(current_obj, attr)
        except AttributeError:
            return f"屬性 '{attr_name}' 不存在"
    return current_obj

# 定義一個函數來從字符串中設置屬性值（包括嵌套屬性）


def set_nested_attribute(obj, attr_name, value):
    if value.isnumeric():
        value = int(value)
    attrs = attr_name.split('.')
    current_obj = obj
    for attr in attrs[:-1]:
        try:
            current_obj = getattr(current_obj, attr)
        except AttributeError:
            return f"屬性 '{attr_name}' 不存在"
    final_attr = attrs[-1]
    if hasattr(current_obj, final_attr):
        setattr(current_obj, final_attr, value)
        return f"屬性 '{attr_name}' 已設置為 {value}"
    else:
        return f"屬性 '{attr_name}' 不存在"
