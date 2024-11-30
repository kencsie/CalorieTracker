import os


def get_subdirectories(start_path):
    top_subdirectories = list()
    for entry in os.listdir(start_path):
        full_path = os.path.join(start_path, entry)
        if os.path.isdir(full_path):
            top_subdirectories.append(full_path)
    return top_subdirectories


def main():
    sub_dirs = get_subdirectories(os.getcwd())

    # Walk each subdir and modify the rgb files within them
    for directory in sub_dirs:
        # Get the date the photo was captured from the subdirectory name
        capture_date = os.path.basename(directory)

        # Walk the subdirectories
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == "rgb.jpg":
                    # Get the time the photo was captured from the file's directory name
                    capture_time = os.path.basename(root)

                    # Rename the files
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, f"{capture_date}_{capture_time}_rgb.jpg")
                    os.rename(old_path, new_path)
                    print(f"Successfully renamed {old_path} to {new_path}")


if __name__ == "__main__":
    main()
