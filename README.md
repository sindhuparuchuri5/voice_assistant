# Voice Assistant Docker Image Setup and Usage Guide

This guide provides detailed instructions on how to set up and use the Voice Assistant Docker image.

## Table of Contents

- [Voice Assistant Docker Image Setup and Usage Guide](#voice-assistant-docker-image-setup-and-usage-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Prerequisites ](#1-prerequisites-)
  - [2. Building the Docker Image ](#2-building-the-docker-image-)
  - [3. Running the Container ](#3-running-the-container-)
  - [4. Interacting with the Voice Assistant ](#4-interacting-with-the-voice-assistant-)
  - [5. Additional Notes ](#5-additional-notes-)

## 1. Prerequisites <a name="prerequisites"></a>

Before proceeding, ensure that you have the following prerequisites installed on your system:

- Docker: Ensure that Docker is installed and running on your machine. You can download Docker from the official website: [Docker Download](https://www.docker.com/products/docker-desktop/).

- Git Bash (for Windows users): Git Bash provides a Unix-like command-line environment for Windows. It is required for running shell scripts within the Docker container. You can download Git Bash from the official website: [Git for Windows](https://git-scm.com/download/win).

## 2. Building the Docker Image <a name="building-the-docker-image"></a>

To build the Docker image, follow these steps:

1. Clone the repository containing the Voice_Assistant project files to your local machine:

   ```
   git clone https://github.com/sindhuparuchuri5/voice_assistant.git
   ```

2. Open a terminal or command prompt and navigate to the directory where the project files are located:

   ```
   cd voice_assistant
   ```

3. Run the following command to build the Docker image:

   ```
   docker build -t voice_assistant_image .
   ```

   This command will build the Docker image based on the provided Dockerfile and tag it with the name `voice_assistant_image`.

## 3. Running the Container <a name="running-the-container"></a>

Once the Docker image is built, you can run the container using the following steps:

1. Open a terminal or command prompt.

2. Run the following command to start the container:

   ```
   docker run -v "<LOCAL_LOGS_PATH>:/voice_assistant/logs" -e PULSE_SERVER=host.docker.internal --name voice_assistant_container -e DISPLAY=$DISPLAY --group-add audio voice_assistant_image
   ```

   Replace `<LOCAL_LOGS_PATH>` with the absolute path to the directory on your local machine where you want to store the interaction logs.

   - `-v "<LOCAL_LOGS_PATH>:/voice_assistant/logs"`: Mounts the local logs directory into the container at `/voice_assistant/logs`.
   - `-e PULSE_SERVER=host.docker.internal`: Sets the PulseAudio server address to `host.docker.internal` for audio support.
   - `--name voice_assistant_container`: Assigns a name to the container for easy reference.
   - `-e DISPLAY=$DISPLAY`: Enables display access for GUI applications.
   - `--group-add audio`: Adds the container to the audio group for audio support.

## 4. Interacting with the Voice Assistant <a name="interacting-with-the-voice-assistant"></a>

Once the container is running, you can interact with the Voice Assistant using speech input. Follow these steps to initiate interaction:

1. Ensure that the container is running successfully by checking the terminal or command prompt for any startup messages or errors.

2. Open a terminal or command prompt and navigate to the directory containing the project files.

3. Run the following command to start the voice assistant:

   ```
   chmod +x start.sh
   ./start.sh
   ```

   This script starts the PulseAudio server in the background and launches the voice assistant application within the container.

4. The voice assistant will greet you and prompt you to answer a series of questions. Speak your responses clearly into the microphone when prompted.

5. Follow the prompts and answer the questions presented by the voice assistant.

6. Once all questions are answered or if you decide to stop the interaction, the voice assistant will provide a closing message.

## 5. Additional Notes <a name="additional-notes"></a>

- PulseAudio Configuration: Ensure that your system has PulseAudio installed and configured correctly for audio support within the Docker container. If you haven't already, download and install PulseAudio from the official website: [PulseAudio Download](https://www.freedesktop.org/wiki/Software/PulseAudio/).

- Default.pa Configuration: After installing PulseAudio, locate the `default.pa` configuration file. For most systems, it can be found in the following directory: `C:\Program Files (x86)\PulseAudio\etc\pulse`. Edit the `default.pa` file and add the following line:

   ```
   load-module module-native-protocol-tcp auth-anonymous=1
   ```

   This line enables TCP support for PulseAudio, allowing communication between the Docker container and the host system.

- Git Bash Usage (Windows): If you're using Windows, you'll need to use Git Bash to run the `start.sh` script within the container. Git Bash provides a Unix-like command-line environment required for executing shell scripts.

- Logs Directory: The interaction logs generated by the voice assistant will be stored in the directory you specified when running the Docker container. You can access these logs on your local machine for reference.

