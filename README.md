<h1>Audio to Text</h1>
<p>Python program that will transcribe mp3 files to text whether you're online or offline.</p>
<h2>Getting Started</h2>
<p>First create a folder to place cloned git project into. Inside this folder also create a folder called “vosk_lang” to place vosk language models into. Go to the link: https://alphacephei.com/vosk/models To use Vosk models. Choose your desired language to transcribe in. In this repo, it is set up to use vosk-model-en-us-0.22. This can later be changed in the project files to suit your needs. Download the model into the folder that was created earlier called “vosk_lang” to be used later during set up.</p>
<h3>Prerequisites</h3>
<p>Have an IDE to run python such as pycharm. Have the Vosk model folder downloaded for use. Have git installed on the computer. A mp3 audio file to transcribe.</p>
<h3>Installing</h3>
<ol>
    <li>Go to your preferred python IDE.</li>
    <li>Then open up the terminal in that IDE.</li>
    <li>Navigate to the folder you created earlier for the git project.</li>
    <li>Once in said folder go to github and click on the green code button and choose the method of download (Usually it will be HTTPS)</li>
    <li>Copy link and go back to the IDE terminal and type “git clone {place coped url here}”. </li>
    <li>After hitting enter the repo will be cloned into that folder.</li>
    <li>Once done downloading, open project with your IDE and download the necessary packages.</li>
    <li>In the root of the project create 3 folders.</ br>
        <ul>
            <li>audio_files</li>
            <li>results</li>
            <li>vosk_lang</li>
        </ul>
    </li>
    <li>Inside the “vosk_lang” folder place the downloaded and unzipped model from vosk here.</li>
</ol>
<h2>Deployment</h2>
<p>After the setup is complete, run the main.py file. The conversion will take a few minutes depending on model type. While running the program will sound a notification sound to signify the completion of the program.</p>
<h2>Built With</h2>
Python - Programming language used
Vosk - Translation library
<h2>Authors</h2>
Andy Min - Creator
