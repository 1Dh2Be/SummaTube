# SummaTube - YouTube Video Summarizer 🚀
**SummaTube** is an application that provides **concise summaries** of YouTube videos, making it easier for users to quickly grasp the **main points** of a video without watching it in its entirety, **which saves you a bunch of your precious time** :-)

Additionally, **SummaTube** enables users to **ask specific questions** about the video content, providing **targeted information** based on the video.

The application utilizes **Anthropic's API** for generating accurate summaries and **AssemblyAI's API** for text extraction.

## Features 🛠️

- Summarize YouTube videos by providing the video URL
- Possibility to ask tailored questions
- Categorize videos by genre for easy navigation
- Store and manage video summaries in a database
- User-friendly app interface for seamless interaction

## Getting Started 🔰

### Prerequisites
- [Python 3.9+](https://www.python.org/downloads): The programming language used for the project.
- [Anaconda](https://www.anaconda.com/download/success): Used to download and manage dependencies.

### Installation

1. Clone the repository:

   ```
   git clone git@github.com:1Dh2Be/SummaTube.git
   ```

2. Navigate to the project directory:

   ```
   cd SummaTube
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up the necessary API keys:
   - Obtain an API key from [Anthropic](https://www.anthropic.com/) and [AssemblyAI](https://www.assemblyai.com/).
   - Create a python file named `api_keys.py` in the src directory and add the following lines, replacing `<your_api_key>` with your actual API keys:
     ```
     ANTHROPIC_API_KEY=<your_api_key>
     ASSEMBLYAI_API_KEY=<your_api_key>
     ```

5. Run the application:

   ```
   python src/app.py
   ```
6. Explore the features!

## Usage 📖

### Summarizing a YouTube Video

1. Open the SummaTube application in your web browser.
2. You will be prompted with the following options:

   Please choose one of these options:

      ```1. Enter video URL.```
   
      ```2. Exit.```

3. Enter `1` to proceed with entering the YouTube video URL.
4. Enter the URL of the YouTube video you want to summarize.

**Note:** SummaTube currently supports summarization and question-answering for English videos only.

5. After the URL is correctly processed, the following options will be displayed:

      Please choose one of this options:

      ```1) Get text.```
   
      ```2) Summarize video.```
   
      ```3) Ask questions about video.```
   
      ```4) Exit.```
   
7. Enter `2` for the application to process the video and generate the summary.
8. The summary will be displayed on the page.

### Asking Questions about a Video
   
1. Enter `3` to ask your question related to the video content in the provided input field.
2. The application will process your question and provide a relevant answer based on the video content.
3. After the aplication answered your question, you can ask another one or type 'quit' to stop asking questions.

### Get the text of video

Additionally, you can get the text of the video by entering `1` 

## Limitations ⚠️

- **Language Support**: Currently, SummaTube supports summarization and question-answering for English videos only. Passing a video in a language other than English may result in unexpected or inaccurate outputs.

- **Video Source**: SummaTube currently works exclusively with YouTube video links. Providing links from other social platforms or video hosting sites is not supported at the moment.

- **Database Interaction**: Interacting with the database (e.g., storing, managing, or retrieving video summaries) is not possible through the application's user interface yet. Database operations need to be performed directly in the codebase.

---

For any further questions or inquiries, please contact me on [LinkedIn](www.linkedin.com/in/mimoun-atmani).
