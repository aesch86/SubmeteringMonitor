import pickle



def restore(file_path):
    instance_list = []
    restored_task_instance = None
    try:
        with open(file_path, "rb") as file:
            restored_task_instance = pickle.load(file)
    except Exception as e:
        print(e)
    if restored_task_instance:
        is_list = isinstance(restored_task_instance, list)
        instance_list.extend(restored_task_instance) if is_list else instance_list.append(restored_task_instance)

    return instance_list
