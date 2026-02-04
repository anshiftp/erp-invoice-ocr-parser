import torch
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel

MODEL_NAME = "naver-clova-ix/donut-base-finetuned-cord-v2"

# Load model and processor
processor = DonutProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

def run_donut(image_path: str) -> dict:
    """
    Runs Donut OCR + understanding.
    Returns structured JSON (CORD-v2 schema).
    """
    # 1. Load Image
    image = Image.open(image_path).convert("RGB")

    # 2. Prepare Encoder Inputs (Image)
    pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)

    # 3. Prepare Decoder Inputs (Prompt)
    # add_special_tokens=False prevents the "R R R R..." infinite loop
    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(
        task_prompt, 
        add_special_tokens=False, 
        return_tensors="pt"
    ).input_ids.to(device)

    # 4. Generate Output
    outputs = model.generate(
        pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=768,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=1,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    # 5. Decode Output
    sequence = processor.batch_decode(outputs.sequences)[0]
    
    # 6. Post-processing to extract JSON
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = sequence.replace(task_prompt, "", 1) 

    print(f"DEBUG - Raw Sequence: {sequence[:100]}...") 

    return processor.token2json(sequence)