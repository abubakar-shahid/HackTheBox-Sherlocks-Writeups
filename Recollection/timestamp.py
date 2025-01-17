import pytsk3
import sys

def extract_creation_time(image_path, target_file):
    try:
        img = pytsk3.Img_Info(image_path)
        fs = pytsk3.FS_Info(img, offset=0)

        for dir_entry in fs.open_dir("/"):
            if dir_entry.info.name.name.decode() == target_file:
                metadata = dir_entry.info.meta
                if metadata:
                    print(f"Creation Time (UTC): {metadata.crtime}")
                    print(f"Modification Time (UTC): {metadata.mtime}")
                    print(f"Access Time (UTC): {metadata.atime}")
                else:
                    print("Metadata not available for the file.")
                return
        print(f"File {target_file} not found.")
    except Exception as e:
        print(f"Error: {e}")

# Replace with your image path and target filename
image_path = "./recollection.bin"
target_file = "./file.None.0xfffffa8003b62990.img"

extract_creation_time(image_path, target_file)
