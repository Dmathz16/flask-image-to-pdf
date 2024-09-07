import os
from PIL import Image  # pip install pillow
from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def index():
    # Define the directories
    dir_source_images = os.path.join(os.getcwd(), 'application', 'static')
    dir_output_pdfs = os.path.join(os.getcwd(), 'application', 'uploads')

    # Ensure the output directory exists
    if not os.path.exists(dir_output_pdfs):
        os.makedirs(dir_output_pdfs)

    file_to_download = None

    # Check if the source directory exists
    if os.path.exists(dir_source_images):
        for file in os.listdir(dir_source_images):
            if file.split('.')[-1].lower() in ('png', 'jpeg', 'jpg'):  # Ensure case-insensitivity
                image = Image.open(os.path.join(dir_source_images, file))
                image_converted = image.convert('RGB')
                pdf_filename = '{0}.pdf'.format(file.split('.')[-2])
                image_converted.save(os.path.join(dir_output_pdfs, pdf_filename))

                # Store the first file for download after conversion
                file_to_download = os.path.join(dir_output_pdfs, pdf_filename)

        # Send the first generated PDF file to the client
        if file_to_download:
            return send_file(file_to_download, as_attachment=True)

    return "Source directory not found or no images to convert!"

if __name__ == "__main__":
    app.run(debug=True)
