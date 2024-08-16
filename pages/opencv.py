from h2o_wave import main, app, Q, ui, on, run_on
import cv2
import io
import os
from utils.ui import add_card, clear_cards

# Function to handle OpenCV operations
async def opencvPage(q: Q):
    clear_cards(q)

    # Show the upload interface
    add_card(q, 'upload', ui.form_card(
        box=ui.box('grid', width='400px'),
        items=[
            ui.file_upload(name='image_file', label='Upload an image file', multiple=False),
        ]
    ))

    # If an image is uploaded, display it and show operation options
    if q.client.image_path is not None:
        # Display the uploaded image
        add_card(q, 'uploaded_image', ui.image_card(
            box='grid',
            title='Uploaded Image',
            type='png',
            path=q.client.image_path
        ))

        # Display the form for selecting OpenCV operations
        add_card(q, 'options', ui.form_card(
            box=ui.box('grid', width='400px'),
            items=[
                ui.dropdown(name='operation', label='Choose operation', choices=[
                    ui.choice(name='gray', label='Convert to Grayscale'),
                    ui.choice(name='blur', label='Apply Gaussian Blur'),
                    ui.choice(name='edge', label='Canny Edge Detection'),
                    ui.choice(name='flip', label='Flip Image'),
                    ui.choice(name='rotate', label='Rotate Image 90 degrees'),
                ]),
                ui.button(name='perform', label='Perform Operation', primary=True),
            ]
        ))

    # If the perform button was clicked and an operation is selected
    if q.args.perform:
        try:
            result_img = None
            operation = q.args.operation
            print(f"Operation selected: {operation}")  # Debugging statement

            if operation == 'gray':
                result_img = cv2.cvtColor(q.client.image, cv2.COLOR_BGR2GRAY)
            elif operation == 'blur':
                result_img = cv2.GaussianBlur(q.client.image, (15, 15), 0)
            elif operation == 'edge':
                result_img = cv2.Canny(q.client.image, 100, 200)
            elif operation == 'flip':
                result_img = cv2.flip(q.client.image, 1)  # Flip horizontally
            elif operation == 'rotate':
                result_img = cv2.rotate(q.client.image, cv2.ROTATE_90_CLOCKWISE)

            if result_img is not None:
                # Convert the result to a format that can be displayed (e.g., PNG)
                is_success, buffer = cv2.imencode(".png", result_img)
                q.client.result_image = io.BytesIO(buffer).getvalue()
                result_image_path = f'/tmp/{operation}_result.png'

                with open(result_image_path, 'wb') as f:
                    f.write(q.client.result_image)

                q.client.image_path = result_image_path

                # Replace the uploaded image with the updated image
                add_card(q, 'uploaded_image', ui.image_card(
                    box='grid',
                    title=f"Result of {operation}",
                    type='png',
                    path=result_image_path
                ))
        except Exception as e:
            await show_error(q, f"An error occurred while performing the operation: {str(e)}")
            return

    await q.page.save()

# Function to handle image upload
async def handle_image_upload(q: Q):
    if q.args.image_file:
        try:
            upload_dir = '/mnt/data/uploads'  # Use a more stable directory for uploads
            os.makedirs(upload_dir, exist_ok=True)

            file_path = q.args.image_file[0]
            local_path = await q.site.download(file_path, upload_dir)

            # Read the image using OpenCV
            img = cv2.imread(local_path)

            if img is None:
                raise ValueError("The uploaded file is not a valid image.")

            q.client.image = img
            q.client.image_path = local_path

            # Show the uploaded image and options
            await opencvPage(q)

        except Exception as e:
            await show_error(q, f"Error loading image file: {str(e)}")

    else:
        await show_error(q, "No image file uploaded.")

# Function to display error messages
async def show_error(q: Q, message: str):
    q.page['error'] = ui.form_card(
        box='grid',
        items=[ui.text(f"Error: {message}")]
    )
    await q.page.save()
