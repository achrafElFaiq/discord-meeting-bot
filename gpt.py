import google.generativeai as genai
import datetime
from config.api_secret import API_KEY_GEMINI
# Configure the API key
genai.configure(api_key=API_KEY_GEMINI)

# Path to your input text file
current_datetime = datetime.datetime.now()

# Format the date and time as a string (e.g., YYYY-MM-DD_HH-MM-SS)
formatted_datetime = current_datetime.strftime("%Y-%m-%d")
input_file = f"transcripts/transcript_{formatted_datetime}.txt"
output_file = "report.tex"

try:
    # Read the content of the file
    with open(input_file, "r", encoding="utf-8") as file:
        text_content = file.read()
    
    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Request LaTeX response directly
    response = model.generate_content(
        f"Analyze the following text and provide the analysis in LaTeX format: this is ameeting of our team about a project analyze it and give a summary in LaTeX format: \n{text_content}"
    )
    
    # Save the LaTeX response to a file
    with open(output_file, "w", encoding="utf-8") as latex_file:
        latex_file.write(response.text)
    
    print(f"Model's analysis in LaTeX format has been saved to {output_file}.")
except FileNotFoundError:
    print(f"The file {input_file} was not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred: {e}")