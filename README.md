<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #222;
      color: #fff;
      text-align: center;
      margin: 0;
      padding: 0;
    }
    .header {
      background-color: #0078D4;
      padding: 20px;
    }
    .header img {
      width: 200px;
    }
    .app-title {
      font-size: 24px;
      margin-top: 10px;
    }
    .features {
      margin: 20px 0;
      padding: 0;
      list-style-type: none;
    }
    .features li {
      margin: 10px 0;
      font-size: 18px;
    }
    .screenshot {
      margin: 20px auto;
      max-width: 90%;
    }
    .getting-started {
      text-align: left;
      margin: 20px 0;
    }
    .getting-started ol {
      list-style-position: inside;
    }
    .getting-started code {
      background-color: #333;
      color: #fff;
      padding: 2px 4px;
      border-radius: 3px;
    }
    .usage {
      text-align: left;
      margin: 20px 0;
    }
  </style>
</head>
<body>
  <div class="header">
    <img src="logo.png" alt="Capsolver Balance Checker Logo">
    <div class="app-title">Capsolver Balance Checker</div>
  </div>
  <h2>Features</h2>
  <ul class="features">
    <li>User-Friendly Interface: Enjoy a modern, intuitive interface with dark mode styling.</li>
    <li>Check Balance: Easily check your Capsolver account balance by entering your API key.</li>
    <li>Auto Check Balance: Enable automatic balance checks at regular intervals.</li>
    <li>API Actions: Create tasks, get task results, and retrieve your Capsolver account state.</li>
  </ul>
  <img class="screenshot" src="https://media.discordapp.net/attachments/1146143667187372142/1146982106191376404/image.png" alt="App Screenshot 1">
  <h2>Getting Started</h2>
  <div class="getting-started">
    <ol>
      <li>Clone this repository to your local machine:</li>
      <pre><code>git clone https://github.com/your-username/capsolver-balance-checker.git</code></pre>
      <li>Install the required dependencies:</li>
      <pre><code>pip install -r requirements.txt</code></pre>
      <li>Run the application:</li>
      <pre><code>python main.py</code></pre>
    </ol>
  </div>
  <h2>Usage</h2>
  <div class="usage">
    <ul>
      <li>Check Balance: Enter your API key and click "Check Balance" to see your account balance.</li>
      <li>Auto Check Balance: Enable automatic balance checks by clicking the checkbox.</li>
      <li>API Actions: Use the tabs on the sidebar to create tasks, get task results, or view your Capsolver account state.</li>
    </ul>
  </div>
</body>
</html>
