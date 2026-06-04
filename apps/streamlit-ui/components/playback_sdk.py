import streamlit.components.v1 as components

def render_spotify_player(access_token: str):
    """
    Injects the Spotify Web Playback SDK into the Streamlit app.
    It runs in an iframe and acts as a Spotify Connect device.
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Spotify Web Playback SDK</title>
      <style>
        body {{
            background-color: #121212;
            color: #ffffff;
            font-family: sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
        }}
        #status {{
            margin-bottom: 10px;
            font-size: 14px;
        }}
        .controls button {{
            background: #1DB954;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            margin: 0 5px;
        }}
        .controls button:hover {{
            background: #1ed760;
        }}
      </style>
    </head>
    <body>
      <div id="status">Initializing Spotify Player...</div>
      <div class="controls">
          <button id="togglePlay">Toggle Play</button>
          <button id="nextTrack">Next</button>
      </div>
      <script src="https://sdk.scdn.co/spotify-player.js"></script>
      <script>
        window.onSpotifyWebPlaybackSDKReady = () => {{
          const token = '{access_token}';
          const player = new Spotify.Player({{
            name: 'Spotigram Web Player',
            getOAuthToken: cb => {{ cb(token); }},
            volume: 0.5
          }});

          // Error handling
          player.addListener('initialization_error', ({{ message }}) => {{ console.error(message); document.getElementById('status').innerText = 'Init Error: ' + message; }});
          player.addListener('authentication_error', ({{ message }}) => {{ console.error(message); document.getElementById('status').innerText = 'Auth Error: ' + message; }});
          player.addListener('account_error', ({{ message }}) => {{ console.error(message); document.getElementById('status').innerText = 'Account Error: ' + message; }});
          player.addListener('playback_error', ({{ message }}) => {{ console.error(message); }});

          // Playback status updates
          player.addListener('player_state_changed', state => {{
            if (!state) return;
            const current_track = state.track_window.current_track;
            if (current_track) {{
                document.getElementById('status').innerText = 'Playing: ' + current_track.name + ' by ' + current_track.artists[0].name;
            }}
          }});

          // Ready
          player.addListener('ready', ({{ device_id }}) => {{
            console.log('Ready with Device ID', device_id);
            document.getElementById('status').innerText = 'Ready! Device ID: ' + device_id;
            
            // Post device_id back to streamlit if possible, or just keep it here
            // In a real app we'd use bi-directional streamlit components, but here we just show it.
          }});

          // Not Ready
          player.addListener('not_ready', ({{ device_id }}) => {{
            console.log('Device ID has gone offline', device_id);
          }});

          // Connect to the player!
          player.connect();

          document.getElementById('togglePlay').onclick = function() {{
              player.togglePlay();
          }};
          
          document.getElementById('nextTrack').onclick = function() {{
              player.nextTrack();
          }};
        }};
      </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=150)
