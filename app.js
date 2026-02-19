const express = require("express");
const path = require("path");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const session = require("express-session");
const bcrypt = require("bcryptjs");
require('dotenv').config(); // For MONGO_URI

const app = express();


// View engine setup
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Serve static files
app.use(express.static(path.join(__dirname, "public")));

// Middleware to parse POST data
app.use(bodyParser.urlencoded({ extended: true }));

// Session
app.use(session({
    secret: 'yourSecretKey',
    resave: false,
    saveUninitialized: true
}));

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI || "mongodb://127.0.0.1:27017/geneanalyzer")
    .then(() => console.log("MongoDB connected"))
    .catch(err => console.log(err));

// Routes

app.get("/", (req, res) => {
    res.render("listings/home", { title: "PharmaGuard | RIFT 2026 Hackathon" });
});

app.get("/analysis", (req, res) => {
    res.render("listings/analysis", { title: "PharmaGuard | Analysis" });
});

app.get('/about', (req, res) => {
    res.render('listings/about'); 
});

app.get('/contact', (req, res) => {
    res.render('listings/contact'); 
});

// SIGN UP
app.get('/signup', (req, res) => {
    res.render('listings/signup');
});

app.post('/signup', async (req, res) => {
    const { name, email, password, confirmPassword } = req.body;

    if (!name || !email || !password || !confirmPassword) {
        return res.send("Please fill all fields.");
    }
    if (password !== confirmPassword) {
        return res.send("Passwords do not match.");
    }

    try {
        const existingUser = await User.findOne({ email });
        if (existingUser) return res.send("Email already registered.");

        const newUser = new User({ name, email, password });
        await newUser.save();

        // Redirect to login page after successful signup
        res.redirect('/signin');
    } catch (err) {
        console.error(err);
        res.send("Something went wrong.");
    }
});

// SIGN IN
app.get('/signin', (req, res) => {
    res.render('listings/login');
});

app.post('/signin', async (req, res) => {
    const { email, password } = req.body;

    try {
        const user = await User.findOne({ email });
        if (!user) return res.send('Invalid email or password.');

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) return res.send('Invalid email or password.');

        // Store in session
        req.session.userId = user._id;
        req.session.userName = user.name;

        // Redirect to home or dashboard after login
        res.send(`Welcome, ${user.name}! <a href="/">Go to Home</a>`);
    } catch (err) {
        console.error(err);
        res.send("Something went wrong.");
    }
});

// Optional: Logout
app.get('/logout', (req, res) => {
    req.session.destroy(() => {
        res.redirect('/signin');
    });
});

// Start server
app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});
