# Japanese Learning Subtitles for Kodi

A Kodi addon that provides real-time Japanese learning subtitles for streaming content. This addon uses OpenAI's Whisper for speech recognition and GPT-4 for translations, providing a three-line subtitle format:

1. Original Japanese text
2. Romaji pronunciation
3. Word-by-word English translation

## Features

- Real-time audio processing for streaming content
- Automatic Japanese transcription
- Romaji conversion
- Word-by-word translation
- Subtitle buffering and caching
- Works with any video source (streaming, local files, etc.)

## Requirements

- Kodi 19 or higher
- OpenAI API key
- Python packages:
  - requests
  - numpy
  - PyAudio
  - diskcache

## Installation

1. Download the latest release
2. Install in Kodi through "Install from zip file"
3. Configure your OpenAI API key in addon settings
4. Restart Kodi

## Configuration

### Basic Settings
- OpenAI API Key: Your API key from OpenAI
- Subtitle Buffer Size: Number of subtitle entries to keep in memory
- Cache Duration: How long to keep cached subtitles
- Debug Logging: Enable detailed logging

### Advanced Settings
- Clear Cache: Remove all cached subtitles
- Audio Chunk Size: Size of audio chunks for processing
- Sample Rate: Audio sample rate for processing

## Usage

1. Start playing any Japanese content in Kodi
2. The addon will automatically detect Japanese audio and begin processing
3. Subtitles will appear in the three-line format
4. Cached subtitles will be used if available for previously watched content

## Troubleshooting

### Common Issues

1. No subtitles appearing:
   - Check if OpenAI API key is correctly configured
   - Verify internet connection
   - Check Kodi error log for details

2. Delayed subtitles:
   - Adjust buffer size in settings
   - Check internet connection speed
   - Reduce audio chunk size in advanced settings

3. Incorrect translations:
   - Clear the subtitle cache
   - Ensure content has clear audio
   - Check if content is actually in Japanese

### Debug Logging

Enable debug logging in settings to get detailed information about the addon's operation. Logs can be found in Kodi's log file.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
