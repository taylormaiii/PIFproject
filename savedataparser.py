import json
from rubymarshal.reader import load as load_marshal


def make_json_safe(obj, seen=None):
    if seen is None:
        seen = set()

    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, (bytes, bytearray)):
        b = bytes(obj)
        try:
            return b.decode("utf-8")
        except UnicodeDecodeError:
            return b.hex()

    if isinstance(obj, dict):
        obj_id = id(obj)
        if obj_id in seen:
            return "<cycle>"
        seen.add(obj_id)
        try:
            return {
                str(key): make_json_safe(value, seen)
                for key, value in obj.items()
            }
        finally:
            seen.remove(obj_id)

    if isinstance(obj, (list, tuple)):
        obj_id = id(obj)
        if obj_id in seen:
            return "<cycle>"
        seen.add(obj_id)
        try:
            return [make_json_safe(item, seen) for item in obj]
        finally:
            seen.remove(obj_id)

    if hasattr(obj, "__dict__"):
        obj_id = id(obj)
        if obj_id in seen:
            return "<cycle>"
        seen.add(obj_id)
        try:
            return {str(key): make_json_safe(value, seen) for key, value in vars(obj).items()}
        finally:
            seen.remove(obj_id)

    return str(obj)

def rxdata_to_json(rxdata_path, json_path):
    # 1. Read the binary .rxdata file
    with open(rxdata_path, 'rb') as f:
        # Load the Ruby Marshal binary into Python objects
        ruby_data = load_marshal(f)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(make_json_safe(ruby_data),f,indent=2,ensure_ascii=False)
        print(f"Successfully wrote JSON to: {json_path}")


save_slot = input("What letter save slot is it? ")
rxdata_path = rf"C:\Users\tjkit\AppData\Roaming\infinitefusion\File {save_slot}.rxdata"
rxdata_to_json(rxdata_path, f"output{save_slot}.json")
