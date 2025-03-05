# Totoko - A Discord AI Bot

Totoko is a Discord bot that integrates AI-powered chat responses, music playback, and interactive games. The bot is designed to provide entertainment and utility features to Discord users, with a playful personality inspired by anime and gaming culture.

## Features

- **AI Chatbot:** Responds to user messages using a fine-tuned AI model.
- **Music Player:** Plays, manages, and searches for music within a predefined library.
- **Voice Channel Interaction:** Joins and leaves voice channels, plays music, and manages playlists.
- **Games & Fun Commands:** Includes rock-paper-scissors and other interactive features.
- **Customizable Personality:** Replies in a playful and engaging manner.

## Installation

### Prerequisites
- Python 3.8+
- Discord bot token
- FFmpeg installed for audio processing
- PyTorch (for AI model inference)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/totoko.git
   cd totoko
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your bot:
   - Create a `.env` file or modify the script to include your **Discord bot token**.
   - Ensure your **music_base_list.txt** file contains the list of songs.
4. Run the bot:
   ```bash
   python totoko.py
   ```
   You will be prompted to enter your bot token when running the script.

## Usage

### Commands
- `!hello` - Greets the user.
- `!join` - Makes the bot join a voice channel.
- `!leave` - Makes the bot leave a voice channel.
- `!play <song_name>` - Plays a song from the predefined library.
- `!random_play` - Plays random songs.
- `!all_play` - Plays all available songs in order.
- `!music_list` - Lists all available songs.
- `!play_list` - Shows the current playlist.
- `!stop` - Stops music playback.
- `!continue` - Resumes paused music.
- `!skip` - Skips the current song.
- `!rps` - Plays rock-paper-scissors with the bot.
- `!search` - Searches for a song in the library.

## AI Model
- The bot uses **Qwen/Qwen2.5-7B-Instruct-1M** with **LoRA fine-tuning** for AI-based responses.
- The model is loaded with 4-bit quantization to optimize performance.

## Contributing
Feel free to fork the repository and submit pull requests with improvements or additional features.

## License
MIT License

## Contact
For questions or suggestions, contact ycy20011234@gmail.com.

