import os
from PIL import Image
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap import Separator


class SIMAAKCROP(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.images_path = ttk.StringVar(value="./")
        self.output_folder = ttk.StringVar(value="./cropped_images")

        self.start = ttk.IntVar(value=6800)
        self.end = ttk.IntVar(value=7200)

        self.left = ttk.IntVar(value=380)
        self.right = ttk.IntVar(value=680)  # Assuming right is left + width
        self.top = ttk.IntVar(value=893)
        self.bottom = ttk.IntVar(value=1255)  # Assuming bottom is top + height

        instruction_text = "Please enter correct information: "
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=10)

        self.create_form_entry("Images Path: ", self.images_path)
        self.create_form_entry("Output Folder Path: ", self.output_folder)

        separator = Separator(self, orient="horizontal")
        separator.pack(fill=X, padx=5, pady=10)

        self.create_form_entry("START: ", self.start)
        self.create_form_entry("END: ", self.end)

        separator = Separator(self, orient="horizontal")
        separator.pack(fill=X, padx=5, pady=10)

        self.create_form_entry("LEFT: ", self.left)
        self.create_form_entry("RIGHT: ", self.right)
        self.create_form_entry("TOP: ", self.top)
        self.create_form_entry("BOTTOM: ", self.bottom)

        self.create_buttonbox()

        separator = Separator(self, orient="horizontal")
        separator.pack(fill=X, padx=5, pady=10)

        # self.progress = ttk.Progressbar(self, orient="horizontal", length=100, mode="determinate")
        # self.progress.pack(pady=10)
        

    def create_form_entry(self, label, variable):
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=5)

        form_field_label = ttk.Label(form_field_container, text=label, width=20)
        form_field_label.pack(side=LEFT, padx=12)

        form_input = ttk.Entry(form_field_container, textvariable=variable)
        form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

        return form_input

    def create_buttonbox(self):
        button_container = ttk.Frame(self)
        button_container.pack(fill=X, expand=YES, pady=(15, 10))

        # Center the buttons by using an inner frame
        inner_button_container = ttk.Frame(button_container)
        inner_button_container.pack(pady=10)

        submit_btn = ttk.Button(
            master=inner_button_container,
            text="SUBMIT",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=10,
        )
        submit_btn.pack(side=LEFT, padx=5)

        cancel_btn = ttk.Button(
            master=inner_button_container,
            text="CANCEL",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=10,
        )
        cancel_btn.pack(side=LEFT, padx=5)


    def on_submit(self):
        images_path = self.images_path.get()
        output_folder = self.output_folder.get()

        start = self.start.get()
        end = self.end.get()

        left = self.left.get()
        right = self.right.get()
        top = self.top.get()
        bottom = self.bottom.get()

        # Define the box to crop (left, upper, right, lower)
        box = (left, top, right, bottom)

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Calculate the total number of images to be processed
        total_images = end - start + 1

        # Set the progress bar's maximum value to the total number of images
        # self.progress["maximum"] = total_images
        # self.progress["value"] = 0

        # Counter for the number of images cropped
        counter = start

        # Loop through all jpg images in the specified directory
        for filename in os.listdir(images_path):
            if filename.endswith('.jpg') and start <= counter <= end:
                # Open the image
                img = Image.open(os.path.join(images_path, filename))
                # Crop the image
                cropped_img = img.crop(box)
                # Save the cropped image in the output folder with a new filename
                cropped_img.save(os.path.join(output_folder, f'{counter}.png'))
                counter += 1
                # Update the progress bar's value
                # self.progress.step(200/total_images)
                # self.update_idletasks()

        toast = ToastNotification(
            title="Cropping Successful!",
            message=f"Images successfully cropped and saved to {output_folder}",
            duration=3000,
        )
        toast.show_toast()



    def on_cancel(self):
        self.quit()


if __name__ == "__main__":
    app = ttk.Window("SIMAAK Crop", "superhero", resizable=(False, False))
    SIMAAKCROP(app)
    app.mainloop()
