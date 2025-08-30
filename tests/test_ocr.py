from transformers import VisionEncoderDecoderModel, TrOCRProcessor
import torch
from PIL import Image
import os

# Preload model and processor
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device for captcha reading: {device}")
processor = TrOCRProcessor.from_pretrained("anuashok/ocr-captcha-v3")
model = VisionEncoderDecoderModel.from_pretrained("anuashok/ocr-captcha-v3").to(device)

# Variables
number_samples = len(os.listdir("tests/assets/"))
correct = 0

def read_captcha(image_path, answer):
    global correct

    # Prepare image
    image = Image.open(image_path).convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255))
    combined = Image.alpha_composite(background, image).convert("RGB")
    pixel_values = processor(combined, return_tensors="pt").pixel_values.to(device)

    # Run model and generate text
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    # Check results
    is_correct = generated_text == answer
    if is_correct:
        correct += 1
    print(f"{'Correct' if is_correct else 'Incorrect'} Captcha text: {generated_text}/{answer}")
    return generated_text

if __name__ == "__main__":
    for file in os.listdir("tests/assets/"):
        read_captcha(f"tests/assets/{file}", file.split(".")[0])

    print(f"Correct: {correct}/{number_samples}")
