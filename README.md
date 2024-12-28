<body>

   # Yada-Yada: Chat Like It’s Nobody’s Business! 💬

   <p>Have you ever wanted to quickly send messages to your internal network in a simple and secure way? Well, we have something that will make you go, "Yada-Yada!" 🤖</p>

 <p><strong>Yada-Yada Chat</strong> could be your new favorite real-time chat application. It's like texting, but cooler and faster! (Okay, maybe not faster... but it's real-time, which is still pretty cool, right?)</p>

   <h2>What’s So Cool About It?</h2>
    <ul>
        <li>Real-time chat using WebSockets! No more refreshing your browser like it’s 2005. 😎</li>
        <li>User authentication via PIN! (Because we like to keep things secure... no random strangers in here.)</li>
        <li>Get a nickname! Be whoever you want to be. Just, you know, keep it cool. 🕶️</li>
        <li>Upload your images! Share your memes, cats, and the occasional pizza picture. 🍕📸</li>
        <li>It’s lightweight, simple, and ONLY for your internal network. So, no prying eyes. 🛑</li>
    </ul>

 <h2>Getting Started</h2>
    <p>So you want to set this thing up? Buckle up, because here’s how you get it running on your local network in just a few easy steps:</p>

   <ol>
        <li>Clone the repo, because why not? This is the 21st century!</li>
        <pre><code>git clone https://github.com/goro-dim/YadaYada.git</code></pre>
                <li>Enter the project directory like a boss:</li>
        <pre><code>cd YadaYada</code></pre>
        <li>Install dependencies. Get that app to do its thing:</li>
        <pre><code>pip install -r requirements.txt</code></pre>

   <li>Make sure to set up your <code>config.json</code> file like a pro:</li>
        <pre><code>
        {
            "pin": "yourpin", 
            "max_file_size": 1000000, 
            "allowed_mime_types": ["image/png", "image/jpeg"],
            "host_ip": "IP_ADRESS"
        }
        </code></pre>
        <p>Just a heads-up: make sure that PIN is a secret, or you might have uninvited guests! 😜</p>
     <li>Run the server like it’s the last game of the season:</li>
        <pre><code>uvicorn server.main:app --reload --host 0.0.0.0 --port 8000</code></pre>
        <p><strong>IMPORTANT: This chat app is meant for <em>internal network use only</em>. We don’t want any uninvited hackers showing up. If you want to expose this to the internet... well, we *strongly* suggest putting on some security armor first! ⚔️</strong></p>
    </ol>

   <h2>How to Use It (Because You’re Here For a Reason)</h2>
    <p>Once the server is up and running (and you’ve probably celebrated with a dance move or two), you can chat away by visiting:</p>
    <pre><code>http://(<)your_server_ip(>):8000</code></pre>

   <p>Now YadaYada as much as you want and have fun! 🕶️💬</p>

   <h2>Warning: Don’t Expose to the Public (Unless You Really Like Drama)</h2>
    <p>Just to be crystal clear: this app is designed to be used on an internal network. Exposing it to the public internet without proper security measures is like leaving your door open with a "Free Wi-Fi" sign outside. It's just... not a good idea. 🚪🔓</p>


</body>
