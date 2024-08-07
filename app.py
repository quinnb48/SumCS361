import os
import time
from urllib.parse import urlparse
# https://docs.python.org/3/library/urllib.parse.html
from PIL import Image
import requests
from io import BytesIO
# learn how to buffer in ram for faster load time
# https://pythonmania.org/python-io-bytesio/
import tkinter as tk
from tkinter import filedialog, messagebox
# got the file showing idea from
# https://stackoverflow.com/questions/66663179/how-to-use-windows-file-explorer-to-select-and-return-a-directory-using-python

#headers for get requests
HEADERS = headers = {'User-Agent': 'BirdOfTheDay/1.0 (https://github.com/quinnb48/SumCS361; quinnbehrens@gmail.com)'}

class PhotoMonitor:
    """
    Monitor a textfile for changes, validate URL in the file,
    download and display images. Handle user interaction and
    allow user to save the photo
    """
    def __init__(self, file_path: str):
        """
        Initializes the PhotoMonitor with the path to the text file.

        Args:
            file_path (str): Path to the text file to monitor.
        """
        # attempt to normalize the file path for cross-platform compatibility
        # not sure if it works
        # https://docs.python.org/3/library/os.path.html
        self.file_path = os.path.normpath(file_path)
        self.last_known_content = None

    def read_file(self) -> str:
        """
        Read content of the monitored file.

        Returns:
            str: Stripped content of the file, or None if an error occurs.
        """
        try:
            with open(self.file_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            print(f"The file {self.file_path} does not exist.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def is_valid_url(self, url: str) -> bool:
        """
        Checks if a given URL has a valid scheme (http or https).

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL scheme is valid, False otherwise.
        """
        # https://docs.python.org/3/library/urllib.parse.html
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https')

    def is_valid_image_url(self, url: str) -> bool:
        """
        Verifies if the URL points to a valid image by making a request and checking the image.

        Args:
            url (str): The URL to verify.

        Returns:
            bool: True if the URL points to a valid image, False otherwise.
        """
        try:
            # attempt to deal with windows file path, not sure if it works
            # https://docs.python.org/3/library/os.path.html

            response = requests.get(url, headers = HEADERS)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            # check if valid image
            # https://www.geeksforgeeks.org/check-if-a-file-is-valid-image-with-python/
            img.verify()
            return True
        except Exception as e:
            print(f"Error verifying image from URL: {e}")
            return False

    def save_image_to_cache(self, url: str) -> str:
        """
        Downloads image from the URL and saves it to the cache directory.

        Args:
            url (str): URL of the image to download.

        Returns:
            str: Path to the cached image file, or None if an error occurs.
        """
        # set cache directory and save image if url is valid
        cache_dir = 'cache'
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, 'image.png')
        try:

            response = requests.get(url, headers = HEADERS)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img.save(cache_path)
            return cache_path
        except Exception as e:
            print(f"Error saving image to cache: {e}")
            return None

    def display_photo(self, cache_path: str) -> Image.Image:
        """
        Displays cached image and waits for the user to close the image window.

        Args:
            cache_path (str): The path to the cached image file.

        Returns:
            Image.Image: The displayed image object, or None if an error occurs.
        """
        try:
            img = Image.open(cache_path)
            # display with build in photo app
            img.show()
            return img
        except Exception as e:
            print(f"Error displaying image: {e}")
            return None

    def confirm_photo_viewed(self) -> str:
        """
        Prompts user to confirm that they have viewed the photo.

        Returns:
            str: "ok" by user interaction.
        """
        root = tk.Tk()
        root.withdraw()
        viewed_option = messagebox.showinfo("Photo Viewed", "Press OK to confirm you have viewed the photo.")
        root.destroy()
        return viewed_option

    def prompt_save_photo(self, img: Image.Image):
        """
        Prompts user to save displayed image and handles save operation.

        Args:
            img (Image.Image): Image to be saved.
        """
        root = tk.Tk()
        root.withdraw()
        save_option = messagebox.askyesno("Save Image", "Do you want to save the image?")
        if save_option:
            # prompt user to choose file format and save location
            # https://www.geeksforgeeks.org/python-asksaveasfile-function-in-tkinter/
            save_path = filedialog.asksaveasfilename(
                initialfile='image.png',
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if save_path:
                try:
                    img.save(save_path)
                    print(f"Image saved to {save_path}")
                except Exception as e:
                    print(f"Error saving image: {e}")
            else:
                print("Image not saved.")
        else:
            print("Image not saved.")
        root.destroy()

    def mark_as_viewed(self) -> None:
        """
        Marks the monitored file as "viewed" by writing "viewed" to the file.
        """
        try:
            with open(self.file_path, 'w') as file:
                file.write("viewed")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def monitor(self) -> None:
        """
        Continuously monitors the text file for changes, validates the URL,
        downloads and displays the image, and handles user interactions.
        """
        while True:
            current_content = self.read_file()
            if current_content is None:
                time.sleep(1)
                continue

            if current_content != self.last_known_content:
                self.last_known_content = current_content

                # checks if url is valid and display
                if self.is_valid_url(current_content) and self.is_valid_image_url(current_content):
                    cache_path = self.save_image_to_cache(current_content)
                    if cache_path:
                        img = self.display_photo(cache_path)
                        if img:
                            if self.confirm_photo_viewed():
                                self.prompt_save_photo(img)
                                self.mark_as_viewed()
                            # deletes cached photo
                            os.remove(cache_path)
                else:
                    print("Invalid photo URL or file does not exist")

            time.sleep(1)

if __name__ == "__main__":
    # Set file path to read
    file_path = '/Users/quinnbehrens/Documents/GitHub/SumCS361/displayphoto.txt'
    # Create PhotoMonitor instart and monitor file
    monitor = PhotoMonitor(file_path)
    monitor.monitor()
