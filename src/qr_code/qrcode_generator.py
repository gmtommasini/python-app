import qrcode
import base64
from io import BytesIO

# Create a QR code instance
def create_qrcode(data: str, path:str = None, box_size=10, border=1, base64encode=False):
    '''
    Create a qrcode image buffer by default.
    It can return a base64 code if the parameter base64encode is set to True
    It can save the image to a PNG file if a path=folder/filename is provided
    '''
    qr = qrcode.QRCode(box_size = box_size, border = border)

    # Add data to the QR code
    if data is None:
        print("QRCODE ERROR, data is empty")
        return 0
    qr.add_data(data)

    # Generate the QR code
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    if path is not None:
        print(f"Saving file at {path}")
        img.save(path)
        return 0
    
    img_buffer = BytesIO()
    # Save the image to a buffer
    img.save(img_buffer)
    
    if base64encode:
        image_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        print("Returning a base64code image")
        return image_base64
    
    img_buffer.seek(0)
    print("Returning a png image buffer")
    return img_buffer


if __name__ == '__main__':
    create_qrcode("test", 'test.png')
    create_qrcode("test")