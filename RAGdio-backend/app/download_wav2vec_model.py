# from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
# from pathlib import Path

# MODEL_NAME = "facebook/wav2vec2-large-xlsr-53"
# TARGET_DIR = Path("models") / MODEL_NAME.replace("/", "-")

# def main():
#     print(f"⬇️ Downloading model '{MODEL_NAME}' to '{TARGET_DIR}'...")

#     processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME)
#     processor.save_pretrained(TARGET_DIR)

#     model = Wav2Vec2ForCTC.from_pretrained(MODEL_NAME)
#     model.save_pretrained(TARGET_DIR)

#     print("✅ Download complete.")

# if __name__ == "__main__":
#     main()


# Load model directly
from transformers import AutoProcessor, AutoModelForPreTraining

processor = AutoProcessor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
model = AutoModelForPreTraining.from_pretrained("facebook/wav2vec2-large-xlsr-53")

