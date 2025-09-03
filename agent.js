const express = require('express');
const app = express();
const PORT = 4000;

const cors = require('cors');
app.use(cors());

app.use(express.json());

// In-memory user data (for demo/testing only)
const userData = {};

// Agent 1 (test agent) will POST the populated JSON here
app.post('/autofill-webhook', (req, res) => {
    const data = req.body;
    if (!data.username) {
        return res.status(400).json({ error: "Missing username in JSON" });
    }
    userData[data.username] = data;
    res.json({ status: "User JSON stored for: " + data.username });
});

// Frontend (application form) can GET the data to auto-fill for the logged-in user
app.get('/get-user-data/:username', (req, res) => {
    const username = req.params.username;
    if (!userData[username]) {
        return res.status(404).json({ error: "No data for user: " + username });
    }
    res.json(userData[username]);
});

app.listen(PORT, () => {
    console.log(`Playwright MCP agent server running at http://localhost:${PORT}`);
});

module.exports = { userData };