import pickle


def save(file_path,Instance):
    try:
        with open(file_path, "wb") as file:
            pickle.dump(Instance, file)
    except:
        print("failure")