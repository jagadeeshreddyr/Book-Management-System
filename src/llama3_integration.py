from transformers import BartTokenizer, BartForConditionalGeneration
import os

class Llama3Model:
    def __init__(self, model_path):
        self.tokenizer = BartTokenizer.from_pretrained(model_path)
        self.model = BartForConditionalGeneration.from_pretrained(model_path)

    def generate_summary(self, text):
        inputs = self.tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary

# Initialize the Llama3 model (assuming the model is loaded locally)
model = Llama3Model(model_path="facebook/bart-large-cnn")

def generate_summary(text):
    return model.generate_summary(text)
    
if __name__ == "__main__":

    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)

    text = "Your long text here..."
    summary = generate_summary(text)
    print("Summary:", summary)