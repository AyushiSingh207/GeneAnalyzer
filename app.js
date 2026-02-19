const express = require("express");
const path = require("path");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const session = require("express-session");
const bcrypt = require("bcryptjs");
const fileUpload = require('express-fileupload');
const axios = require('axios');
const FormData = require('form-data');
require('dotenv').config(); // For MONGO_URI

const app = express();

// View engine setup
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Serve static files
app.use(express.static(path.join(__dirname, "public")));

// Middleware to parse POST data
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// File upload middleware
app.use(fileUpload());

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

// User Model (add this before routes)
const UserSchema = new mongoose.Schema({
    name: String,
    email: { type: String, unique: true },
    password: String,
    createdAt: { type: Date, default: Date.now }
});

// Hash password before saving
UserSchema.pre('save', async function(next) {
    if (!this.isModified('password')) return next();
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
});

const User = mongoose.model('User', UserSchema);

// ==================== ROUTES ====================

// Home Page
app.get("/", (req, res) => {
    res.render("listings/home", { 
        title: "PharmaGuard | RIFT 2026 Hackathon",
        user: req.session.userId ? { name: req.session.userName } : null
    });
});

// Analysis Page - GET
app.get("/analysis", (req, res) => {
    res.render("listings/analysis", { 
        title: "PharmaGuard | Analysis",
        user: req.session.userId ? { name: req.session.userName } : null,
        success: false,
        result: null,
        error: null
    });
});

// Analysis Page - POST (File Upload & API Call)
app.post('/analysis', async (req, res) => {
    try {
        // Check if file uploaded
        if (!req.files || !req.files.geneticFile) {
            return res.render('listings/analysis', { 
                title: 'Analysis - PharmaGuard',
                user: req.session.userId ? { name: req.session.userName } : null,
                error: 'No file uploaded. Please select a VCF file.',
                success: false,
                result: null
            });
        }

        const geneticFile = req.files.geneticFile;
        const drug = req.body.drug || 'warfarin';
        
        // Check file extension
        const fileExt = geneticFile.name.split('.').pop().toLowerCase();
        if (fileExt !== 'vcf') {
            return res.render('listings/analysis', { 
                title: 'Analysis - PharmaGuard',
                user: req.session.userId ? { name: req.session.userName } : null,
                error: 'Invalid file type. Please upload a .vcf file.',
                success: false,
                result: null
            });
        }

        // Create form data for Python backend
        const formData = new FormData();
        formData.append('patient_id', 'PAT' + Date.now());
        formData.append('drug', drug);
        formData.append('file', geneticFile.data, {
            filename: geneticFile.name,
            contentType: geneticFile.mimetype || 'text/plain'
        });

        console.log('Sending request to Python backend...');

        // Send to Python backend
        const response = await axios.post('http://localhost:8000/analyze', formData, {
            headers: {
                ...formData.getHeaders(),
                'Accept': 'application/json'
            },
            timeout: 30000 // 30 second timeout
        });

        console.log('Python backend response:', response.data);

        // Render result
        res.render('listings/analysis', {
            title: 'Analysis Result - PharmaGuard',
            user: req.session.userId ? { name: req.session.userName } : null,
            result: response.data,
            success: true,
            error: null
        });

    } catch (error) {
        console.error('Analysis error details:', error);
        
        let errorMessage = 'Something went wrong during analysis.';
        
        if (error.code === 'ECONNREFUSED') {
            errorMessage = 'Cannot connect to Python backend. Make sure Python server is running on port 8000.';
        } else if (error.response) {
            errorMessage = `Python backend error: ${error.response.data?.detail || error.response.statusText}`;
        } else if (error.request) {
            errorMessage = 'No response from Python backend. Please check if it\'s running.';
        } else if (error.message) {
            errorMessage = error.message;
        }

        res.render('listings/analysis', {
            title: 'Analysis - PharmaGuard',
            user: req.session.userId ? { name: req.session.userName } : null,
            error: errorMessage,
            success: false,
            result: null
        });
    }
});

// About Page
app.get('/about', (req, res) => {
    res.render('listings/about', {
        title: 'About - PharmaGuard',
        user: req.session.userId ? { name: req.session.userName } : null
    });
});

// Contact Page
app.get('/contact', (req, res) => {
    res.render('listings/contact', {
        title: 'Contact - PharmaGuard',
        user: req.session.userId ? { name: req.session.userName } : null
    });
});

// SIGN UP - GET
app.get('/signup', (req, res) => {
    res.render('listings/signup', {
        title: 'Sign Up - PharmaGuard',
        user: null
    });
});

// SIGN UP - POST
app.post('/signup', async (req, res) => {
    const { name, email, password, confirmPassword } = req.body;

    if (!name || !email || !password || !confirmPassword) {
        return res.render('listings/signup', {
            title: 'Sign Up - PharmaGuard',
            error: 'Please fill all fields.',
            user: null
        });
    }
    
    if (password !== confirmPassword) {
        return res.render('listings/signup', {
            title: 'Sign Up - PharmaGuard',
            error: 'Passwords do not match.',
            user: null
        });
    }

    try {
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.render('listings/signup', {
                title: 'Sign Up - PharmaGuard',
                error: 'Email already registered.',
                user: null
            });
        }

        const newUser = new User({ name, email, password });
        await newUser.save();

        // Redirect to login page after successful signup
        res.redirect('/signin?registered=true');
    } catch (err) {
        console.error(err);
        res.render('listings/signup', {
            title: 'Sign Up - PharmaGuard',
            error: 'Something went wrong. Please try again.',
            user: null
        });
    }
});

// SIGN IN - GET
app.get('/signin', (req, res) => {
    const registered = req.query.registered === 'true';
    res.render('listings/login', {
        title: 'Sign In - PharmaGuard',
        registered: registered,
        error: null,
        user: null
    });
});

// SIGN IN - POST
app.post('/signin', async (req, res) => {
    const { email, password } = req.body;

    try {
        const user = await User.findOne({ email });
        if (!user) {
            return res.render('listings/login', {
                title: 'Sign In - PharmaGuard',
                error: 'Invalid email or password.',
                registered: false,
                user: null
            });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.render('listings/login', {
                title: 'Sign In - PharmaGuard',
                error: 'Invalid email or password.',
                registered: false,
                user: null
            });
        }

        // Store in session
        req.session.userId = user._id;
        req.session.userName = user.name;

        // Redirect to home after login
        res.redirect('/');
    } catch (err) {
        console.error(err);
        res.render('listings/login', {
            title: 'Sign In - PharmaGuard',
            error: 'Something went wrong.',
            registered: false,
            user: null
        });
    }
});

// Logout
app.get('/logout', (req, res) => {
    req.session.destroy(() => {
        res.redirect('/signin');
    });
});

// 404 Page
app.use((req, res) => {
    res.status(404).render('listings/404', {
        title: 'Page Not Found - PharmaGuard',
        user: req.session.userId ? { name: req.session.userName } : null
    });
});

// Start server
app.listen(3000, () => {
    console.log("🚀 Server running on http://localhost:3000");
    console.log("📝 Make sure Python backend is running on http://localhost:8000");
});